# =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 1/5
# =====================================================

from __future__ import annotations

# =====================================================
# STANDARD LIBRARY
# =====================================================

from datetime import datetime
from typing import Final, Any

# =====================================================
# THIRD PARTY
# =====================================================

import streamlit as st

# =====================================================
# LOCAL MODULES
# =====================================================

from crypto import encrypt_password, decrypt_password

from master import (
    DEFAULT_SECURITY_QUESTIONS,
    master_exists,
    verify_master_password,
    set_master_password,
    reset_master_password,
    verify_recovery,
    get_security_question,
)

from database import (
    save_vault,
    get_vault,
    update_vault,
    delete_vault,
    search_vault,
    filter_category,
    toggle_favorite,
    get_favorites,
    expired_passwords,
    vault_count,
    favorite_count,
)

# =====================================================
# MODULE INFO
# =====================================================

MODULE_NAME: Final = "Password Vault"

MODULE_VERSION: Final = "6.0 Professional"

# =====================================================
# CONSTANTS
# =====================================================

CATEGORIES: Final[list[str]] = [
    "Email",
    "Banking",
    "Social Media",
    "Shopping",
    "Gaming",
    "Developer",
    "Cloud",
    "Database",
    "Server",
    "WiFi",
    "Office",
    "Personal",
    "Business",
    "Other",
]

MIN_MASTER_PASSWORD_LENGTH = 8
AUTO_LOCK_MINUTES = 10
MAX_NOTE_LENGTH = 500
MAX_TAG_LENGTH = 100

# =====================================================
# SESSION INITIALIZATION
# =====================================================

def initialize_session() -> None:
    """
    Initialize all session variables.
    Safe to call multiple times.
    """

    defaults = {

        "vault_unlocked": False,

        "editing_id": None,

        "selected_password": None,

        "search_keyword": "",

        "selected_category": "All",

        "show_favorites": False,

        "show_expired": False,

        "show_recovery": False,

        "recovery_verified": False,

        "generated_recovery_key": "",

        "last_activity": datetime.now(),

    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


# =====================================================
# SESSION HELPERS
# =====================================================

def update_activity() -> None:
    """Update last activity time."""

    st.session_state["last_activity"] = datetime.now()


def session_expired() -> bool:
    """Check inactivity timeout."""

    if not st.session_state.get("vault_unlocked", False):
        return False

    elapsed = (
        datetime.now()
        - st.session_state["last_activity"]
    ).total_seconds()

    return elapsed > AUTO_LOCK_MINUTES * 60


def auto_lock() -> None:
    """Automatically lock vault."""

    if session_expired():

        st.session_state["vault_unlocked"] = False

        st.warning(
            "Vault locked due to inactivity."
        )

        st.rerun()


def lock_vault() -> None:
    """Manual lock."""

    st.session_state["vault_unlocked"] = False
    st.session_state["editing_id"] = None
    st.session_state["selected_password"] = None
    st.session_state["show_recovery"] = False
    st.session_state["recovery_verified"] = False

    st.success("Vault Locked Successfully.")

    st.rerun()


# =====================================================
# VALIDATION
# =====================================================

def validate_master_password(
    password1: str,
    password2: str,
) -> bool:

    if not password1.strip():

        st.error("Master Password cannot be empty.")

        return False

    if len(password1) < MIN_MASTER_PASSWORD_LENGTH:

        st.error(
            f"Minimum {MIN_MASTER_PASSWORD_LENGTH} characters required."
        )

        return False

    if password1 != password2:

        st.error("Passwords do not match.")

        return False

    return True


def validate_entry(
    website: str,
    username: str,
    password: str,
    tags: str,
    notes: str,
) -> bool:

    if not website.strip():

        st.error("Website is required.")

        return False

    if not username.strip():

        st.error("Username is required.")

        return False

    if not password.strip():

        st.error("Password is required.")

        return False

    if len(tags) > MAX_TAG_LENGTH:

        st.error(
            f"Tags cannot exceed {MAX_TAG_LENGTH} characters."
        )

        return False

    if len(notes) > MAX_NOTE_LENGTH:

        st.error(
            f"Notes cannot exceed {MAX_NOTE_LENGTH} characters."
        )

        return False

    return True


# =====================================================
# UI HELPERS
# =====================================================

def password_mask(password: str) -> str:
    return "*" * len(password)


def favorite_badge(favorite: bool) -> None:

    if favorite:
        st.success("★ Favorite")


def category_badge(category: str) -> None:

    st.caption(f"Category : {category}")


def copy_button(password: str, key: str) -> None:
    """
    Placeholder copy button.
    Replace later with clipboard.py if required.
    """

    st.code(password, language="text")

    st.caption(
        "Use the copy icon above."
    )


# =====================================================
# MODULE INFO
# =====================================================

def module_info() -> dict[str, Any]:

    return {

        "module": MODULE_NAME,

        "version": MODULE_VERSION,

        "cloud_ready": True,

        "auto_lock_minutes": AUTO_LOCK_MINUTES,

    }
    
    # =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 2/5
# Master Password + Login + Recovery
# =====================================================

# =====================================================
# RECOVERY KEY
# =====================================================

def show_recovery_key(
    recovery_key: str,
) -> None:
    """
    Display Recovery Key after creating
    Master Password.
    """

    st.success(
        "Master Password created successfully."
    )

    st.warning(
        "Save this Recovery Key securely.\n"
        "It can be used to recover your vault."
    )

    st.code(
        recovery_key,
        language="text",
    )


# =====================================================
# CREATE MASTER PASSWORD
# =====================================================

def setup_master_password() -> bool:
    """
    Create Master Password if it
    does not already exist.
    """

    if master_exists():
        return True

    st.subheader(
        "Create Master Password"
    )

    st.info(
        "Create a strong Master Password "
        "to protect your Password Vault."
    )

    password1 = st.text_input(
        "Master Password",
        type="password",
        key="master_password_1",
    )

    password2 = st.text_input(
        "Confirm Master Password",
        type="password",
        key="master_password_2",
    )

    security_question = st.selectbox(
        "Security Question",
        DEFAULT_SECURITY_QUESTIONS,
    )

    security_answer = st.text_input(
        "Security Answer",
        type="password",
    )

    create_clicked = st.button(
        "Create Master Password",
        type="primary",
        use_container_width=True,
    )

    if not create_clicked:
        return False

    if not validate_master_password(
        password1,
        password2,
    ):
        return False

    if not security_answer.strip():

        st.error(
            "Security Answer is required."
        )

        return False

    try:

        recovery_key = set_master_password(
            password=password1,
            security_question=security_question,
            security_answer=security_answer,
        )

        st.session_state[
            "generated_recovery_key"
        ] = recovery_key

        show_recovery_key(
            recovery_key
        )

        if st.button(
            "Continue",
            use_container_width=True,
        ):
            st.rerun()

    except Exception as error:

        st.error(str(error))

    return False


# =====================================================
# LOGIN SCREEN
# =====================================================

def login_screen() -> bool:
    """
    Unlock Password Vault.
    """

    st.subheader(
        "Unlock Password Vault"
    )

    password = st.text_input(
        "Master Password",
        type="password",
        key="vault_login_password",
    )

    unlock = st.button(
        "Unlock Vault",
        type="primary",
        use_container_width=True,
    )

    if unlock:

        if verify_master_password(password):

            st.session_state[
                "vault_unlocked"
            ] = True

            update_activity()

            st.success(
                "Vault unlocked successfully."
            )

            st.rerun()

        else:

            st.error(
                "Incorrect Master Password."
            )

    st.divider()

    if st.button(
        "Forgot Master Password?",
        use_container_width=True,
    ):

        st.session_state[
            "show_recovery"
        ] = True

        st.rerun()

    return False


# =====================================================
# RECOVERY SCREEN
# =====================================================

def recovery_screen() -> bool:
    """
    Verify Recovery Key.
    """

    st.warning(
        "Recover Master Password"
    )

    recovery_key = st.text_input(
        "Recovery Key"
    )

    question = get_security_question()

    st.text_input(
        "Security Question",
        value=question,
        disabled=True,
    )

    answer = st.text_input(
        "Security Answer",
        type="password",
    )

    left, right = st.columns(2)

    with left:

        verify_clicked = st.button(
            "Verify",
            use_container_width=True,
        )

    with right:

        cancel_clicked = st.button(
            "Cancel",
            use_container_width=True,
        )

    if cancel_clicked:

        st.session_state[
            "show_recovery"
        ] = False

        st.session_state[
            "recovery_verified"
        ] = False

        st.rerun()

    if verify_clicked:

        if verify_recovery(
            recovery_key,
            answer,
        ):

            st.session_state[
                "recovery_verified"
            ] = True

            st.success(
                "Recovery verified successfully."
            )

        else:

            st.error(
                "Recovery verification failed."
            )

    return st.session_state.get(
        "recovery_verified",
        False,
    )


# =====================================================
# RESET MASTER PASSWORD
# =====================================================

def reset_password_screen() -> None:
    """
    Reset Master Password.
    """

    st.subheader(
        "Reset Master Password"
    )

    password1 = st.text_input(
        "New Master Password",
        type="password",
        key="reset_pass_1",
    )

    password2 = st.text_input(
        "Confirm Password",
        type="password",
        key="reset_pass_2",
    )

    if st.button(
        "Reset Password",
        type="primary",
        use_container_width=True,
    ):

        if not validate_master_password(
            password1,
            password2,
        ):
            return

        try:

            reset_master_password(
                password1
            )

            st.success(
                "Master Password updated successfully."
            )

            st.session_state[
                "show_recovery"
            ] = False

            st.session_state[
                "recovery_verified"
            ] = False

            st.session_state[
                "vault_unlocked"
            ] = False

            st.rerun()

        except Exception as error:

            st.error(str(error))


# =====================================================
# UNLOCK VAULT
# =====================================================

def unlock_vault() -> bool:
    """
    Handle Vault Authentication.
    """

    auto_lock()

    if st.session_state.get(
        "vault_unlocked",
        False,
    ):

        update_activity()

        return True

    if not st.session_state.get(
        "show_recovery",
        False,
    ):

        return login_screen()

    verified = recovery_screen()

    if verified:

        st.divider()

        reset_password_screen()

    return False

# =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 3A/5
# Add Password + Search + Filters
# =====================================================

# =====================================================
# ADD PASSWORD FORM
# =====================================================

def render_add_password() -> None:
    """
    Render Add Password form.
    """

    st.subheader("Add New Password")

    with st.form(
        "vault_add_form",
        clear_on_submit=True,
    ):

        website = st.text_input(
            "Website / Application",
            placeholder="example.com",
        )

        username = st.text_input(
            "Username / Email",
            placeholder="user@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        category = st.selectbox(
            "Category",
            CATEGORIES,
        )

        tags = st.text_input(
            "Tags",
            placeholder="Work, Personal",
        )

        notes = st.text_area(
            "Notes",
            max_chars=MAX_NOTE_LENGTH,
        )

        favorite = st.checkbox(
            "Favorite"
        )

        expiry = st.date_input(
            "Expiry Date",
            value=None,
        )

        submitted = st.form_submit_button(
            "Save Password",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    update_activity()

    if not validate_entry(
        website,
        username,
        password,
        tags,
        notes,
    ):
        return

    try:

        encrypted = encrypt_password(
            password.strip()
        )

        save_vault(
            website=website.strip(),
            username=username.strip(),
            encrypted_password=encrypted,
            category=category,
            tags=tags.strip(),
            notes=notes.strip(),
            favorite=int(favorite),
            expiry_date=(
                expiry.isoformat()
                if expiry
                else None
            ),
        )

        st.success(
            "Password saved successfully."
        )

        st.rerun()

    except Exception as error:

        st.error(
            f"Unable to save password.\n\n{error}"
        )


# =====================================================
# SEARCH & FILTERS
# =====================================================

def render_search_filters() -> list:
    """
    Render Search + Filter section
    and return filtered records.
    """

    st.divider()

    st.subheader("Search Passwords")

    search_text = st.text_input(
        "Search",
        value=st.session_state.get(
            "search_keyword",
            "",
        ),
        placeholder="Website, Username, Category...",
    )

    st.session_state.search_keyword = search_text

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "All",
            use_container_width=True,
        ):

            st.session_state.show_favorites = False
            st.session_state.show_expired = False

    with col2:

        if st.button(
            "Favorites",
            use_container_width=True,
        ):

            st.session_state.show_favorites = True
            st.session_state.show_expired = False

    with col3:

        if st.button(
            "Expired",
            use_container_width=True,
        ):

            st.session_state.show_expired = True
            st.session_state.show_favorites = False

    category_filter = [
        "All",
        *CATEGORIES,
    ]

    selected_category = st.selectbox(
        "Category Filter",
        category_filter,
        index=category_filter.index(
            st.session_state.get(
                "selected_category",
                "All",
            )
        ),
    )

    st.session_state.selected_category = (
        selected_category
    )

    # ----------------------------
    # Fetch records
    # ----------------------------

    if search_text.strip():

        rows = search_vault(
            search_text.strip()
        )

    elif st.session_state.show_favorites:

        rows = get_favorites()

    elif st.session_state.show_expired:

        rows = expired_passwords()

    elif selected_category != "All":

        rows = filter_category(
            selected_category
        )

    else:

        rows = get_vault()

    return rows


# =====================================================
# MAIN CRUD VIEW
# =====================================================

def render_vault_crud() -> list:
    """
    Add Password + Search Filters.
    Returns vault rows.
    """

    render_add_password()

    rows = render_search_filters()

    st.divider()

    st.subheader("Stored Passwords")

    return rows

# =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 3B-1/5
# Password List + Reveal + Favorite
# =====================================================

def render_password_cards(rows: list) -> None:
    """
    Display all stored passwords.
    """

    if not rows:

        st.info(
            "No passwords found."
        )

        return

    for row in rows:

        (
            vault_id,
            website,
            username,
            encrypted_password,
            category,
            tags,
            notes,
            favorite,
            expiry,
            created,
            updated,
        ) = row

        # ---------------------------------------
        # Decrypt Password
        # ---------------------------------------

        try:

            password = decrypt_password(
                encrypted_password
            )

        except Exception:

            password = "[Unable to decrypt]"

        # ---------------------------------------
        # Password Card
        # ---------------------------------------

        with st.container(border=True):

            left, right = st.columns([8, 1])

            with left:

                st.subheader(website)

                category_badge(category)

            with right:

                favorite_badge(bool(favorite))

            info1, info2 = st.columns(2)

            with info1:

                st.write(
                    f"**Username:** {username}"
                )

                if tags:

                    st.caption(
                        f"Tags: {tags}"
                    )

            with info2:

                if expiry:

                    st.write(
                        f"**Expiry:** {expiry}"
                    )

                if updated:

                    st.caption(
                        f"Updated: {updated}"
                    )

            if notes:

                st.info(notes)

            # ---------------------------------------
            # Password Reveal
            # ---------------------------------------

            reveal = st.toggle(
                "Show Password",
                key=f"show_{vault_id}",
            )

            if reveal:

                copy_button(
                    password,
                    key=f"copy_{vault_id}",
                )

            else:

                st.code(
                    password_mask(password),
                    language="text",
                )

            # ---------------------------------------
            # Action Buttons
            # ---------------------------------------

            col1, col2, col3 = st.columns(3)

            # Favorite
            with col1:

                if st.button(
                    "⭐ Favorite",
                    key=f"fav_{vault_id}",
                    use_container_width=True,
                ):

                    toggle_favorite(
                        vault_id
                    )

                    st.rerun()

            # Edit
            with col2:

                if st.button(
                    "✏ Edit",
                    key=f"edit_{vault_id}",
                    use_container_width=True,
                ):

                    st.session_state.editing_id = (
                        vault_id
                    )

                    st.rerun()

            # Delete
            with col3:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{vault_id}",
                    use_container_width=True,
                ):

                    st.session_state[
                        "delete_id"
                    ] = vault_id

                    st.rerun()
                    
# =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 3B-2/5
# Edit + Delete
# =====================================================

            # ==========================================
            # EDIT PASSWORD
            # ==========================================

            if st.session_state.get(
                "editing_id"
            ) == vault_id:

                st.warning(
                    "Edit Password"
                )

                with st.form(
                    f"edit_form_{vault_id}"
                ):

                    new_website = st.text_input(
                        "Website",
                        value=website,
                    )

                    new_username = st.text_input(
                        "Username",
                        value=username,
                    )

                    new_password = st.text_input(
                        "Password",
                        value=password,
                        type="password",
                    )

                    new_category = st.selectbox(
                        "Category",
                        CATEGORIES,
                        index=(
                            CATEGORIES.index(category)
                            if category in CATEGORIES
                            else 0
                        ),
                    )

                    new_tags = st.text_input(
                        "Tags",
                        value=tags or "",
                    )

                    new_notes = st.text_area(
                        "Notes",
                        value=notes or "",
                        max_chars=MAX_NOTE_LENGTH,
                    )

                    new_favorite = st.checkbox(
                        "Favorite",
                        value=bool(favorite),
                    )

                    save_col, cancel_col = st.columns(2)

                    with save_col:

                        update_clicked = (
                            st.form_submit_button(
                                "Update Password",
                                type="primary",
                                use_container_width=True,
                            )
                        )

                    with cancel_col:

                        cancel_clicked = (
                            st.form_submit_button(
                                "Cancel",
                                use_container_width=True,
                            )
                        )

                if cancel_clicked:

                    st.session_state.editing_id = None

                    st.rerun()

                if update_clicked:

                    if validate_entry(
                        new_website,
                        new_username,
                        new_password,
                        new_tags,
                        new_notes,
                    ):

                        try:

                            encrypted = encrypt_password(
                                new_password.strip()
                            )

                            update_vault(
                                vault_id,
                                new_website.strip(),
                                new_username.strip(),
                                encrypted,
                                new_category,
                                new_tags.strip(),
                                new_notes.strip(),
                                int(new_favorite),
                                expiry,
                            )

                            st.success(
                                "Password updated successfully."
                            )

                            st.session_state.editing_id = None

                            st.rerun()

                        except Exception as error:

                            st.error(
                                f"Unable to update password.\n\n{error}"
                            )

            # ==========================================
            # DELETE PASSWORD
            # ==========================================

            if (
                st.session_state.get("delete_id")
                == vault_id
            ):

                st.error(
                    f"Delete '{website}' ?"
                )

                yes_col, no_col = st.columns(2)

                with yes_col:

                    if st.button(
                        "Yes, Delete",
                        key=f"yes_delete_{vault_id}",
                        type="primary",
                        use_container_width=True,
                    ):

                        try:

                            delete_vault(
                                vault_id
                            )

                            st.success(
                                "Password deleted successfully."
                            )

                            st.session_state.delete_id = None

                            st.rerun()

                        except Exception as error:

                            st.error(str(error))

                with no_col:

                    if st.button(
                        "Cancel",
                        key=f"cancel_delete_{vault_id}",
                        use_container_width=True,
                    ):

                        st.session_state.delete_id = None

                        st.rerun()


# =====================================================
# MAIN PASSWORD LIST
# =====================================================

def render_password_list() -> None:
    """
    Render complete password list.
    """

    rows = render_vault_crud()

    render_password_cards(rows)
    
    # =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 3C/5
# Dashboard + Main Entry
# =====================================================

# =====================================================
# DASHBOARD
# =====================================================

def render_dashboard() -> None:
    """
    Vault dashboard.
    """

    st.divider()

    st.subheader("Vault Dashboard")

    total = vault_count()
    favorites = favorite_count()
    expired = len(expired_passwords())

    health_score = 100

    if total == 0:
        health_score -= 40

    if expired > 0:
        health_score -= min(expired * 5, 30)

    if favorites == 0:
        health_score -= 10

    health_score = max(health_score, 0)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Passwords", total)
    c2.metric("Favorites", favorites)
    c3.metric("Expired", expired)
    c4.metric("Health", f"{health_score}/100")

    st.progress(health_score / 100)

    st.divider()

    st.subheader("Security Recommendations")

    recommendations = [

        "Use a unique password for every account.",

        "Enable Multi-Factor Authentication.",

        "Change expired passwords immediately.",

        "Store your Recovery Key offline.",

        "Review your vault regularly.",

        "Delete unused accounts.",

    ]

    for item in recommendations:

        st.markdown(f"- {item}")


# =====================================================
# ABOUT
# =====================================================

def about() -> None:

    st.divider()

    st.subheader("About")

    st.info(
        f"""
**{MODULE_NAME}**

Version : {MODULE_VERSION}

Features

• Master Password

• AES Encryption

• Recovery Key

• Categories

• Search

• Favorites

• Dashboard

• Auto Lock

• Streamlit Cloud Ready
"""
    )


# =====================================================
# FOOTER
# =====================================================

def footer() -> None:

    st.divider()

    if st.button(
        "Lock Vault",
        type="primary",
        use_container_width=True,
    ):

        lock_vault()

    st.caption(
        f"{MODULE_NAME} | Version {MODULE_VERSION}"
    )


# =====================================================
# MAIN FUNCTION
# =====================================================

def show_vault() -> None:
    """
    Main Password Vault UI.
    """

    initialize_session()

    auto_lock()

    # ----------------------------
    # First-time setup
    # ----------------------------

    if not setup_master_password():
        return

    # ----------------------------
    # Login
    # ----------------------------

    if not unlock_vault():
        return

    update_activity()

    # ----------------------------
    # Main UI
    # ----------------------------

    render_password_list()

    render_dashboard()

    about()

    footer()


# =====================================================
# DIAGNOSTICS
# =====================================================

def diagnostics() -> dict[str, Any]:

    return {

        "module": MODULE_NAME,

        "version": MODULE_VERSION,

        "vault_unlocked": st.session_state.get(
            "vault_unlocked",
            False,
        ),

        "total_passwords": vault_count(),

        "favorites": favorite_count(),

        "expired": len(expired_passwords()),

        "auto_lock": AUTO_LOCK_MINUTES,

    }


# =====================================================
# MODULE INFORMATION
# =====================================================

def module_information() -> dict[str, Any]:

    return {

        "name": MODULE_NAME,

        "version": MODULE_VERSION,

        "cloud_ready": True,

        "streamlit": True,

        "python": "3.11+",

    }


# =====================================================
# SELF TEST
# =====================================================

def run_self_test() -> bool:

    try:

        assert isinstance(CATEGORIES, list)

        assert MIN_MASTER_PASSWORD_LENGTH >= 8

        assert AUTO_LOCK_MINUTES > 0

        return True

    except Exception:

        return False


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    if run_self_test():

        show_vault()

    else:

        st.error(
            "Vault self-test failed."
        )
        
        # =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 4/5
# Export • Backup • Utilities
# =====================================================

import json
import pandas as pd

# =====================================================
# EXPORT CSV
# =====================================================

def export_csv() -> None:
    """
    Export vault to CSV.
    """

    rows = get_vault()

    if not rows:
        st.info("No passwords available.")
        return

    data = []

    for row in rows:

        (
            vault_id,
            website,
            username,
            encrypted_password,
            category,
            tags,
            notes,
            favorite,
            expiry,
            created,
            updated,
        ) = row

        try:
            password = decrypt_password(
                encrypted_password
            )
        except Exception:
            password = ""

        data.append(
            {
                "Website": website,
                "Username": username,
                "Password": password,
                "Category": category,
                "Tags": tags,
                "Notes": notes,
                "Favorite": bool(favorite),
                "Expiry": expiry,
                "Created": created,
                "Updated": updated,
            }
        )

    df = pd.DataFrame(data)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False),
        file_name="password_vault.csv",
        mime="text/csv",
    )


# =====================================================
# EXPORT JSON
# =====================================================

def export_json() -> None:

    rows = get_vault()

    if not rows:
        return

    data = []

    for row in rows:

        (
            vault_id,
            website,
            username,
            encrypted_password,
            category,
            tags,
            notes,
            favorite,
            expiry,
            created,
            updated,
        ) = row

        try:
            password = decrypt_password(
                encrypted_password
            )
        except Exception:
            password = ""

        data.append(
            {
                "website": website,
                "username": username,
                "password": password,
                "category": category,
                "tags": tags,
                "notes": notes,
                "favorite": bool(favorite),
                "expiry": expiry,
            }
        )

    st.download_button(
        "⬇ Download JSON",
        json.dumps(data, indent=4),
        file_name="password_vault.json",
        mime="application/json",
    )


# =====================================================
# BACKUP SECTION
# =====================================================

def render_backup_section():

    st.divider()

    st.subheader("Backup & Export")

    c1, c2 = st.columns(2)

    with c1:
        export_csv()

    with c2:
        export_json()


# =====================================================
# QUICK STATS
# =====================================================

def quick_statistics():

    st.divider()

    st.subheader("Quick Statistics")

    st.write(f"Stored Passwords : {vault_count()}")

    st.write(f"Favorites : {favorite_count()}")

    st.write(
        f"Expired : {len(expired_passwords())}"
    )


# =====================================================
# VERSION
# =====================================================

def version():

    st.caption(
        f"{MODULE_NAME} | {MODULE_VERSION}"
    )
    
    # =====================================================
# PASSWORD VAULT
# Version 6.0 Professional
# Part 5/5
# Final Utilities
# =====================================================

from typing import Any

# =====================================================
# SETTINGS
# =====================================================

def render_settings() -> None:
    """
    Vault settings.
    """

    st.divider()

    st.subheader("Settings")

    auto_lock_enabled = st.toggle(
        "Enable Auto Lock",
        value=True,
        disabled=True,
    )

    cloud_ready = st.toggle(
        "Streamlit Cloud Compatible",
        value=True,
        disabled=True,
    )

    encryption = st.toggle(
        "AES Encryption Enabled",
        value=True,
        disabled=True,
    )

    st.caption(
        "These settings are currently managed automatically."
    )


# =====================================================
# DIAGNOSTICS
# =====================================================

def diagnostics() -> dict[str, Any]:
    """
    Return module diagnostics.
    """

    return {

        "module": MODULE_NAME,

        "version": MODULE_VERSION,

        "master_exists": master_exists(),

        "vault_unlocked":
            st.session_state.get(
                "vault_unlocked",
                False,
            ),

        "total_passwords":
            vault_count(),

        "favorites":
            favorite_count(),

        "expired":
            len(
                expired_passwords()
            ),

        "categories":
            len(
                CATEGORIES
            ),

        "auto_lock_minutes":
            AUTO_LOCK_MINUTES,

    }


# =====================================================
# DIAGNOSTICS PANEL
# =====================================================

def diagnostics_panel() -> None:
    """
    Display diagnostics.
    """

    st.divider()

    with st.expander(
        "Diagnostics",
        expanded=False,
    ):

        info = diagnostics()

        for key, value in info.items():

            st.write(
                f"**{key}** : {value}"
            )


# =====================================================
# MODULE INFORMATION
# =====================================================

def module_information() -> dict[str, Any]:

    return {

        "name":
            MODULE_NAME,

        "version":
            MODULE_VERSION,

        "status":
            "Production",

        "author":
            "Tech Education World",

        "python":
            "3.11+",

        "streamlit":
            True,

        "cloud_ready":
            True,

    }


# =====================================================
# SELF TEST
# =====================================================

def run_self_test() -> bool:
    """
    Basic validation.
    """

    try:

        assert isinstance(
            CATEGORIES,
            list,
        )

        assert len(
            CATEGORIES
        ) > 0

        assert (
            MIN_MASTER_PASSWORD_LENGTH
            >= 8
        )

        assert (
            AUTO_LOCK_MINUTES
            > 0
        )

        assert isinstance(
            module_information(),
            dict,
        )

        return True

    except Exception:

        return False


# =====================================================
# APPLICATION
# =====================================================

def run_application() -> None:
    """
    Launch Password Vault.
    """

    show_vault()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    if run_self_test():

        run_application()

    else:

        st.error(
            "Vault self-test failed."
        )