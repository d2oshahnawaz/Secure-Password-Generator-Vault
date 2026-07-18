# =====================================================
# MASTER PASSWORD MANAGER
# Version 5.1 Professional
# Part 1/4
# =====================================================

from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Final
from typing import Optional

# =====================================================
# PATHS
# =====================================================

BASE_DIR: Final[Path] = Path(__file__).resolve().parent

MASTER_FILE: Final[Path] = BASE_DIR / "master.json"

BACKUP_FILE: Final[Path] = BASE_DIR / "master_backup.json"

AUDIT_FILE: Final[Path] = BASE_DIR / "master_audit.json"

# =====================================================
# CRYPTOGRAPHY
# =====================================================

HASH_ALGORITHM: Final[str] = "sha256"

ITERATIONS: Final[int] = 250_000

SALT_LENGTH: Final[int] = 16

# =====================================================
# ACCOUNT SECURITY
# =====================================================

MAX_FAILED_ATTEMPTS: Final[int] = 5

LOCKOUT_MINUTES: Final[int] = 15

PASSWORD_EXPIRY_DAYS: Final[int] = 180

PASSWORD_HISTORY_LIMIT: Final[int] = 5

RECOVERY_KEY_GROUPS: Final[int] = 4

RECOVERY_KEY_LENGTH: Final[int] = 4

# =====================================================
# DEFAULT SECURITY QUESTIONS
# =====================================================

DEFAULT_SECURITY_QUESTIONS: Final[list[str]] = [

    "What is your first school?",

    "What is your mother's first name?",

    "What is your favorite teacher's name?",

    "What is your childhood nickname?",

    "What city were you born in?",

]

# =====================================================
# PASSWORD HASHING
# =====================================================

def _hash_password(
    password: str,
    salt: bytes,
) -> str:
    """
    Generate PBKDF2 hash.
    """

    return hashlib.pbkdf2_hmac(

        HASH_ALGORITHM,

        password.encode("utf-8"),

        salt,

        ITERATIONS,

    ).hex()

# =====================================================
# TIMESTAMP
# =====================================================

def _timestamp() -> str:
    """
    Return ISO timestamp.
    """

    return datetime.now().isoformat(
        timespec="seconds"
    )

# =====================================================
# RECOVERY KEY
# =====================================================

def generate_recovery_key() -> str:
    """
    Example:
    A1B2-C3D4-E5F6-G7H8
    """

    groups: list[str] = []

    for _ in range(
        RECOVERY_KEY_GROUPS
    ):

        groups.append(

            secrets.token_hex(
                RECOVERY_KEY_LENGTH // 2
            ).upper()

        )

    return "-".join(groups)

# =====================================================
# JSON HELPERS
# =====================================================

def _load_json(
    path: Path,
) -> Dict[str, Any]:
    """
    Load JSON safely.
    """

    if not path.exists():

        return {}

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except (

        json.JSONDecodeError,

        OSError,

    ):

        return {}

# -----------------------------------------------------

def _save_json(
    path: Path,
    data: Dict[str, Any],
) -> None:
    """
    Save JSON atomically.
    """

    temp = path.with_suffix(".tmp")

    with temp.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(

            data,

            file,

            indent=4,

            ensure_ascii=False,

        )

    temp.replace(path)

# =====================================================
# MASTER FILE
# =====================================================

def _load_master_data() -> Dict[str, Any]:
    """
    Load master database.
    """

    return _load_json(
        MASTER_FILE
    )

# -----------------------------------------------------

def _save_master_data(
    data: Dict[str, Any],
) -> None:
    """
    Save master database.
    """

    _save_json(
        MASTER_FILE,
        data,
    )

# =====================================================
# AUDIT LOG
# =====================================================

def _audit(
    action: str,
    status: str,
    details: str = "",
) -> None:
    """
    Append audit entry.
    """

    audit = _load_json(
        AUDIT_FILE
    )

    logs = audit.get(
        "logs",
        [],
    )

    logs.append({

        "timestamp":
            _timestamp(),

        "action":
            action,

        "status":
            status,

        "details":
            details,

    })

    audit["logs"] = logs[-500:]

    _save_json(
        AUDIT_FILE,
        audit,
    )

# =====================================================
# PASSWORD HASH
# =====================================================

def _create_password_hash(
    password: str,
) -> tuple[str, str]:

    salt = secrets.token_bytes(
        SALT_LENGTH
    )

    password_hash = _hash_password(

        password,

        salt,

    )

    return (

        salt.hex(),

        password_hash,

    )

# =====================================================
# SECURITY ANSWER
# =====================================================

def _create_answer_hash(
    answer: str,
) -> tuple[str, str]:

    salt = secrets.token_bytes(
        SALT_LENGTH
    )

    answer_hash = _hash_password(

        answer.strip().lower(),

        salt,

    )

    return (

        salt.hex(),

        answer_hash,

    )

# =====================================================
# LOCKOUT HELPERS
# =====================================================

def _locked_until() -> Optional[datetime]:
    """
    Return lockout expiry time.
    """

    data = _load_master_data()

    value = data.get(
        "locked_until"
    )

    if not value:

        return None

    try:

        return datetime.fromisoformat(
            value
        )

    except ValueError:

        return None

# -----------------------------------------------------

def is_locked() -> bool:
    """
    Check whether account is locked.
    """

    locked = _locked_until()

    if locked is None:

        return False

    return datetime.now() < locked

# -----------------------------------------------------

def remaining_lock_time() -> int:
    """
    Remaining lock time (seconds).
    """

    locked = _locked_until()

    if locked is None:

        return 0

    seconds = int(

        (locked - datetime.now())

        .total_seconds()

    )

    return max(
        seconds,
        0,
    )
    
    # =====================================================
# PUBLIC FUNCTIONS
# Version 5.1 Professional
# Part 2A-1
# =====================================================

def master_exists() -> bool:
    """
    Check whether a master password has been configured.
    """

    data = _load_master_data()

    return bool(
        data.get("salt")
        and data.get("hash")
    )


# =====================================================

def _initialize_master_data() -> Dict[str, Any]:
    """
    Create the default master data structure.
    """

    return {

        "salt": "",

        "hash": "",

        "password_history": [],

        "failed_attempts": 0,

        "locked_until": None,

        "created_at": None,

        "last_changed": None,

        "last_login": None,

        "last_failed_login": None,

        "password_hint": "",

        "recovery_key": "",

        "security_question": "",

        "security_answer_salt": "",

        "security_answer_hash": "",

    }


# =====================================================

def _validate_master_password(
    password: str,
) -> None:
    """
    Validate master password.
    """

    password = password.strip()

    if not password:

        raise ValueError(
            "Master password cannot be empty."
        )

    if len(password) < 8:

        raise ValueError(
            "Master password must contain at least 8 characters."
        )


# =====================================================

def _validate_security_data(
    question: str,
    answer: str,
) -> None:
    """
    Validate recovery information.
    """

    if not question.strip():

        raise ValueError(
            "Security question is required."
        )

    if not answer.strip():

        raise ValueError(
            "Security answer is required."
        )


# =====================================================

def set_master_password(
    password: str,
    security_question: str,
    security_answer: str,
    password_hint: str = "",
) -> str:
    """
    Create or replace the master password.

    Returns
    -------
    str
        Generated recovery key.
    """

    _validate_master_password(
        password
    )

    _validate_security_data(

        security_question,

        security_answer,

    )

    password_salt, password_hash = (

        _create_password_hash(
            password
        )

    )

    answer_salt, answer_hash = (

        _create_answer_hash(
            security_answer
        )

    )

    recovery_key = (
        generate_recovery_key()
    )

    timestamp = _timestamp()

    data = _initialize_master_data()

    data.update({

        "salt":
            password_salt,

        "hash":
            password_hash,

        "password_history": [

            password_hash

        ],

        "created_at":
            timestamp,

        "last_changed":
            timestamp,

        "recovery_key":
            recovery_key,

        "security_question":
            security_question,

        "security_answer_salt":
            answer_salt,

        "security_answer_hash":
            answer_hash,

        "password_hint":
            password_hint.strip(),

    })

    _save_master_data(
        data
    )

    _audit(

        action="CREATE_MASTER",

        status="SUCCESS",

        details="Master password created.",

    )

    return recovery_key


# =====================================================

def get_security_question() -> str:
    """
    Return stored security question.
    """

    data = _load_master_data()

    return data.get(
        "security_question",
        "",
    )


# =====================================================

def get_password_hint() -> str:
    """
    Return password hint.
    """

    data = _load_master_data()

    return data.get(
        "password_hint",
        "",
    )


# =====================================================

def get_recovery_key() -> str:
    """
    Return recovery key.
    """

    data = _load_master_data()

    return data.get(
        "recovery_key",
        "",
    )
    
    # =====================================================
# PUBLIC FUNCTIONS
# Version 5.1 Professional
# Part 2A-2
# =====================================================

def _reset_failed_attempts() -> None:
    """
    Reset failed login attempts.
    """

    data = _load_master_data()

    if not data:
        return

    data["failed_attempts"] = 0
    data["locked_until"] = None

    _save_master_data(data)


# -----------------------------------------------------

def _register_failed_attempt() -> None:
    """
    Register a failed login attempt.
    """

    data = _load_master_data()

    if not data:
        return

    attempts = data.get(
        "failed_attempts",
        0,
    ) + 1

    data["failed_attempts"] = attempts

    data["last_failed_login"] = _timestamp()

    if attempts >= MAX_FAILED_ATTEMPTS:

        lock_until = (
            datetime.now()
            + timedelta(
                minutes=LOCKOUT_MINUTES
            )
        )

        data["locked_until"] = (
            lock_until.isoformat(
                timespec="seconds"
            )
        )

        _audit(
            action="ACCOUNT_LOCKED",
            status="FAILED",
            details=(
                f"Exceeded {MAX_FAILED_ATTEMPTS} failed attempts."
            ),
        )

    _save_master_data(data)


# -----------------------------------------------------

def failed_attempts() -> int:
    """
    Return failed login count.
    """

    data = _load_master_data()

    return int(
        data.get(
            "failed_attempts",
            0,
        )
    )


# -----------------------------------------------------

def last_login() -> Optional[str]:
    """
    Return last successful login timestamp.
    """

    data = _load_master_data()

    return data.get(
        "last_login"
    )


# -----------------------------------------------------

def last_failed_login() -> Optional[str]:
    """
    Return last failed login timestamp.
    """

    data = _load_master_data()

    return data.get(
        "last_failed_login"
    )


# -----------------------------------------------------

def verify_master_password(
    password: str,
) -> bool:
    """
    Verify master password.

    Automatically tracks:

    • Failed attempts
    • Last login
    • Account lock
    • Audit logs
    """

    if is_locked():

        _audit(
            action="LOGIN",
            status="LOCKED",
            details="Attempt while account locked.",
        )

        return False

    data = _load_master_data()

    if not data:

        return False

    try:

        salt = bytes.fromhex(
            data["salt"]
        )

        stored_hash = data["hash"]

    except (
        KeyError,
        ValueError,
    ):

        return False

    current_hash = _hash_password(
        password,
        salt,
    )

    verified = secrets.compare_digest(
        current_hash,
        stored_hash,
    )

    if verified:

        data["last_login"] = (
            _timestamp()
        )

        data["failed_attempts"] = 0

        data["locked_until"] = None

        _save_master_data(
            data
        )

        _audit(
            action="LOGIN",
            status="SUCCESS",
            details="Master password verified.",
        )

        return True

    _register_failed_attempt()

    _audit(
        action="LOGIN",
        status="FAILED",
        details="Invalid master password.",
    )

    return False


# -----------------------------------------------------

def unlock_account() -> bool:
    """
    Remove account lock manually.
    """

    data = _load_master_data()

    if not data:
        return False

    data["failed_attempts"] = 0

    data["locked_until"] = None

    _save_master_data(
        data
    )

    _audit(
        action="ACCOUNT_UNLOCK",
        status="SUCCESS",
        details="Manual unlock.",
    )

    return True


# -----------------------------------------------------

def login_statistics() -> Dict[str, Any]:
    """
    Return login-related statistics.
    """

    data = _load_master_data()

    return {

        "failed_attempts":
            data.get(
                "failed_attempts",
                0,
            ),

        "locked":
            is_locked(),

        "remaining_lock_seconds":
            remaining_lock_time(),

        "last_login":
            data.get(
                "last_login"
            ),

        "last_failed_login":
            data.get(
                "last_failed_login"
            ),

    }
    
    # =====================================================
# PUBLIC FUNCTIONS
# Version 5.1 Professional
# Part 2B
# =====================================================

def password_age() -> int:
    """
    Return password age in days.
    """

    data = _load_master_data()

    changed = data.get(
        "last_changed"
    )

    if not changed:
        return 0

    try:

        changed_date = datetime.fromisoformat(
            changed
        )

    except ValueError:

        return 0

    return (
        datetime.now() - changed_date
    ).days


# -----------------------------------------------------

def password_expired() -> bool:
    """
    Check whether password has expired.
    """

    return (
        password_age()
        >= PASSWORD_EXPIRY_DAYS
    )


# -----------------------------------------------------

def _password_used_before(
    password: str,
) -> bool:
    """
    Check whether password exists
    in password history.
    """

    data = _load_master_data()

    if not data:
        return False

    history = data.get(
        "password_history",
        [],
    )

    for item in history:

        try:

            salt = bytes.fromhex(
                item["salt"]
            )

            old_hash = item["hash"]

        except (
            KeyError,
            ValueError,
        ):

            continue

        current_hash = _hash_password(
            password,
            salt,
        )

        if secrets.compare_digest(
            current_hash,
            old_hash,
        ):
            return True

    return False


# -----------------------------------------------------

def _append_password_history(
    salt: str,
    password_hash: str,
) -> None:
    """
    Save password into history.
    """

    data = _load_master_data()

    history = data.get(
        "password_history",
        [],
    )

    history.append({

        "salt":
            salt,

        "hash":
            password_hash,

        "changed":
            _timestamp(),

    })

    history = history[
        -PASSWORD_HISTORY_LIMIT:
    ]

    data["password_history"] = history

    _save_master_data(data)


# -----------------------------------------------------

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

    _validate_master_password(
        new_password
    )

    if _password_used_before(
        new_password
    ):
        raise ValueError(
            "Password was used recently."
        )

    data = _load_master_data()

    salt, password_hash = (
        _create_password_hash(
            new_password
        )
    )

    data["salt"] = salt

    data["hash"] = password_hash

    data["last_changed"] = (
        _timestamp()
    )

    _save_master_data(
        data
    )

    _append_password_history(
        salt,
        password_hash,
    )

    _audit(
        action="CHANGE_PASSWORD",
        status="SUCCESS",
        details="Master password changed.",
    )

    return True


# -----------------------------------------------------

def reset_master_password(
    new_password: str,
) -> bool:
    """
    Reset master password after
    successful recovery.
    """

    _validate_master_password(
        new_password
    )

    if _password_used_before(
        new_password
    ):
        raise ValueError(
            "Password was used recently."
        )

    data = _load_master_data()

    if not data:
        return False

    salt, password_hash = (
        _create_password_hash(
            new_password
        )
    )

    data["salt"] = salt

    data["hash"] = password_hash

    data["last_changed"] = (
        _timestamp()
    )

    data["failed_attempts"] = 0

    data["locked_until"] = None

    _save_master_data(
        data
    )

    _append_password_history(
        salt,
        password_hash,
    )

    _audit(
        action="RESET_PASSWORD",
        status="SUCCESS",
        details="Password reset completed.",
    )

    return True


# -----------------------------------------------------

def update_password_hint(
    hint: str,
) -> bool:
    """
    Update password hint.
    """

    data = _load_master_data()

    if not data:
        return False

    data["password_hint"] = (
        hint.strip()
    )

    _save_master_data(
        data
    )

    _audit(
        action="UPDATE_HINT",
        status="SUCCESS",
        details="Password hint updated.",
    )

    return True


# -----------------------------------------------------

def password_history() -> list[dict]:
    """
    Return password history.
    """

    data = _load_master_data()

    return data.get(
        "password_history",
        [],
    )


# -----------------------------------------------------

def password_statistics() -> Dict[str, Any]:
    """
    Return password-related statistics.
    """

    return {

        "age_days":
            password_age(),

        "expired":
            password_expired(),

        "history_size":
            len(
                password_history()
            ),

        "history_limit":
            PASSWORD_HISTORY_LIMIT,

        "last_changed":
            _load_master_data().get(
                "last_changed"
            ),

    }
    
    # =====================================================
# PUBLIC FUNCTIONS
# Version 5.1 Professional
# Part 3A
# Recovery & Security Management
# =====================================================

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

        stored_hash = data[
            "security_answer_hash"
        ]

    except (
        KeyError,
        ValueError,
    ):

        return False

    if not secrets.compare_digest(

        recovery_key.strip().upper(),

        stored_key.upper(),

    ):

        _audit(
            action="RECOVERY",
            status="FAILED",
            details="Invalid recovery key.",
        )

        return False

    current_hash = _hash_password(

        security_answer.strip().lower(),

        answer_salt,

    )

    verified = secrets.compare_digest(

        current_hash,

        stored_hash,

    )

    _audit(

        action="RECOVERY",

        status="SUCCESS" if verified else "FAILED",

        details=(
            "Recovery verification."
        ),

    )

    return verified


# -----------------------------------------------------

def change_security_question(
    security_question: str,
    security_answer: str,
) -> bool:
    """
    Update security question and answer.
    """

    _validate_security_data(

        security_question,

        security_answer,

    )

    data = _load_master_data()

    if not data:
        return False

    salt, answer_hash = (

        _create_answer_hash(

            security_answer

        )

    )

    data["security_question"] = (

        security_question

    )

    data["security_answer_salt"] = (

        salt

    )

    data["security_answer_hash"] = (

        answer_hash

    )

    data["last_changed"] = (

        _timestamp()

    )

    _save_master_data(
        data
    )

    _audit(

        action="UPDATE_SECURITY",

        status="SUCCESS",

        details="Security question updated.",

    )

    return True


# -----------------------------------------------------

def regenerate_recovery_key() -> str:
    """
    Generate a new recovery key.
    """

    data = _load_master_data()

    if not data:
        return ""

    old_key = data.get(
        "recovery_key",
        "",
    )

    new_key = generate_recovery_key()

    history = data.get(
        "recovery_history",
        [],
    )

    if old_key:

        history.append({

            "key":
                old_key,

            "changed":
                _timestamp(),

        })

    history = history[-10:]

    data["recovery_history"] = (
        history
    )

    data["recovery_key"] = (
        new_key
    )

    data["last_changed"] = (
        _timestamp()
    )

    _save_master_data(
        data
    )

    _audit(

        action="ROTATE_RECOVERY_KEY",

        status="SUCCESS",

        details="Recovery key regenerated.",

    )

    return new_key


# -----------------------------------------------------

def recovery_history() -> list[dict]:
    """
    Return previous recovery keys.
    """

    data = _load_master_data()

    return data.get(
        "recovery_history",
        [],
    )


# -----------------------------------------------------

def recovery_statistics() -> Dict[str, Any]:
    """
    Recovery information.
    """

    data = _load_master_data()

    return {

        "has_recovery_key":
            bool(
                data.get(
                    "recovery_key"
                )
            ),

        "security_question":
            data.get(
                "security_question",
                "",
            ),

        "recovery_rotations":
            len(
                data.get(
                    "recovery_history",
                    [],
                )
            ),

        "last_changed":
            data.get(
                "last_changed"
            ),

    }


# -----------------------------------------------------

def available_security_questions() -> list[str]:
    """
    Return default security questions.
    """

    return DEFAULT_SECURITY_QUESTIONS.copy()


# -----------------------------------------------------

def recovery_info() -> Dict[str, Any]:
    """
    Return recovery metadata.
    """

    data = _load_master_data()

    return {

        "question":
            data.get(
                "security_question",
                "",
            ),

        "has_answer":
            bool(
                data.get(
                    "security_answer_hash"
                )
            ),

        "has_key":
            bool(
                data.get(
                    "recovery_key"
                )
            ),

        "history":
            len(
                data.get(
                    "recovery_history",
                    [],
                )
            ),

    }
    
    # =====================================================
# PUBLIC FUNCTIONS
# Version 5.1 Professional
# Part 3B
# Backup • Restore • Diagnostics
# =====================================================

import shutil


# =====================================================
# BACKUP
# =====================================================

def backup_master() -> bool:
    """
    Create a backup of master.json.
    """

    if not MASTER_FILE.exists():
        return False

    try:

        shutil.copy2(
            MASTER_FILE,
            BACKUP_FILE,
        )

        _audit(
            action="BACKUP",
            status="SUCCESS",
            details="Master database backed up.",
        )

        return True

    except OSError:

        _audit(
            action="BACKUP",
            status="FAILED",
            details="Backup failed.",
        )

        return False


# =====================================================
# RESTORE
# =====================================================

def restore_master() -> bool:
    """
    Restore master database from backup.
    """

    if not BACKUP_FILE.exists():
        return False

    try:

        shutil.copy2(
            BACKUP_FILE,
            MASTER_FILE,
        )

        _audit(
            action="RESTORE",
            status="SUCCESS",
            details="Master database restored.",
        )

        return True

    except OSError:

        _audit(
            action="RESTORE",
            status="FAILED",
            details="Restore failed.",
        )

        return False


# =====================================================
# EXPORT METADATA
# =====================================================

def export_master_metadata() -> Dict[str, Any]:
    """
    Export safe metadata only.
    """

    data = _load_master_data()

    return {

        "algorithm":
            HASH_ALGORITHM,

        "iterations":
            ITERATIONS,

        "created_at":
            data.get(
                "created_at"
            ),

        "last_changed":
            data.get(
                "last_changed"
            ),

        "password_age_days":
            password_age(),

        "password_expired":
            password_expired(),

        "failed_attempts":
            failed_attempts(),

        "locked":
            is_locked(),

        "recovery_enabled":
            bool(
                data.get(
                    "recovery_key"
                )
            ),

    }


# =====================================================
# DELETE MASTER
# =====================================================

def delete_master_password() -> bool:
    """
    Delete all master files.
    """

    success = True

    for file in (

        MASTER_FILE,

        BACKUP_FILE,

    ):

        try:

            if file.exists():
                file.unlink()

        except OSError:

            success = False

    _audit(

        action="DELETE_MASTER",

        status="SUCCESS" if success else "FAILED",

        details="Master database deleted.",

    )

    return success


# =====================================================
# HEALTH REPORT
# =====================================================

def master_health() -> Dict[str, Any]:
    """
    Return complete health report.
    """

    return {

        "master_exists":
            master_exists(),

        "locked":
            is_locked(),

        "failed_attempts":
            failed_attempts(),

        "password_age":
            password_age(),

        "password_expired":
            password_expired(),

        "history_entries":
            len(
                password_history()
            ),

        "recovery_history":
            len(
                recovery_history()
            ),

        "audit_available":
            AUDIT_FILE.exists(),

        "backup_available":
            BACKUP_FILE.exists(),

    }


# =====================================================
# MASTER INFO
# =====================================================

def get_master_info() -> Dict[str, Any]:
    """
    Return master configuration.
    """

    data = _load_master_data()

    return {

        "version":
            "5.1 Professional",

        "algorithm":
            HASH_ALGORITHM,

        "iterations":
            ITERATIONS,

        "salt_length":
            SALT_LENGTH,

        "created_at":
            data.get(
                "created_at"
            ),

        "last_changed":
            data.get(
                "last_changed"
            ),

        "last_login":
            data.get(
                "last_login"
            ),

        "storage":
            str(MASTER_FILE),

        "backup":
            str(BACKUP_FILE),

        "audit":
            str(AUDIT_FILE),

    }


# =====================================================
# DIAGNOSTICS
# =====================================================

def diagnostics() -> Dict[str, Any]:
    """
    Module diagnostics.
    """

    return {

        "module":
            "master",

        "version":
            "5.1 Professional",

        "healthy":
            master_exists(),

        "locked":
            is_locked(),

        "expired":
            password_expired(),

        "backup":
            BACKUP_FILE.exists(),

        "audit":
            AUDIT_FILE.exists(),

    }


# =====================================================
# SELF TEST
# =====================================================

def run_self_test() -> bool:
    """
    Execute basic module tests.
    """

    assert isinstance(
        master_exists(),
        bool,
    )

    assert isinstance(
        diagnostics(),
        dict,
    )

    assert isinstance(
        export_master_metadata(),
        dict,
    )

    assert isinstance(
        master_health(),
        dict,
    )

    assert isinstance(
        get_master_info(),
        dict,
    )

    return True


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Master Password Manager")
    print("Version 5.1 Professional")
    print("=" * 60)

    print()

    print("Module Information")

    print(get_master_info())

    print()

    print("Health")

    print(master_health())

    print()

    print("Diagnostics")

    print(diagnostics())

    print()

    if run_self_test():

        print("✓ All tests passed successfully.")

    print("=" * 60)