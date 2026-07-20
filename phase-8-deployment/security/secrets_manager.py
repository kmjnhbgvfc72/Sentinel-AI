import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken


class SecretsManager:
    """Environment/file secret adapter; replace the provider method for Vault/KMS."""
    def get(self, name: str, required: bool = True) -> str | None:
        value = os.getenv(name)
        file_path = os.getenv(f"{name}_FILE")
        if not value and file_path:
            value = Path(file_path).read_text(encoding="utf-8").strip()
        if required and not value:
            raise RuntimeError(f"Required secret {name} is unavailable")
        return value

    def encrypt(self, plaintext: str) -> str:
        key = self.get("ENCRYPTION_KEY")
        return Fernet(key.encode()).encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        key = self.get("ENCRYPTION_KEY")
        try:
            return Fernet(key.encode()).decrypt(ciphertext.encode()).decode()
        except InvalidToken as exc:
            raise ValueError("Ciphertext authentication failed") from exc

