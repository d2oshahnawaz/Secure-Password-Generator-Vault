# =====================================================
# MASTER PASSWORD MANAGER
# Version 5.0 Professional
# Part 1 / 3
# =====================================================

from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# =====================================================
# CONSTANTS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

MASTER_FILE = BASE_DIR / "master.json"

ITERATIONS = 200_000

SALT_LENGTH = 16

HASH_ALGORITHM = "sha256"

RECOVERY_KEY_GROUPS = 4

RECOVERY_KEY_LENGTH = 4

DEFAULT_SECURITY_QUESTIONS = [

    "What is your first school?",

    "What is your mother's first name?",

    "What is your favorite teacher's name?",

    "What is your childhood nickname?",

    "What city were you born in?",

]

# =====================================================
# INTERNAL FUNCTIONS
# =====================================================

def _hash_password(
    password: str,
    salt: bytes,
) -> str:
    """
    Generate PBKDF2 password hash.
    """

    return hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    ).hex()


def _current_timestamp() -> str:
    """
    Return current timestamp.
    """

    return datetime.now().isoformat(timespec="seconds")


def generate_recovery_key() -> str:
    """
    Generate a secure recovery key.

    Example:
    A1B2-C3D4-E5F6-G7H8
    """

    groups = []

    for _ in range(RECOVERY_KEY_GROUPS):

        groups.append(

            secrets.token_hex(
                RECOVERY_KEY_LENGTH // 2
            ).upper()

        )

    return "-".join(groups)


def _load_master_data() -> Dict[str, Any]:
    """
    Load master password data.
    """

    if not MASTER_FILE.exists():

        return {}

    try:

        with MASTER_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {}


def _save_master_data(
    data: Dict[str, Any],
) -> None:
    """
    Save master password data safely.
    """

    temp_file = MASTER_FILE.with_suffix(".tmp")

    with temp_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    temp_file.replace(MASTER_FILE)


def _create_password_hash(
    password: str,
) -> tuple[str, str]:
    """
    Create salt and password hash.
    """

    salt = secrets.token_bytes(
        SALT_LENGTH
    )

    password_hash = _hash_password(
        password,
        salt,
    )

    return salt.hex(), password_hash


def _create_answer_hash(
    answer: str,
) -> tuple[str, str]:
    """
    Hash security answer.
    """

    salt = secrets.token_bytes(
        SALT_LENGTH
    )

    answer_hash = _hash_password(
        answer.strip().lower(),
        salt,
    )

    return salt.hex(), answer_hash

# =====================================================
# PUBLIC FUNCTIONS
# Part 2 / 3
# =====================================================

def master_exists() -> bool:
    """
    Check whether a master password exists.
    """

    data = _load_master_data()

    return bool(

        data.get("hash")

        and data.get("salt")

    )


def set_master_password(
    password: str,
    security_question: str,
    security_answer: str,
) -> str:
    """
    Create or replace the master password.

    Returns
    -------
    str
        Generated Recovery Key.
    """

    if not password.strip():

        raise ValueError(
            "Master password cannot be empty."
        )

    if not security_question.strip():

        raise ValueError(
            "Security question is required."
        )

    if not security_answer.strip():

        raise ValueError(
            "Security answer is required."
        )

    password_salt, password_hash = (

        _create_password_hash(password)

    )

    answer_salt, answer_hash = (

        _create_answer_hash(
            security_answer
        )

    )

    recovery_key = generate_recovery_key()

    timestamp = _current_timestamp()

    data = {

        "salt": password_salt,

        "hash": password_hash,

        "recovery_key": recovery_key,

        "security_question": security_question,

        "security_answer_salt": answer_salt,

        "security_answer_hash": answer_hash,

        "created_at": timestamp,

        "last_changed": timestamp,

    }

    _save_master_data(data)

    return recovery_key


def verify_master_password(
    password: str,
) -> bool:
    """
    Verify master password.
    """

    data = _load_master_data()

    if not data:

        return False

    try:

        salt = bytes.fromhex(
            data["salt"]
        )

        stored_hash = data["hash"]

    except KeyError:

        return False

    current_hash = _hash_password(

        password,

        salt,

    )

    return secrets.compare_digest(

        current_hash,

        stored_hash,

    )


def get_security_question() -> str:
    """
    Return stored security question.
    """

    data = _load_master_data()

    return data.get(

        "security_question",

        ""

    )


def verify_recovery(
    recovery_key: str,
    security_answer: str,
) -> bool:
    """
    Verify recovery credentials.
    """

    data = _load_master_data()

    if not data:

        return False

    try:

        stored_key = data["recovery_key"]

        answer_salt = bytes.fromhex(

            data["security_answer_salt"]

        )

        stored_answer_hash = data[
            "security_answer_hash"
        ]

    except KeyError:

        return False

    if not secrets.compare_digest(

        recovery_key.strip().upper(),

        stored_key.upper(),

    ):

        return False

    current_answer_hash = _hash_password(

        security_answer.strip().lower(),

        answer_salt,

    )

    return secrets.compare_digest(

        current_answer_hash,

        stored_answer_hash,

    )


def get_recovery_key() -> str:
    """
    Return recovery key.
    Useful immediately after setup.
    """

    data = _load_master_data()

    return data.get(

        "recovery_key",

        ""

    )


# =====================================================
# PUBLIC FUNCTIONS
# Part 3 / 3
# =====================================================

def reset_master_password(
    new_password: str,
) -> bool:
    """
    Reset master password after successful
    recovery verification.

    Recovery information remains unchanged.
    """

    if not new_password.strip():

        raise ValueError(
            "Master password cannot be empty."
        )

    data = _load_master_data()

    if not data:

        return False

    password_salt, password_hash = (

        _create_password_hash(
            new_password
        )

    )

    data["salt"] = password_salt

    data["hash"] = password_hash

    data["last_changed"] = (

        _current_timestamp()

    )

    _save_master_data(data)

    return True


def change_master_password(
    old_password: str,
    new_password: str,
) -> bool:
    """
    Change master password.
    """

    if not verify_master_password(
        old_password
    ):

        return False

    return reset_master_password(
        new_password
    )


def change_security_question(
    security_question: str,
    security_answer: str,
) -> bool:
    """
    Change security question and answer.
    """

    if not security_question.strip():

        return False

    if not security_answer.strip():

        return False

    data = _load_master_data()

    if not data:

        return False

    answer_salt, answer_hash = (

        _create_answer_hash(
            security_answer
        )

    )

    data["security_question"] = (

        security_question

    )

    data["security_answer_salt"] = (

        answer_salt

    )

    data["security_answer_hash"] = (

        answer_hash

    )

    data["last_changed"] = (

        _current_timestamp()

    )

    _save_master_data(data)

    return True


def regenerate_recovery_key() -> str:
    """
    Generate a new recovery key.
    """

    data = _load_master_data()

    if not data:

        return ""

    recovery_key = (

        generate_recovery_key()

    )

    data["recovery_key"] = (

        recovery_key

    )

    data["last_changed"] = (

        _current_timestamp()

    )

    _save_master_data(data)

    return recovery_key


def delete_master_password() -> bool:
    """
    Delete master password file.
    """

    try:

        if MASTER_FILE.exists():

            MASTER_FILE.unlink()

        return True

    except OSError:

        return False


def get_master_info() -> Dict[str, Any]:
    """
    Return master password metadata.
    """

    data = _load_master_data()

    return {

        "exists": master_exists(),

        "algorithm": HASH_ALGORITHM,

        "iterations": ITERATIONS,

        "salt_length": SALT_LENGTH,

        "has_recovery_key": bool(

            data.get("recovery_key")

        ),

        "has_security_question": bool(

            data.get(
                "security_question"
            )

        ),

        "created_at": data.get(

            "created_at"

        ),

        "last_changed": data.get(

            "last_changed"

        ),

        "storage": str(

            MASTER_FILE

        ),

    }


# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Master Password Manager")

    print("=" * 60)

    print("\nCreating Master Password...")

    recovery_key = set_master_password(

        password="Mohd@123",

        security_question=(
            "What is your first school?"
        ),

        security_answer="ABC School",

    )

    print(
        "Recovery Key :",
        recovery_key,
    )

    print(
        "Correct Password :",
        verify_master_password(
            "Mohd@123"
        ),
    )

    print(
        "Wrong Password :",
        verify_master_password(
            "Wrong@123"
        ),
    )

    print(
        "\nSecurity Question :",
        get_security_question(),
    )

    print(
        "Recovery Verification :",
        verify_recovery(
            recovery_key,
            "ABC School",
        ),
    )

    print(
        "\nChanging Password..."
    )

    change_master_password(

        "Mohd@123",

        "NewPassword@123",

    )

    print(
        "Verification :",
        verify_master_password(
            "NewPassword@123"
        ),
    )

    print(
        "\nReset Password..."
    )

    reset_master_password(

        "Reset@123"

    )

    print(
        "Reset Verification :",
        verify_master_password(
            "Reset@123"
        ),
    )

    print("\nMaster Information")

    print(
        get_master_info()
    )