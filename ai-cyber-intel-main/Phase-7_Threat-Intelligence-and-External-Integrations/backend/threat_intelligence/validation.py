import ipaddress
import re
from urllib.parse import urlsplit, urlunsplit

DOMAIN_PATTERN = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$", re.I)
HASH_LENGTHS = {32: "md5", 40: "sha1", 64: "sha256"}


class IOCValidationError(ValueError):
    pass


def normalize_ioc(ioc_type: str, value: str) -> str:
    kind = ioc_type.strip().lower()
    raw = value.strip()
    if not raw or len(raw) > 2048:
        raise IOCValidationError("IOC value must contain 1 to 2048 characters")
    if kind == "ip":
        try:
            return str(ipaddress.ip_address(raw))
        except ValueError as exc:
            raise IOCValidationError("Invalid IP address") from exc
    if kind == "domain":
        normalized = raw.rstrip(".").lower().encode("idna").decode("ascii")
        if not DOMAIN_PATTERN.fullmatch(normalized):
            raise IOCValidationError("Invalid domain")
        return normalized
    if kind == "url":
        parts = urlsplit(raw)
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
            raise IOCValidationError("URL must be HTTP(S) and must not contain credentials")
        host = parts.hostname.lower().encode("idna").decode("ascii")
        port = f":{parts.port}" if parts.port else ""
        return urlunsplit((parts.scheme.lower(), host + port, parts.path or "/", parts.query, ""))
    if kind == "hash":
        normalized = raw.lower()
        if len(normalized) not in HASH_LENGTHS or not re.fullmatch(r"[a-f0-9]+", normalized):
            raise IOCValidationError("Hash must be a valid MD5, SHA-1, or SHA-256 value")
        return normalized
    if kind == "email":
        if raw.count("@") != 1:
            raise IOCValidationError("Invalid email indicator")
        local, domain = raw.rsplit("@", 1)
        if not local or not DOMAIN_PATTERN.fullmatch(domain):
            raise IOCValidationError("Invalid email indicator")
        return f"{local}@{domain.lower()}"
    raise IOCValidationError("IOC type must be ip, domain, url, hash, or email")
