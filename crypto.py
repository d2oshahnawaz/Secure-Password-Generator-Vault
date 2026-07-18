# =====================================================
# PASSWORD VAULT CRYPTO
# Version 5.0 Professional
# Part 1
# =====================================================

from __future__ import annotations

from pathlib import Path
from typing import Final
import hashlib
import logging
import shutil

from cryptography.fernet import (
    Fernet,
    InvalidToken,
)

# =====================================================
# LOGGING
# =====================================================

logger = logging.getLogger(__name__)

# =====================================================
# CONSTANTS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

KEY_FILE = BASE_DIR / "vault.key"

BACKUP_KEY_FILE = BASE_DIR / "vault.key.bak"

ENCODING: Final[str] = "utf-8"

# =====================================================
# KEY GENERATION
# =====================================================

def generate_key() -> bytes:
    """
    Generate and store a new encryption key.
    """

    key = Fernet.generate_key()

    KEY_FILE.write_bytes(key)

    logger.info("Encryption key generated.")

    return key

# =====================================================
# LOAD KEY
# =====================================================

def load_key() -> bytes:
    """
    Load encryption key.
    Automatically creates one if missing.
    """

    if not KEY_FILE.exists():

        logger.warning(
            "Encryption key not found. Creating a new one."
        )

        return generate_key()

    key = KEY_FILE.read_bytes()

    try:

        Fernet(key)

    except Exception as exc:

        logger.exception(
            "Invalid encryption key."
        )

        raise ValueError(
            "Encryption key is invalid."
        ) from exc

    return key

# =====================================================
# KEY EXISTS
# =====================================================

def key_exists() -> bool:
    """
    Return True if key exists.
    """

    return KEY_FILE.exists()

# =====================================================
# DELETE KEY
# =====================================================

def delete_key() -> bool:
    """
    Delete encryption key.
    """

    try:

        if KEY_FILE.exists():

            KEY_FILE.unlink()

            logger.info(
                "Encryption key deleted."
            )

        return True

    except OSError as exc:

        logger.exception(exc)

        return False

# =====================================================
# ROTATE KEY
# =====================================================

def rotate_key() -> bytes:
    """
    Rotate encryption key.

    Existing encrypted passwords
    cannot be decrypted afterwards.
    """

    if KEY_FILE.exists():

        backup_key()

    delete_key()

    return generate_key()

# =====================================================
# BACKUP KEY
# =====================================================

def backup_key() -> bool:
    """
    Create a backup of the encryption key.
    """

    try:

        if KEY_FILE.exists():

            shutil.copy2(
                KEY_FILE,
                BACKUP_KEY_FILE,
            )

            logger.info(
                "Encryption key backup created."
            )

            return True

    except Exception as exc:

        logger.exception(exc)

    return False

# =====================================================
# RESTORE KEY
# =====================================================

def restore_key() -> bool:
    """
    Restore encryption key
    from backup.
    """

    try:

        if BACKUP_KEY_FILE.exists():

            shutil.copy2(
                BACKUP_KEY_FILE,
                KEY_FILE,
            )

            logger.info(
                "Encryption key restored."
            )

            return True

    except Exception as exc:

        logger.exception(exc)

    return False

# =====================================================
# KEY FINGERPRINT
# =====================================================

def key_fingerprint() -> str:
    """
    Return SHA-256 fingerprint
    of current encryption key.
    """

    if not key_exists():

        return "Unavailable"

    digest = hashlib.sha256(
        load_key()
    ).hexdigest()

    return digest[:16].upper()

# =====================================================
# KEY INFORMATION
# =====================================================

def key_info() -> dict:
    """
    Return encryption key details.
    """

    return {

        "exists": key_exists(),

        "path": str(KEY_FILE),

        "backup_exists": BACKUP_KEY_FILE.exists(),

        "fingerprint": key_fingerprint(),

    }

# =====================================================
# CIPHER
# =====================================================

def get_cipher() -> Fernet:
    """
    Return a validated Fernet cipher instance.
    """

    return Fernet(load_key())


# =====================================================
# ENCRYPT PASSWORD
# =====================================================

def encrypt_password(password: str) -> str:
    """
    Encrypt a plaintext password.

    Parameters
    ----------
    password : str
        Plaintext password.

    Returns
    -------
    str
        Encrypted password.
    """

    if not password:
        return ""

    try:

        cipher = get_cipher()

        encrypted = cipher.encrypt(
            password.encode(ENCODING)
        )

        return encrypted.decode(ENCODING)

    except Exception as exc:

        logger.exception(
            "Password encryption failed."
        )

        raise RuntimeError(
            "Unable to encrypt password."
        ) from exc


# =====================================================
# DECRYPT PASSWORD
# =====================================================

def decrypt_password(
    encrypted_password: str,
) -> str:
    """
    Decrypt an encrypted password.

    Parameters
    ----------
    encrypted_password : str
        Fernet encrypted password.

    Returns
    -------
    str
        Plaintext password.
    """

    if not encrypted_password:
        return ""

    try:

        cipher = get_cipher()

        decrypted = cipher.decrypt(
            encrypted_password.encode(ENCODING)
        )

        return decrypted.decode(ENCODING)

    except InvalidToken as exc:

        logger.exception(
            "Invalid encryption token."
        )

        raise ValueError(
            "Unable to decrypt password. "
            "The encryption key is invalid or "
            "the encrypted data is corrupted."
        ) from exc

    except Exception as exc:

        logger.exception(
            "Password decryption failed."
        )

        raise RuntimeError(
            "Unexpected decryption error."
        ) from exc


# =====================================================
# VERIFY ENCRYPTION
# =====================================================

def verify_encryption(
    password: str,
) -> bool:
    """
    Verify encryption integrity.
    """

    if not password:
        return False

    encrypted = encrypt_password(password)

    decrypted = decrypt_password(encrypted)

    return password == decrypted


# =====================================================
# BATCH ENCRYPTION
# =====================================================

def encrypt_passwords(
    passwords: list[str],
) -> list[str]:
    """
    Encrypt multiple passwords.
    """

    return [
        encrypt_password(password)
        for password in passwords
    ]


# =====================================================
# BATCH DECRYPTION
# =====================================================

def decrypt_passwords(
    encrypted_passwords: list[str],
) -> list[str]:
    """
    Decrypt multiple passwords.
    """

    return [
        decrypt_password(password)
        for password in encrypted_passwords
    ]


# =====================================================
# ENCRYPTION STATUS
# =====================================================

def encryption_status() -> dict:
    """
    Return current encryption status.
    """

    return {

        "algorithm": "Fernet",

        "encoding": ENCODING,

        "key_exists": key_exists(),

        "fingerprint": key_fingerprint(),

        "backup_available": BACKUP_KEY_FILE.exists(),

    }

# =====================================================
# CRYPTO INFORMATION
# =====================================================

def crypto_info() -> dict:
    """
    Return crypto module information.
    """

    return {

        "algorithm": "Fernet",

        "encoding": ENCODING,

        "key_file": str(KEY_FILE),

        "backup_key_file": str(BACKUP_KEY_FILE),

        "key_exists": key_exists(),

        "backup_exists": BACKUP_KEY_FILE.exists(),

        "fingerprint": key_fingerprint(),

    }


# =====================================================
# CRYPTO HEALTH CHECK
# =====================================================

def crypto_health_check() -> dict:
    """
    Perform a crypto health check.
    """

    report = {

        "healthy": True,

        "issues": [],

    }

    if not key_exists():

        report["healthy"] = False

        report["issues"].append(
            "Encryption key is missing."
        )

        return report

    try:

        load_key()

    except Exception as exc:

        report["healthy"] = False

        report["issues"].append(str(exc))

    return report


# =====================================================
# ENCRYPTION BENCHMARK
# =====================================================

def benchmark_encryption() -> bool:
    """
    Test encryption pipeline.
    """

    sample = "Password@123"

    encrypted = encrypt_password(sample)

    decrypted = decrypt_password(encrypted)

    return sample == decrypted


# =====================================================
# MODULE SELF TEST
# =====================================================

if __name__ == "__main__":

    SAMPLE_PASSWORD = "Mohd@1234"

    print("=" * 60)
    print("Password Vault Crypto Test")
    print("=" * 60)

    print()

    print("Key Information")
    print(key_info())

    print()

    print("Crypto Information")
    print(crypto_info())

    print()

    print("Health Check")
    print(crypto_health_check())

    print()

    print("Original Password")
    print(SAMPLE_PASSWORD)

    print()

    encrypted = encrypt_password(
        SAMPLE_PASSWORD
    )

    print("Encrypted Password")
    print(encrypted)

    print()

    decrypted = decrypt_password(
        encrypted
    )

    print("Decrypted Password")
    print(decrypted)

    print()

    print(
        "Verification :",
        verify_encryption(
            SAMPLE_PASSWORD
        )
    )

    print()

    print(
        "Benchmark :",
        benchmark_encryption()
    )

    print()

    print(
        "Encryption Status"
    )

    print(
        encryption_status()
    )

    print()

    print("=" * 60)

# =====================================================
# END OF FILE
# crypto.py
# Version 5.0 Professional
# =====================================================