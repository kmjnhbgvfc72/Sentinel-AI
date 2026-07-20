"""Create the requested development administrator with a hashed password."""

import argparse

from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from backend.database import SessionLocal, initialize_database
from backend.models import User
from backend.services.auth_service import AuthService, hash_password
from backend.scripts.database_cli import database_connection_error

DEVELOPMENT_USERNAME = "admin"
DEVELOPMENT_PASSWORD = "admin123"
DEVELOPMENT_EMAIL = "admin@localhost"


def create_admin(*, reset_password: bool = False) -> User:
    initialize_database()
    with SessionLocal() as db:
        existing = db.scalar(select(User).where(User.username == DEVELOPMENT_USERNAME))
        if existing:
            if reset_password:
                existing.password_hash = hash_password(DEVELOPMENT_PASSWORD)
                existing.role = "admin"
                db.commit()
                db.refresh(existing)
                print("Development admin password and role updated.")
            else:
                print("Development admin already exists; no changes made.")
            return existing
        user = AuthService(db).create_user(
            DEVELOPMENT_USERNAME,
            DEVELOPMENT_EMAIL,
            DEVELOPMENT_PASSWORD,
            role="admin",
        )
        print("Development admin created. Change its password before non-development use.")
        return user


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the development SOC administrator.")
    parser.add_argument("--reset-password", action="store_true", help="Reset an existing admin to the development password.")
    args = parser.parse_args()
    try:
        create_admin(reset_password=args.reset_password)
    except OperationalError as exc:
        raise database_connection_error(exc) from None


if __name__ == "__main__":
    main()
