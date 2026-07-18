# =====================================================
# DATABASE
# Version 5.1 Professional
# Part 1/5
# =====================================================

from __future__ import annotations

# =====================================================
# IMPORTS
# =====================================================

import shutil
import sqlite3
from pathlib import Path
from typing import Any
from typing import Final

# =====================================================
# MODULE INFORMATION
# =====================================================

MODULE_NAME: Final[str] = "database"

MODULE_VERSION: Final[str] = "5.1 Professional"

# =====================================================
# DATABASE PATH
# =====================================================

BASE_DIR: Final[Path] = Path(__file__).resolve().parent

DB_NAME: Final[str] = "password_history.db"

DB_PATH: Final[Path] = BASE_DIR / DB_NAME

BACKUP_DIR: Final[Path] = BASE_DIR / "backups"

BACKUP_DIR.mkdir(
    exist_ok=True
)

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False,
)

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# =====================================================
# PRAGMA SETTINGS
# =====================================================

cursor.execute(
    "PRAGMA foreign_keys = ON"
)

cursor.execute(
    "PRAGMA journal_mode = WAL"
)

cursor.execute(
    "PRAGMA synchronous = NORMAL"
)

cursor.execute(
    "PRAGMA temp_store = MEMORY"
)

cursor.execute(
    "PRAGMA cache_size = -10000"
)

conn.commit()

# =====================================================
# PASSWORD HISTORY TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS passwords(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        password TEXT NOT NULL,

        strength TEXT,

        entropy REAL,

        crack_time TEXT,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP

    )
"""
)

# =====================================================
# PASSWORD VAULT TABLE
# =====================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS vault(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        website TEXT NOT NULL,

        username TEXT NOT NULL,

        encrypted_password TEXT NOT NULL,

        category TEXT,

        tags TEXT,

        notes TEXT,

        favorite INTEGER DEFAULT 0,

        expiry_date TEXT,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP

    )
"""
)

conn.commit()

# =====================================================
# DATABASE MIGRATION
# =====================================================

def add_column_if_not_exists(
    table_name: str,
    column_name: str,
    definition: str,
) -> None:
    """
    Add a column only if it
    does not already exist.
    """

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [

        row[1]

        for row in cursor.fetchall()

    ]

    if column_name not in columns:

        cursor.execute(
            f"""
            ALTER TABLE {table_name}

            ADD COLUMN {column_name}

            {definition}
            """
        )

        conn.commit()


# =====================================================
# SAFE MIGRATIONS
# =====================================================

MIGRATIONS: Final = [

    (
        "vault",
        "tags",
        "TEXT",
    ),

    (
        "vault",
        "favorite",
        "INTEGER DEFAULT 0",
    ),

    (
        "vault",
        "expiry_date",
        "TEXT",
    ),

    (
        "vault",
        "updated_at",
        "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    ),

]

for table, column, definition in MIGRATIONS:

    add_column_if_not_exists(
        table,
        column,
        definition,
    )

conn.commit()

# =====================================================
# DATABASE HELPERS
# =====================================================

def execute(
    query: str,
    parameters: tuple[Any, ...] = (),
) -> sqlite3.Cursor:
    """
    Execute INSERT/UPDATE/DELETE query.
    """

    cursor.execute(
        query,
        parameters,
    )

    conn.commit()

    return cursor


# -----------------------------------------------------

def fetchall(
    query: str,
    parameters: tuple[Any, ...] = (),
) -> list[sqlite3.Row]:
    """
    Execute SELECT query.
    """

    cursor.execute(
        query,
        parameters,
    )

    return cursor.fetchall()


# -----------------------------------------------------

def fetchone(
    query: str,
    parameters: tuple[Any, ...] = (),
) -> sqlite3.Row | None:
    """
    Execute SELECT query
    returning one row.
    """

    cursor.execute(
        query,
        parameters,
    )

    return cursor.fetchone()


# =====================================================
# DATABASE UTILITIES
# =====================================================

def database_exists() -> bool:
    """
    Check whether database exists.
    """

    return DB_PATH.exists()


# -----------------------------------------------------

def database_size() -> int:
    """
    Database size in bytes.
    """

    if not database_exists():

        return 0

    return DB_PATH.stat().st_size


# -----------------------------------------------------

def optimize_database() -> None:
    """
    Optimize SQLite database.
    """

    cursor.execute(
        "VACUUM"
    )

    cursor.execute(
        "ANALYZE"
    )

    conn.commit()


# -----------------------------------------------------

def close_database() -> None:
    """
    Close SQLite connection.
    """

    conn.commit()

    conn.close()


# =====================================================
# MODULE INFORMATION
# =====================================================

def module_info() -> dict[str, Any]:
    """
    Database module metadata.
    """

    return {

        "module":
            MODULE_NAME,

        "version":
            MODULE_VERSION,

        "database":
            str(DB_PATH),

        "database_exists":
            database_exists(),

        "database_size":
            database_size(),

        "wal_mode":
            True,

        "cloud_ready":
            True,

    }
    
    # =====================================================
# PASSWORD HISTORY API
# Version 5.1 Professional
# Part 2/5
# =====================================================

# =====================================================
# SAVE PASSWORD
# =====================================================

def save_password(
    password: str,
    strength: str,
    entropy: float,
    crack_time: str,
) -> int:
    """
    Save generated password into history.

    Returns:
        Inserted row ID.
    """

    execute(
        """
        INSERT INTO passwords(

            password,

            strength,

            entropy,

            crack_time

        )

        VALUES(?,?,?,?)

        """,
        (
            password,
            strength,
            entropy,
            crack_time,
        ),
    )

    return cursor.lastrowid


# =====================================================
# GET HISTORY
# =====================================================

def get_history() -> list[sqlite3.Row]:
    """
    Return complete password history.
    """

    return fetchall(
        """
        SELECT *

        FROM passwords

        ORDER BY created_at DESC
        """
    )


# =====================================================
# GET RECENT HISTORY
# =====================================================

def get_recent_history(
    limit: int = 10,
) -> list[sqlite3.Row]:
    """
    Return recent password history.
    """

    return fetchall(
        """
        SELECT *

        FROM passwords

        ORDER BY created_at DESC

        LIMIT ?
        """,
        (limit,),
    )


# =====================================================
# SEARCH HISTORY
# =====================================================

def search_history(
    keyword: str,
) -> list[sqlite3.Row]:
    """
    Search password history.
    """

    keyword = keyword.strip()

    if not keyword:

        return get_history()

    value = f"%{keyword}%"

    return fetchall(
        """
        SELECT *

        FROM passwords

        WHERE

            password LIKE ?

            OR strength LIKE ?

            OR crack_time LIKE ?

        ORDER BY created_at DESC
        """,
        (
            value,
            value,
            value,
        ),
    )


# =====================================================
# DELETE HISTORY RECORD
# =====================================================

def delete_history(
    history_id: int,
) -> bool:
    """
    Delete a history record.
    """

    execute(
        """
        DELETE FROM passwords

        WHERE id=?
        """,
        (history_id,),
    )

    return cursor.rowcount > 0


# =====================================================
# CLEAR HISTORY
# =====================================================

def clear_history() -> None:
    """
    Remove all history records.
    """

    execute(
        """
        DELETE FROM passwords
        """
    )


# =====================================================
# HISTORY COUNT
# =====================================================

def history_count() -> int:
    """
    Total generated passwords.
    """

    row = fetchone(
        """
        SELECT COUNT(*)

        FROM passwords
        """
    )

    return int(row[0])


# =====================================================
# HISTORY STATISTICS
# =====================================================

def history_statistics() -> dict[str, Any]:
    """
    Return history statistics.
    """

    row = fetchone(
        """
        SELECT

            COUNT(*) AS total,

            AVG(entropy) AS avg_entropy,

            MIN(entropy) AS min_entropy,

            MAX(entropy) AS max_entropy

        FROM passwords
        """
    )

    return {

        "total":
            int(row["total"] or 0),

        "average_entropy":
            round(
                row["avg_entropy"] or 0,
                2,
            ),

        "minimum_entropy":
            round(
                row["min_entropy"] or 0,
                2,
            ),

        "maximum_entropy":
            round(
                row["max_entropy"] or 0,
                2,
            ),

    }


# =====================================================
# PASSWORD STRENGTH COUNTS
# =====================================================

def strength_count() -> list[sqlite3.Row]:
    """
    Count passwords by strength.
    """

    return fetchall(
        """
        SELECT

            strength,

            COUNT(*) AS total

        FROM passwords

        GROUP BY strength

        ORDER BY total DESC
        """
    )


# =====================================================
# DELETE DUPLICATE HISTORY
# =====================================================

def remove_duplicate_history() -> int:
    """
    Remove duplicate passwords.

    Returns:
        Number of deleted rows.
    """

    before = history_count()

    execute(
        """
        DELETE FROM passwords

        WHERE id NOT IN(

            SELECT MIN(id)

            FROM passwords

            GROUP BY password

        )
        """
    )

    after = history_count()

    return before - after


# =====================================================
# HISTORY EXISTS
# =====================================================

def history_exists() -> bool:
    """
    Check if history contains data.
    """

    return history_count() > 0

# =====================================================
# PASSWORD VAULT API
# Version 5.1 Professional
# Part 3/5
# =====================================================

# =====================================================
# SAVE VAULT PASSWORD
# =====================================================

def save_vault(
    website: str,
    username: str,
    encrypted_password: str,
    category: str,
    tags: str,
    notes: str,
    favorite: int = 0,
    expiry_date: str | None = None,
) -> int:
    """
    Save password into vault.

    Returns:
        Inserted row ID.
    """

    execute(
        """
        INSERT INTO vault(

            website,

            username,

            encrypted_password,

            category,

            tags,

            notes,

            favorite,

            expiry_date

        )

        VALUES(?,?,?,?,?,?,?,?)

        """,
        (
            website,
            username,
            encrypted_password,
            category,
            tags,
            notes,
            favorite,
            expiry_date,
        ),
    )

    return cursor.lastrowid


# =====================================================
# GET VAULT
# =====================================================

def get_vault() -> list[sqlite3.Row]:
    """
    Return all vault entries.
    """

    return fetchall(
        """
        SELECT *

        FROM vault

        ORDER BY created_at DESC
        """
    )


# =====================================================
# GET PASSWORD
# =====================================================

def get_password(
    vault_id: int,
) -> sqlite3.Row | None:
    """
    Return a single vault entry.
    """

    return fetchone(
        """
        SELECT *

        FROM vault

        WHERE id=?
        """,
        (vault_id,),
    )


# =====================================================
# SEARCH VAULT
# =====================================================

def search_vault(
    keyword: str,
) -> list[sqlite3.Row]:
    """
    Search vault.
    """

    keyword = keyword.strip()

    if not keyword:

        return get_vault()

    value = f"%{keyword}%"

    return fetchall(
        """
        SELECT *

        FROM vault

        WHERE

            website LIKE ?

            OR username LIKE ?

            OR category LIKE ?

            OR tags LIKE ?

            OR notes LIKE ?

        ORDER BY created_at DESC
        """,
        (
            value,
            value,
            value,
            value,
            value,
        ),
    )


# =====================================================
# UPDATE PASSWORD
# =====================================================

def update_vault(
    vault_id: int,
    website: str,
    username: str,
    encrypted_password: str,
    category: str,
    tags: str,
    notes: str,
    favorite: int,
    expiry_date: str | None,
) -> bool:
    """
    Update vault password.
    """

    execute(
        """
        UPDATE vault

        SET

            website=?,

            username=?,

            encrypted_password=?,

            category=?,

            tags=?,

            notes=?,

            favorite=?,

            expiry_date=?,

            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

        """,
        (
            website,
            username,
            encrypted_password,
            category,
            tags,
            notes,
            favorite,
            expiry_date,
            vault_id,
        ),
    )

    return cursor.rowcount > 0


# =====================================================
# DELETE PASSWORD
# =====================================================

def delete_vault(
    vault_id: int,
) -> bool:
    """
    Delete vault password.
    """

    execute(
        """
        DELETE FROM vault

        WHERE id=?
        """,
        (vault_id,),
    )

    return cursor.rowcount > 0


# =====================================================
# CLEAR VAULT
# =====================================================

def clear_vault() -> None:
    """
    Delete all vault entries.
    """

    execute(
        """
        DELETE FROM vault
        """
    )


# =====================================================
# VAULT COUNT
# =====================================================

def vault_count() -> int:
    """
    Total stored passwords.
    """

    row = fetchone(
        """
        SELECT COUNT(*)

        FROM vault
        """
    )

    return int(row[0])


# =====================================================
# VAULT EXISTS
# =====================================================

def vault_exists() -> bool:
    """
    Check whether vault has data.
    """

    return vault_count() > 0


# =====================================================
# GET RECENT VAULT
# =====================================================

def get_recent_vault(
    limit: int = 10,
) -> list[sqlite3.Row]:
    """
    Return recent vault entries.
    """

    return fetchall(
        """
        SELECT *

        FROM vault

        ORDER BY created_at DESC

        LIMIT ?
        """,
        (limit,),
    )


# =====================================================
# DUPLICATE PASSWORDS
# =====================================================

def duplicate_passwords() -> list[sqlite3.Row]:
    """
    Find duplicate encrypted passwords.
    """

    return fetchall(
        """
        SELECT

            encrypted_password,

            COUNT(*) AS total

        FROM vault

        GROUP BY encrypted_password

        HAVING COUNT(*) > 1

        ORDER BY total DESC
        """
    )
    
    # =====================================================
# DATABASE ANALYTICS & UTILITIES
# Version 5.1 Professional
# Part 4/5
# =====================================================

from datetime import datetime

# =====================================================
# FAVORITES
# =====================================================

def get_favorites() -> list[sqlite3.Row]:
    """
    Return favorite passwords.
    """

    return fetchall(
        """
        SELECT *

        FROM vault

        WHERE favorite=1

        ORDER BY created_at DESC
        """
    )


# =====================================================
# TOGGLE FAVORITE
# =====================================================

def toggle_favorite(
    vault_id: int,
) -> bool:
    """
    Toggle favorite status.
    """

    execute(
        """
        UPDATE vault

        SET

            favorite = CASE

                WHEN favorite=1 THEN 0

                ELSE 1

            END,

            updated_at=CURRENT_TIMESTAMP

        WHERE id=?

        """,
        (vault_id,),
    )

    return cursor.rowcount > 0


# =====================================================
# FILTER CATEGORY
# =====================================================

def filter_category(
    category: str,
) -> list[sqlite3.Row]:
    """
    Filter passwords by category.
    """

    return fetchall(
        """
        SELECT *

        FROM vault

        WHERE category=?

        ORDER BY created_at DESC
        """,
        (category,),
    )


# =====================================================
# EXPIRED PASSWORDS
# =====================================================

def expired_passwords() -> list[sqlite3.Row]:
    """
    Return expired passwords.
    """

    return fetchall(
        """
        SELECT *

        FROM vault

        WHERE

            expiry_date IS NOT NULL

            AND date(expiry_date)
                <= date('now')

        ORDER BY expiry_date
        """
    )


# =====================================================
# FAVORITE COUNT
# =====================================================

def favorite_count() -> int:
    """
    Return favorite count.
    """

    row = fetchone(
        """
        SELECT COUNT(*)

        FROM vault

        WHERE favorite=1
        """
    )

    return int(row[0])


# =====================================================
# CATEGORY COUNT
# =====================================================

def category_count() -> list[sqlite3.Row]:
    """
    Category-wise statistics.
    """

    return fetchall(
        """
        SELECT

            category,

            COUNT(*) AS total

        FROM vault

        GROUP BY category

        ORDER BY total DESC
        """
    )


# =====================================================
# VAULT STATISTICS
# =====================================================

def vault_statistics() -> dict[str, Any]:
    """
    Overall vault statistics.
    """

    return {

        "total":
            vault_count(),

        "favorites":
            favorite_count(),

        "expired":
            len(
                expired_passwords()
            ),

        "duplicates":
            len(
                duplicate_passwords()
            ),

        "categories":
            len(
                category_count()
            ),

    }


# =====================================================
# RECENTLY UPDATED
# =====================================================

def recently_updated(
    limit: int = 10,
) -> list[sqlite3.Row]:
    """
    Recently updated passwords.
    """

    return fetchall(
        """
        SELECT *

        FROM vault

        ORDER BY updated_at DESC

        LIMIT ?
        """,
        (limit,),
    )


# =====================================================
# DATABASE BACKUP
# =====================================================

def backup_database() -> Path:
    """
    Create SQLite backup.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (

        BACKUP_DIR

        / f"password_history_{timestamp}.db"

    )

    shutil.copy2(
        DB_PATH,
        backup_file,
    )

    return backup_file


# =====================================================
# RESTORE DATABASE
# =====================================================

def restore_database(
    backup_file: Path,
) -> None:
    """
    Restore database from backup.
    """

    conn.commit()

    shutil.copy2(
        backup_file,
        DB_PATH,
    )


# =====================================================
# DATABASE HEALTH
# =====================================================

def database_health() -> dict[str, Any]:
    """
    Database health information.
    """

    return {

        "database_exists":
            database_exists(),

        "database_size":
            database_size(),

        "history_records":
            history_count(),

        "vault_records":
            vault_count(),

        "favorite_records":
            favorite_count(),

        "expired_records":
            len(
                expired_passwords()
            ),

    }


# =====================================================
# OPTIMIZE DATABASE
# =====================================================

def optimize() -> None:
    """
    Optimize SQLite database.
    """

    optimize_database()


# =====================================================
# BACKUP EXISTS
# =====================================================

def available_backups() -> list[Path]:
    """
    Return available backups.
    """

    return sorted(

        BACKUP_DIR.glob("*.db"),

        reverse=True,

    )
    
    # =====================================================
# DATABASE DIAGNOSTICS
# Version 5.1 Professional
# Part 5/5
# =====================================================

# =====================================================
# DATABASE DIAGNOSTICS
# =====================================================

def diagnostics() -> dict[str, Any]:
    """
    Return complete database diagnostics.
    """

    return {

        "module":
            MODULE_NAME,

        "version":
            MODULE_VERSION,

        "database_path":
            str(DB_PATH),

        "database_exists":
            database_exists(),

        "database_size":
            database_size(),

        "history_records":
            history_count(),

        "vault_records":
            vault_count(),

        "favorite_records":
            favorite_count(),

        "expired_records":
            len(
                expired_passwords()
            ),

        "duplicate_passwords":
            len(
                duplicate_passwords()
            ),

        "categories":
            len(
                category_count()
            ),

        "backups":
            len(
                available_backups()
            ),

        "wal_mode":
            True,

        "cloud_ready":
            True,

    }


# =====================================================
# DATABASE INTEGRITY
# =====================================================

def integrity_check() -> bool:
    """
    Run SQLite integrity check.
    """

    row = fetchone(
        "PRAGMA integrity_check"
    )

    if row is None:

        return False

    return row[0] == "ok"


# =====================================================
# TABLE INFORMATION
# =====================================================

def table_information() -> dict[str, int]:
    """
    Number of records in each table.
    """

    return {

        "passwords":
            history_count(),

        "vault":
            vault_count(),

    }


# =====================================================
# DATABASE INFORMATION
# =====================================================

def database_information() -> dict[str, Any]:
    """
    Public database information.
    """

    return {

        "module":
            MODULE_NAME,

        "version":
            MODULE_VERSION,

        "database":
            DB_NAME,

        "path":
            str(DB_PATH),

        "backup_directory":
            str(BACKUP_DIR),

        "database_size":
            database_size(),

        "history_records":
            history_count(),

        "vault_records":
            vault_count(),

    }


# =====================================================
# CLEANUP
# =====================================================

def cleanup() -> None:
    """
    Commit pending transactions.
    """

    conn.commit()


# =====================================================
# CLOSE
# =====================================================

def shutdown() -> None:
    """
    Close database safely.
    """

    cleanup()

    close_database()


# =====================================================
# SELF TEST
# =====================================================

def run_self_test() -> bool:
    """
    Validate database module.
    """

    try:

        assert database_exists()

        assert integrity_check()

        assert isinstance(
            history_count(),
            int,
        )

        assert isinstance(
            vault_count(),
            int,
        )

        assert isinstance(
            favorite_count(),
            int,
        )

        assert isinstance(
            diagnostics(),
            dict,
        )

        assert isinstance(
            database_health(),
            dict,
        )

        assert isinstance(
            vault_statistics(),
            dict,
        )

        return True

    except Exception:

        return False


# =====================================================
# MODULE INFO
# =====================================================

def module_information() -> dict[str, Any]:
    """
    Module metadata.
    """

    return {

        "name":
            MODULE_NAME,

        "version":
            MODULE_VERSION,

        "database":
            DB_NAME,

        "database_path":
            str(DB_PATH),

        "cloud_ready":
            True,

        "sqlite":
            sqlite3.sqlite_version,

        "python":
            "3.11+",

        "status":
            "Production",

    }


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print(
        "Database Module"
    )

    print(
        f"Version : {MODULE_VERSION}"
    )

    print(
        f"Database : {DB_PATH}"
    )

    print(
        f"Integrity : {integrity_check()}"
    )

    print(
        f"History : {history_count()}"
    )

    print(
        f"Vault : {vault_count()}"
    )

    print(
        f"Favorites : {favorite_count()}"
    )

    print(
        f"Backups : {len(available_backups())}"
    )

    print(
        f"Self Test : {run_self_test()}"
    )