import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from backend.models import AuthSession, User

PBKDF2_ITERATIONS = 600_000


class InvalidCredentials(ValueError):
    pass


def hash_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(iterations))
        return hmac.compare_digest(actual, bytes.fromhex(expected))
    except (TypeError, ValueError):
        return False


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class AuthService:
    def __init__(self, db: Session, token_ttl_minutes: int = 480):
        self.db = db
        self.token_ttl_minutes = token_ttl_minutes

    def authenticate(self, username: str, password: str) -> tuple[str, AuthSession, User]:
        user = self.db.scalar(select(User).where(User.username == username.strip().lower()))
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentials("Invalid username or password")
        now = datetime.now(timezone.utc)
        self.db.execute(delete(AuthSession).where(AuthSession.expires_at <= now))
        token = secrets.token_urlsafe(48)
        session = AuthSession(user_id=user.id, token_hash=token_digest(token), expires_at=now + timedelta(minutes=self.token_ttl_minutes))
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return token, session, user

    def user_for_token(self, token: str) -> User | None:
        now = datetime.now(timezone.utc)
        statement = select(User).join(AuthSession).where(AuthSession.token_hash == token_digest(token), AuthSession.expires_at > now)
        return self.db.scalar(statement)

    def create_user(self, username: str, email: str, password: str, role: str = "analyst") -> User:
        normalized = username.strip().lower()
        if self.db.scalar(select(User).where((User.username == normalized) | (User.email == email.strip().lower()))):
            raise ValueError("Username or email already exists")
        user = User(username=normalized, email=email.strip().lower(), password_hash=hash_password(password), role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def bootstrap_admin(self, username: str, email: str, password: str | None) -> None:
        if not password or self.db.scalar(select(User.id).limit(1)):
            return
        self.create_user(username, email, password, "admin")
