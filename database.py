# =====================================================
# DATABASE
# =====================================================

import sqlite3
from pathlib import Path

# =====================================================
# DATABASE PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "password_history.db"

# =====================================================
# CONNECTION
# =====================================================

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================================
# PASSWORD HISTORY TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    password TEXT,

    strength TEXT,

    entropy REAL,

    crack_time TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# =====================================================
# PASSWORD VAULT TABLE
# =====================================================

cursor.execute("""
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

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

# =====================================================
# AUTO DATABASE MIGRATION
# =====================================================

def add_column_if_not_exists(
    table_name,
    column_name,
    definition
):
    """
    Add a column only if it does not already exist.
    Safe for existing databases.
    """

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [

        column[1]

        for column in cursor.fetchall()

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
# MIGRATE OLD DATABASE
# =====================================================

add_column_if_not_exists(
    "vault",
    "tags",
    "TEXT"
)

add_column_if_not_exists(
    "vault",
    "favorite",
    "INTEGER DEFAULT 0"
)

add_column_if_not_exists(
    "vault",
    "expiry_date",
    "TEXT"
)

add_column_if_not_exists(
    "vault",
    "updated_at",
    "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
)

conn.commit()

# =====================================================
# PASSWORD HISTORY
# =====================================================

def save_password(
    password,
    strength,
    entropy,
    crack_time
):
    """
    Save generated password into history.
    """

    cursor.execute(
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
            crack_time
        )
    )

    conn.commit()


# =====================================================
# GET HISTORY
# =====================================================

def get_history():
    """
    Return complete password history.
    """

    cursor.execute(
        """
        SELECT *

        FROM passwords

        ORDER BY created_at DESC
        """
    )

    return cursor.fetchall()


# =====================================================
# SEARCH HISTORY
# =====================================================

def search_history(keyword):
    """
    Search password history.
    """

    cursor.execute(
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
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    return cursor.fetchall()


# =====================================================
# DELETE HISTORY ITEM
# =====================================================

def delete_history(history_id):
    """
    Delete a single history record.
    """

    cursor.execute(
        """
        DELETE FROM passwords

        WHERE id=?
        """,
        (history_id,)
    )

    conn.commit()


# =====================================================
# HISTORY COUNT
# =====================================================

def history_count():
    """
    Return total saved passwords.
    """

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM passwords
        """
    )

    return cursor.fetchone()[0]


# =====================================================
# CLEAR HISTORY
# =====================================================

def clear_history():
    """
    Delete all password history.
    """

    cursor.execute(
        """
        DELETE FROM passwords
        """
    )

    conn.commit()

# =====================================================
# PASSWORD VAULT
# =====================================================

def save_vault(
    website,
    username,
    encrypted_password,
    category,
    tags,
    notes,
    favorite=0,
    expiry_date=None
):
    """
    Save password into encrypted vault.
    """

    cursor.execute(
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
            expiry_date
        )
    )

    conn.commit()


# =====================================================
# GET ALL PASSWORDS
# =====================================================

def get_vault():
    """
    Return all vault passwords.
    """

    cursor.execute(
        """
        SELECT *

        FROM vault

        ORDER BY created_at DESC
        """
    )

    return cursor.fetchall()


# =====================================================
# SEARCH PASSWORDS
# =====================================================

def search_vault(keyword):
    """
    Search vault.
    """

    cursor.execute(
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
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    return cursor.fetchall()


# =====================================================
# UPDATE PASSWORD
# =====================================================

def update_vault(

    vault_id,

    website,

    username,

    encrypted_password,

    category,

    tags,

    notes,

    favorite,

    expiry_date

):
    """
    Update vault password.
    """

    cursor.execute(
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
            vault_id
        )
    )

    conn.commit()


# =====================================================
# TOGGLE FAVORITE
# =====================================================

def toggle_favorite(vault_id):
    """
    Toggle favorite status.
    """

    cursor.execute(
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
        (vault_id,)
    )

    conn.commit()


# =====================================================
# GET FAVORITES
# =====================================================

def get_favorites():
    """
    Return favorite passwords.
    """

    cursor.execute(
        """
        SELECT *

        FROM vault

        WHERE favorite=1

        ORDER BY created_at DESC
        """
    )

    return cursor.fetchall()


# =====================================================
# FILTER CATEGORY
# =====================================================

def filter_category(category):
    """
    Filter passwords by category.
    """

    cursor.execute(
        """
        SELECT *

        FROM vault

        WHERE category=?

        ORDER BY created_at DESC
        """,
        (category,)
    )

    return cursor.fetchall()


# =====================================================
# EXPIRED PASSWORDS
# =====================================================

def expired_passwords():
    """
    Return expired passwords.
    """

    cursor.execute(
        """
        SELECT *

        FROM vault

        WHERE

        expiry_date IS NOT NULL

        AND date(expiry_date) <= date('now')

        ORDER BY expiry_date
        """
    )

    return cursor.fetchall()


# =====================================================
# DELETE PASSWORD
# =====================================================

def delete_vault(vault_id):
    """
    Delete one vault password.
    """

    cursor.execute(
        """
        DELETE FROM vault

        WHERE id=?
        """,
        (vault_id,)
    )

    conn.commit()


# =====================================================
# CLEAR VAULT
# =====================================================

def clear_vault():
    """
    Delete all vault passwords.
    """

    cursor.execute(
        """
        DELETE FROM vault
        """
    )

    conn.commit()


# =====================================================
# VAULT COUNT
# =====================================================

def vault_count():
    """
    Total passwords stored.
    """

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM vault
        """
    )

    return cursor.fetchone()[0]


# =====================================================
# FAVORITE COUNT
# =====================================================

def favorite_count():
    """
    Total favorite passwords.
    """

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM vault

        WHERE favorite=1
        """
    )

    return cursor.fetchone()[0]


# =====================================================
# CATEGORY COUNT
# =====================================================

def category_count():
    """
    Category wise password count.
    """

    cursor.execute(
        """
        SELECT

        category,

        COUNT(*)

        FROM vault

        GROUP BY category

        ORDER BY COUNT(*) DESC
        """
    )

    return cursor.fetchall()