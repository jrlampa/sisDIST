"""Security utilities for sisDIST."""
import hashlib
import secrets


def generate_secret_key(length: int = 32) -> str:
    """Generate a cryptographically secure random key."""
    return secrets.token_hex(length)


def hash_string(value: str) -> str:
    """SHA-256 hash a string (for non-sensitive identifiers)."""
    return hashlib.sha256(value.encode()).hexdigest()
