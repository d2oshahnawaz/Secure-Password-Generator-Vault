# =====================================================
# SESSION STATE
# Version 5.0 Professional
# =====================================================

from __future__ import annotations

from typing import Any

import streamlit as st

# =====================================================
# VALID PAGES
# =====================================================

VALID_PAGES = {
    "generator",
    "dashboard",
    "vault",
    "history",
    "favorites",
    "expired",
}

# =====================================================
# DEFAULT SESSION STATE
# =====================================================

DEFAULT_SESSION = {

    # =================================================
    # PASSWORD GENERATOR
    # =================================================

    "passwords": [],
    "generated": False,
    "extra_passwords": [],

    # =================================================
    # PAGE NAVIGATION
    # =================================================

    "page": "generator",

    "show_history": False,
    "show_dashboard": False,
    "show_vault": False,

    # =================================================
    # PASSWORD VAULT
    # =================================================

    "vault_unlocked": False,
    "editing_id": None,

    # =================================================
    # VAULT FILTERS
    # =================================================

    "show_favorites": False,
    "show_expired": False,
    "selected_category": "All",

    # =================================================
    # SEARCH
    # =================================================

    "search_keyword": "",

    # =================================================
    # ANALYTICS
    # =================================================

    "selected_chart": "Strength",

    # =================================================
    # USER INTERFACE
    # =================================================

    "theme": "Dark",
    "page_loaded": False,
    "notification": None,

    # =================================================
    # EXPORT
    # =================================================

    "export_format": "CSV",

    # =================================================
    # SECURITY
    # =================================================

    "master_verified": False,

    # =================================================
    # BACKUP
    # =================================================

    "last_backup": None,

}

# =====================================================
# INITIALIZE SESSION
# =====================================================

def initialize_session() -> None:
    """
    Initialize Streamlit session state.
    """

    for key, value in DEFAULT_SESSION.items():

        st.session_state.setdefault(
            key,
            value,
        )

# =====================================================
# GET SESSION VALUE
# =====================================================

def get_session(
    key: str,
    default: Any = None,
) -> Any:
    """
    Return a session value.
    """

    return st.session_state.get(
        key,
        default,
    )

# =====================================================
# SET SESSION VALUE
# =====================================================

def set_session(
    key: str,
    value: Any,
) -> None:
    """
    Store a session value.
    """

    st.session_state[key] = value

# =====================================================
# CLEAR SESSION VALUE
# =====================================================

def clear_session(
    key: str,
) -> None:
    """
    Remove a session key.
    """

    if key in st.session_state:

        del st.session_state[key]

# =====================================================
# RESET NAVIGATION
# =====================================================

def reset_navigation() -> None:
    """
    Reset navigation flags.
    """

    st.session_state.show_history = False
    st.session_state.show_dashboard = False
    st.session_state.show_vault = False

    st.session_state.show_favorites = False
    st.session_state.show_expired = False

# =====================================================
# CHANGE PAGE
# =====================================================

def set_page(
    page: str,
) -> None:
    """
    Change application page.
    """

    if page not in VALID_PAGES:

        page = "generator"

    reset_navigation()

    st.session_state.page = page

    if page == "history":

        st.session_state.show_history = True

    elif page == "dashboard":

        st.session_state.show_dashboard = True

    elif page == "vault":

        st.session_state.show_vault = True

    elif page == "favorites":

        st.session_state.show_vault = True
        st.session_state.show_favorites = True

    elif page == "expired":

        st.session_state.show_vault = True
        st.session_state.show_expired = True

# =====================================================
# CURRENT PAGE
# =====================================================

def current_page() -> str:
    """
    Return current page.
    """

    return st.session_state.get(
        "page",
        "generator",
    )

# =====================================================
# RESET PASSWORD GENERATOR
# =====================================================

def reset_generator() -> None:
    """
    Clear generated passwords.
    """

    st.session_state.passwords = []
    st.session_state.extra_passwords = []
    st.session_state.generated = False

# =====================================================
# RESET APPLICATION
# =====================================================

def reset_application() -> None:
    """
    Reset complete application state.
    """

    for key, value in DEFAULT_SESSION.items():

        st.session_state[key] = value

# =====================================================
# SESSION INFORMATION
# =====================================================

def session_info() -> dict:
    """
    Return session information.
    """

    return {

        "current_page": current_page(),

        "generated": st.session_state.generated,

        "passwords": len(
            st.session_state.passwords
        ),

        "extra_passwords": len(
            st.session_state.extra_passwords
        ),

        "vault_unlocked":
            st.session_state.vault_unlocked,

        "theme":
            st.session_state.theme,

    }

# =====================================================
# END OF FILE
# session.py
# Version 5.0 Professional
# =====================================================