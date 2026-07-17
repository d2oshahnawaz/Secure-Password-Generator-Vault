# =====================================================
# PASSWORD BREACH CHECKER
# Version 4.0 Professional
# =====================================================

from pathlib import Path

import streamlit as st

# =====================================================
# DATABASE
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

PASSWORD_FILE = BASE_DIR / "data" / "common_passwords.txt"

# =====================================================
# LOAD PASSWORD DATABASE
# =====================================================

@st.cache_data(show_spinner=False)
def load_passwords():
    """
    Load local password breach database.
    """

    try:

        with open(
            PASSWORD_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return {

                line.strip().lower()

                for line in file

                if line.strip()

            }

    except FileNotFoundError:

        return set()


COMMON_PASSWORDS = load_passwords()

# =====================================================
# CHECK PASSWORD
# =====================================================

def check_breach(password):
    """
    Return True if password exists
    in local breach database.
    """

    return str(password).lower() in COMMON_PASSWORDS


# =====================================================
# BREACH UI
# =====================================================

def show_breach_check(password):

    st.subheader("Password Breach Checker")

    breached = check_breach(password)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Database Size",
            f"{len(COMMON_PASSWORDS):,}"
        )

    with col2:

        st.metric(
            "Password Status",
            "Breached" if breached else "Safe"
        )

    st.divider()

    if breached:

        st.error(
            "This password exists in the local breach database."
        )

        st.warning(
            """
Risk Level: HIGH

Choose another password immediately.
"""
        )

        st.info(
            """
Recommended:

• Minimum 12 characters

• Uppercase letters

• Lowercase letters

• Numbers

• Special characters
"""
        )

    else:

        st.success(
            "This password was not found in the local breach database."
        )

        st.info(
            """
Risk Level: LOW

No match found in the offline breach database.
"""
        )

    st.caption(
        "Offline breach detection using a local common-password database."
    )