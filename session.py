# =====================================================
# SESSION STATE
# Version 4.2 Professional
# =====================================================

from __future__ import annotations

import streamlit as st

# =====================================================
# DEFAULT SESSION STATE
# =====================================================

DEFAULT_SESSION = {

    # =====================================================
    # PASSWORD GENERATOR
    # =====================================================

    "passwords": [],
    "generated": False,

    # =====================================================
    # PAGE NAVIGATION
    # =====================================================

    "page": "generator",

    "show_history": False,
    "show_dashboard": False,
    "show_vault": False,

    # =====================================================
    # PASSWORD VAULT
    # =====================================================

    "vault_unlocked": False,
    "editing_id": None,

    # =====================================================
    # VAULT FILTERS
    # =====================================================

    "show_favorites": False,
    "show_expired": False,
    "selected_category": "All",

    # =====================================================
    # SEARCH
    # =====================================================

    "search_keyword": "",

    # =====================================================
    # ANALYTICS
    # =====================================================

    "selected_chart": "Strength",

    # =====================================================
    # UI
    # =====================================================

    "theme": "Dark",
    "page_loaded": False,
    "notification": None,

    # =====================================================
    # EXPORT
    # =====================================================

    "export_format": "CSV",

    # =====================================================
    # SECURITY
    # =====================================================

    "master_verified": False,

    # =====================================================
    # BACKUP
    # =====================================================

    "last_backup": None,

}

# =====================================================
# INITIALIZE SESSION
# =====================================================

def initialize_session() -> None:
    """
    Initialize all Streamlit session variables.
    """

    for key, value in DEFAULT_SESSION.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =====================================================
# RESET NAVIGATION
# =====================================================

def reset_navigation() -> None:
    """
    Reset all navigation flags.
    """

    st.session_state.show_history = False
    st.session_state.show_dashboard = False
    st.session_state.show_vault = False

    st.session_state.show_favorites = False
    st.session_state.show_expired = False


# =====================================================
# CHANGE PAGE
# =====================================================

def set_page(page: str) -> None:
    """
    Change current application page.
    """

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