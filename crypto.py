# =====================================================
# PASSWORD VAULT CRYPTO
# Version 4.1 Professional
# Fernet Authenticated Encryption
# =====================================================

from __future__ import annotations

from pathlib import Path
from typing import Final

from cryptography.fernet import (
    Fernet,
    InvalidToken,
)

# =====================================================
# CONSTANTS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

KEY_FILE = BASE_DIR / "vault.key"

ENCODING: Final[str] = "utf-8"

# =====================================================
# KEY MANAGEMENT
# =====================================================

def generate_key() -> bytes:
    """
    Generate a new encryption key and save it.
    """

    key = Fernet.generate_key()

    KEY_FILE.write_bytes(key)

    return key


def load_key() -> bytes:
    """
    Load encryption key.
    Automatically creates one if missing.
    """

    if not KEY_FILE.exists():

        return generate_key()

    key = KEY_FILE.read_bytes()

    try:

        Fernet(key)

    except Exception as exc:

        raise ValueError(
            "Encryption key is invalid."
        ) from exc

    return key


def key_exists() -> bool:
    """
    Check whether the encryption key exists.
    """

    return KEY_FILE.exists()


def delete_key() -> bool:
    """
    Delete encryption key.
    """

    try:

        if KEY_FILE.exists():

            KEY_FILE.unlink()

        return True

    except OSError:

        return False


def rotate_key() -> bytes:
    """
    Replace the existing encryption key
    with a newly generated key.

    NOTE:
    Existing encrypted passwords
    cannot be decrypted afterwards.
    """

    delete_key()

    return generate_key()


# =====================================================
# CIPHER
# =====================================================

def get_cipher() -> Fernet:
    """
    Return a Fernet cipher instance.
    """

    return Fernet(load_key())


# =====================================================
# ENCRYPT
# =====================================================

def encrypt_password(password: str) -> str:
    """
    Encrypt a plaintext password.
    """

    if not password:

        return ""

    cipher = get_cipher()

    encrypted = cipher.encrypt(

        password.encode(ENCODING)

    )

    return encrypted.decode(ENCODING)


# =====================================================
# DECRYPT
# =====================================================

def decrypt_password(
    encrypted_password: str
) -> str:
    """
    Decrypt an encrypted password.
    """

    if not encrypted_password:

        return ""

    cipher = get_cipher()

    try:

        decrypted = cipher.decrypt(

            encrypted_password.encode(
                ENCODING
            )

        )

        return decrypted.decode(
            ENCODING
        )

    except InvalidToken as exc:

        raise ValueError(

            "Unable to decrypt password. "
            "The encryption key may be invalid "
            "or the encrypted data is corrupted."

        ) from exc


# =====================================================
# VERIFY ENCRYPTION
# =====================================================

def verify_encryption(
    password: str
) -> bool:
    """
    Verify encryption integrity.
    """

    encrypted = encrypt_password(
        password
    )

    decrypted = decrypt_password(
        encrypted
    )

    return password == decrypted


# =====================================================
# INFORMATION
# =====================================================

def crypto_info() -> dict:
    """
    Return crypto module information.
    """

    return {

        "algorithm": "Fernet",

        "encoding": ENCODING,

        "key_file": str(KEY_FILE),

        "key_exists": key_exists(),

    }


# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    SAMPLE_PASSWORD = "Mohd@1234"

    print("=" * 60)

    print("Password Vault Crypto Test")

    print("=" * 60)

    print("Key Exists :", key_exists())

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

    print("Crypto Information")

    print(crypto_info())

    print("=" * 60)