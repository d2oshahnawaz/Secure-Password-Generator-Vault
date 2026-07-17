# =====================================================
# PASSWORD VAULT
# Version 5.0 Professional
# Part 1 / 4
# =====================================================

from __future__ import annotations

# =====================================================
# IMPORTS
# =====================================================

from typing import Final

import pyperclip
import streamlit as st

from crypto import (
    encrypt_password,
    decrypt_password,
)

from master import (
    master_exists,
    set_master_password,
    verify_master_password,
    get_security_question,
    verify_recovery,
    reset_master_password,
    DEFAULT_SECURITY_QUESTIONS,
)

from database import (
    save_vault,
    get_vault,
    search_vault,
    delete_vault,
    update_vault,
    toggle_favorite,
    get_favorites,
    filter_category,
    expired_passwords,
    vault_count,
    favorite_count,
)

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

    "WiFi",

    "Office",

    "Personal",

    "Other",

]

MIN_MASTER_PASSWORD_LENGTH: Final[int] = 8

# =====================================================
# SESSION STATE
# =====================================================

def initialize_session() -> None:
    """
    Initialize Password Vault session state.
    """

    defaults = {

        "vault_unlocked": False,

        "editing_id": None,

        "show_favorites": False,

        "show_expired": False,

        # Recovery

        "show_recovery": False,

        "recovery_verified": False,

        "generated_recovery_key": "",

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def copy_password(password: str) -> None:
    """
    Copy password to clipboard.
    """

    try:

        pyperclip.copy(password)

        st.success(
            "Password copied successfully."
        )

    except Exception:

        st.warning(
            "Clipboard is unavailable."
        )


def lock_vault() -> None:
    """
    Lock Password Vault.
    """

    st.session_state.vault_unlocked = False

    st.session_state.editing_id = None

    st.session_state.show_recovery = False

    st.session_state.recovery_verified = False

    st.success(
        "Vault locked successfully."
    )

    st.rerun()


def show_recovery_key(
    recovery_key: str,
) -> None:
    """
    Display Recovery Key after setup.
    """

    st.success(
        "Master Password created successfully."
    )

    st.warning(
        "Save this Recovery Key safely. "
        "It will be required if you ever "
        "forget your Master Password."
    )

    st.code(
        recovery_key,
        language="text",
    )


def validate_master_password(
    password1: str,
    password2: str,
) -> bool:
    """
    Validate Master Password.
    """

    if not password1.strip():

        st.error(
            "Master Password cannot be empty."
        )

        return False

    if len(password1) < MIN_MASTER_PASSWORD_LENGTH:

        st.error(
            f"Master Password must contain at least "
            f"{MIN_MASTER_PASSWORD_LENGTH} characters."
        )

        return False

    if password1 != password2:

        st.error(
            "Passwords do not match."
        )

        return False

    return True

# =====================================================
# MASTER PASSWORD SETUP
# =====================================================

def setup_master_password() -> bool:
    """
    Create Master Password if it does not exist.
    """

    if master_exists():

        return True

    st.subheader("Create Master Password")

    st.info(
        "Create a strong Master Password to protect your Password Vault."
    )

    password1 = st.text_input(
        "Master Password",
        type="password",
    )

    password2 = st.text_input(
        "Confirm Master Password",
        type="password",
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

        st.session_state.generated_recovery_key = (

            recovery_key

        )

        show_recovery_key(
            recovery_key
        )

        st.success(
            "Setup completed successfully."
        )

        st.info(
            "Copy the Recovery Key before continuing."
        )

        if st.button(
            "Continue to Vault",
            use_container_width=True,
            type="primary",
        ):

            st.rerun()

    except Exception as error:

        st.error(
            f"Unable to create Master Password.\n\n{error}"
        )

    return False

# =====================================================
# UNLOCK VAULT
# =====================================================

def unlock_vault() -> bool:
    """
    Unlock Password Vault.
    Supports Master Password recovery.
    """

    if st.session_state.vault_unlocked:

        return True

    st.subheader("Unlock Password Vault")

    # =====================================================
    # NORMAL LOGIN
    # =====================================================

    if not st.session_state.show_recovery:

        password = st.text_input(
            "Master Password",
            type="password",
        )

        if st.button(
            "Unlock Vault",
            use_container_width=True,
            type="primary",
        ):

            if verify_master_password(password):

                st.session_state.vault_unlocked = True

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

            st.session_state.show_recovery = True

            st.rerun()

        return False

    # =====================================================
    # RECOVERY SCREEN
    # =====================================================

    st.warning(
        "Recover Master Password"
    )

    st.info(
        "Verify your Recovery Key and "
        "Security Answer."
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

    security_answer = st.text_input(
        "Security Answer",
        type="password",
    )

    verify_col, cancel_col = st.columns(2)

    with verify_col:

        verify_clicked = st.button(
            "Verify Recovery",
            use_container_width=True,
        )

    with cancel_col:

        cancel_clicked = st.button(
            "Cancel",
            use_container_width=True,
        )

    if cancel_clicked:

        st.session_state.show_recovery = False

        st.session_state.recovery_verified = False

        st.rerun()

    if verify_clicked:

        if verify_recovery(
            recovery_key,
            security_answer,
        ):

            st.session_state.recovery_verified = True

            st.success(
                "Recovery verified successfully."
            )

        else:

            st.error(
                "Recovery verification failed."
            )

            return False

    # =====================================================
    # RESET PASSWORD
    # =====================================================

    if st.session_state.recovery_verified:

        st.divider()

        st.subheader(
            "Reset Master Password"
        )

        new_password = st.text_input(
            "New Master Password",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
        )

        if st.button(
            "Reset Password",
            use_container_width=True,
            type="primary",
        ):

            if not validate_master_password(
                new_password,
                confirm_password,
            ):

                return False

            try:

                reset_master_password(
                    new_password
                )

                st.success(
                    "Master Password reset successfully."
                )

                st.session_state.show_recovery = False

                st.session_state.recovery_verified = False

                st.rerun()

            except Exception as error:

                st.error(
                    f"Unable to reset password.\n\n{error}"
                )

    return False

# =====================================================
# MAIN VAULT
# =====================================================

def show_vault() -> None:
    """
    Main Password Vault UI.
    """

    initialize_session()

    st.title("Password Vault")

    if not setup_master_password():
        return

    if not unlock_vault():
        return

    # =====================================================
    # DASHBOARD
    # =====================================================

    total_passwords = vault_count()
    favorites = favorite_count()
    expired = len(expired_passwords())

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Stored Passwords",
            total_passwords,
        )

    with metric2:
        st.metric(
            "Favorites",
            favorites,
        )

    with metric3:
        st.metric(
            "Expired",
            expired,
        )

    st.divider()

    # =====================================================
    # ADD PASSWORD
    # =====================================================

    st.subheader("Add New Password")

    with st.form(
        "vault_form",
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
            placeholder="Work, Office, Personal",
        )

        notes = st.text_area(
            "Notes",
            placeholder="Optional notes...",
        )

        favorite = st.checkbox(
            "Mark as Favorite"
        )

        expiry_date = st.date_input(
            "Password Expiry Date",
            value=None,
        )

        submitted = st.form_submit_button(
            "Save Password",
            use_container_width=True,
        )

    # =====================================================
    # SAVE PASSWORD
    # =====================================================

    if submitted:

        website = website.strip()
        username = username.strip()
        password = password.strip()
        tags = tags.strip()
        notes = notes.strip()

        if not website:

            st.error(
                "Website is required."
            )

        elif not username:

            st.error(
                "Username is required."
            )

        elif not password:

            st.error(
                "Password is required."
            )

        else:

            try:

                encrypted_password = encrypt_password(
                    password
                )

                save_vault(

                    website=website,

                    username=username,

                    encrypted_password=encrypted_password,

                    category=category,

                    tags=tags,

                    notes=notes,

                    favorite=int(favorite),

                    expiry_date=(
                        expiry_date.isoformat()
                        if expiry_date
                        else None
                    ),

                )

                st.success(
                    "Password saved successfully."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Failed to save password.\n\n{error}"
                )

    st.divider()

    # =====================================================
    # SEARCH & FILTER
    # =====================================================

    st.subheader("Search Passwords")

    keyword = st.text_input(
        "Search",
        placeholder="Search by website, username, category or tags...",
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        show_all = st.button(
            "All Passwords",
            use_container_width=True,
        )

    with filter_col2:

        show_favorites = st.button(
            "Favorites",
            use_container_width=True,
        )

    with filter_col3:

        show_expired = st.button(
            "Expired",
            use_container_width=True,
        )

    # =====================================================
    # LOAD PASSWORDS
    # =====================================================

    rows = []

    if keyword.strip():

        rows = search_vault(
            keyword.strip()
        )

    elif show_favorites:

        rows = get_favorites()

    elif show_expired:

        rows = expired_passwords()

    elif st.session_state.show_favorites:

        rows = get_favorites()

    elif st.session_state.show_expired:

        rows = expired_passwords()

    else:

        rows = get_vault()

    if show_all:

        st.session_state.show_favorites = False

        st.session_state.show_expired = False

        rows = get_vault()

    elif show_favorites:

        st.session_state.show_favorites = True

        st.session_state.show_expired = False

    elif show_expired:

        st.session_state.show_expired = True

        st.session_state.show_favorites = False

    st.divider()

    st.subheader("Stored Passwords")

    if not rows:

        st.info(
            "No passwords found."
        )

        return

    else:
    
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

                password = "[Unable to decrypt]"

            with st.container(border=True):

                # ==========================================
                # HEADER
                # ==========================================

                left, right = st.columns([6, 1])

                with left:

                    st.subheader(website)

                with right:

                    if favorite:

                        st.success("Favorite")

                # ==========================================
                # DETAILS
                # ==========================================

                info1, info2 = st.columns(2)

                with info1:

                    st.write(
                        f"**Username:** {username}"
                    )

                    st.write(
                        f"**Category:** {category}"
                    )

                with info2:

                    if expiry:

                        st.write(
                            f"**Expiry:** {expiry}"
                        )

                    st.write(
                        f"**Created:** {created}"
                    )

                if tags:

                    st.caption(
                        f"Tags: {tags}"
                    )

                if notes:

                    st.info(notes)

                if updated:

                    st.caption(
                        f"Last Updated: {updated}"
                    )

                # ==========================================
                # PASSWORD
                # ==========================================

                reveal = st.toggle(

                    "Show Password",

                    key=f"show_{vault_id}",

                )

                if reveal:

                    st.code(
                        password,
                        language="text",
                    )

                else:

                    st.code(
                        "*" * len(password),
                        language="text",
                    )

                # ==========================================
                # ACTION BUTTONS
                # ==========================================

                action1, action2, action3, action4 = st.columns(4)

                with action1:

                    if st.button(

                        "Copy",

                        key=f"copy_{vault_id}",

                        use_container_width=True,

                    ):

                        copy_password(password)

                with action2:

                    if st.button(

                        "Favorite",

                        key=f"favorite_{vault_id}",

                        use_container_width=True,

                    ):

                        toggle_favorite(
                            vault_id
                        )

                        st.rerun()

                with action3:

                    if st.button(

                        "Edit",

                        key=f"edit_{vault_id}",

                        use_container_width=True,

                    ):

                        st.session_state.editing_id = (
                            vault_id
                        )

                        st.rerun()

                with action4:

                    if st.button(

                        "Delete",

                        key=f"delete_{vault_id}",

                        use_container_width=True,

                    ):

                        delete_vault(
                            vault_id
                        )

                        st.success(
                            "Password deleted successfully."
                        )

                        st.rerun()

                # ==========================================
                # EDIT PASSWORD
                # ==========================================

                if st.session_state.editing_id == vault_id:

                    st.warning("Edit Password")

                    with st.form(
                        f"edit_form_{vault_id}"
                    ):

                        new_website = st.text_input(
                            "Website / Application",
                            value=website,
                        )

                        new_username = st.text_input(
                            "Username / Email",
                            value=username,
                        )

                        new_password = st.text_input(
                            "Password",
                            value=password,
                            type="password",
                        )

                        if category in CATEGORIES:
                            category_index = CATEGORIES.index(category)
                        else:
                            category_index = 0

                        new_category = st.selectbox(
                            "Category",
                            CATEGORIES,
                            index=category_index,
                        )

                        new_tags = st.text_input(
                            "Tags",
                            value=tags or "",
                        )

                        new_notes = st.text_area(
                            "Notes",
                            value=notes or "",
                        )

                        new_favorite = st.checkbox(
                            "Favorite",
                            value=bool(favorite),
                        )

                        new_expiry = st.text_input(
                            "Expiry Date (YYYY-MM-DD)",
                            value=expiry or "",
                        )

                        save_col, cancel_col = st.columns(2)

                        with save_col:

                            update_clicked = st.form_submit_button(
                                "Update Password",
                                use_container_width=True,
                            )

                        with cancel_col:

                            cancel_clicked = st.form_submit_button(
                                "Cancel",
                                use_container_width=True,
                            )

                    # ======================================
                    # UPDATE PASSWORD
                    # ======================================

                    if update_clicked:

                        new_website = new_website.strip()
                        new_username = new_username.strip()
                        new_password = new_password.strip()
                        new_tags = new_tags.strip()
                        new_notes = new_notes.strip()
                        new_expiry = new_expiry.strip()

                        if not new_website:

                            st.error(
                                "Website is required."
                            )

                        elif not new_username:

                            st.error(
                                "Username is required."
                            )

                        elif not new_password:

                            st.error(
                                "Password is required."
                            )

                        else:

                            try:

                                encrypted = encrypt_password(
                                    new_password
                                )

                                update_vault(

                                    vault_id,

                                    new_website,

                                    new_username,

                                    encrypted,

                                    new_category,

                                    new_tags,

                                    new_notes,

                                    int(new_favorite),

                                    new_expiry if new_expiry else None,

                                )

                                st.session_state.editing_id = None

                                st.success(
                                    "Password updated successfully."
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    f"Unable to update password.\n\n{error}"
                                )

                    # ======================================
                    # CANCEL EDIT
                    # ======================================

                    if cancel_clicked:

                        st.session_state.editing_id = None

                        st.rerun()

    # =====================================================
    # VAULT SUMMARY
    # =====================================================

    st.divider()

    st.subheader("Vault Summary")

    summary1, summary2, summary3 = st.columns(3)

    with summary1:
        st.metric(
            "Stored Passwords",
            vault_count(),
        )

    with summary2:
        st.metric(
            "Favorites",
            favorite_count(),
        )

    with summary3:
        st.metric(
            "Expired",
            len(expired_passwords()),
        )

    st.divider()

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.subheader("Quick Actions")

    action1, action2, action3 = st.columns(3)

    with action1:

        if st.button(
            "Show Favorites",
            use_container_width=True,
        ):

            st.session_state.show_favorites = True
            st.session_state.show_expired = False
            st.rerun()

    with action2:

        if st.button(
            "Show Expired",
            use_container_width=True,
        ):

            st.session_state.show_expired = True
            st.session_state.show_favorites = False
            st.rerun()

    with action3:

        if st.button(
            "Show All",
            use_container_width=True,
        ):

            st.session_state.show_favorites = False
            st.session_state.show_expired = False
            st.rerun()

    st.divider()

    # =====================================================
    # SECURITY INFORMATION
    # =====================================================

    with st.expander(
        "Password Vault Security",
        expanded=False,
    ):

        st.markdown(
            """
### Security Features

- AES Encrypted Password Storage
- Master Password Protection
- Recovery Key Support
- Security Question Verification
- Secure Password Decryption
- Search & Filter
- Password Categories
- Password Expiry Tracking
- Clipboard Copy Support
- Edit & Delete Passwords

---

### Security Tips

- Never share your Master Password.
- Store your Recovery Key offline.
- Use a unique password for every account.
- Enable Multi-Factor Authentication (MFA).
- Rotate important passwords regularly.
- Backup your encrypted database.
- Delete passwords you no longer use.

---

### Dashboard Metrics

The vault dashboard displays:

- Total Stored Passwords
- Favorite Password Count
- Expired Password Count
- Search & Filter Status
"""
        )

    st.divider()

    # =====================================================
    # LOCK VAULT
    # =====================================================

    if st.button(
        "Lock Vault",
        type="primary",
        use_container_width=True,
    ):

        lock_vault()

    st.divider()

    # =====================================================
    # FOOTER
    # =====================================================

    st.caption(
        "Smart Password Generator & Vault • Version 5.0 Professional"
    )