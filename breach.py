# =====================================================
# PASSWORD BREACH CHECKER
# Version 5.0 Professional
# =====================================================

from pathlib import Path
import streamlit as st

# =====================================================
# DATABASE PATH
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
            encoding="utf-8",
        ) as file:

            passwords = {
                line.strip().lower()
                for line in file
                if line.strip()
            }

            return passwords

    except FileNotFoundError:

        st.error(
            "Local breach database not found."
        )

        return set()

    except Exception as error:

        st.error(
            f"Unable to load breach database.\n\n{error}"
        )

        return set()


COMMON_PASSWORDS = load_passwords()

# =====================================================
# CHECK PASSWORD
# =====================================================

def check_breach(password: str) -> bool:
    """
    Returns True if password exists
    in local breach database.
    """

    if not password:
        return False

    return password.lower() in COMMON_PASSWORDS


# =====================================================
# BREACH REPORT
# =====================================================

def show_breach_check(password: str):

    st.markdown(
        """
<h3>
<i class="bi bi-shield-exclamation"></i>
Password Breach Checker
</h3>
""",
        unsafe_allow_html=True,
    )

    breached = check_breach(password)

    # =================================================
    # OVERVIEW
    # =================================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Database Size",
            f"{len(COMMON_PASSWORDS):,}",
        )

    with col2:

        st.metric(
            "Status",
            "Breached" if breached else "Safe",
        )

    st.divider()

    # =================================================
    # RESULT
    # =================================================

    if breached:

        st.error(
            "This password was found in the local breach database."
        )

        st.markdown(
            """
<div class="card">

<h4>
<i class="bi bi-exclamation-triangle-fill"></i>
Risk Level : HIGH
</h4>

This password is commonly used and should not be used for any online account.

</div>
""",
            unsafe_allow_html=True,
        )

    else:

        st.success(
            "This password was not found in the local breach database."
        )

        st.markdown(
            """
<div class="card">

<h4>
<i class="bi bi-shield-check"></i>
Risk Level : LOW
</h4>

No match was found in the offline breach database.

</div>
""",
            unsafe_allow_html=True,
        )

    # =================================================
    # SECURITY RECOMMENDATIONS
    # =================================================

    st.markdown(
        """
<h4>
<i class="bi bi-lightbulb"></i>
Security Recommendations
</h4>
""",
        unsafe_allow_html=True,
    )

    recommendations = [
        "Use at least 16 characters.",
        "Include uppercase letters.",
        "Include lowercase letters.",
        "Include numbers.",
        "Include special characters.",
        "Avoid dictionary words.",
        "Avoid personal information.",
        "Use a unique password for every account.",
        "Enable Multi-Factor Authentication (MFA).",
        "Store passwords securely in Password Vault.",
    ]

    for item in recommendations:

        st.write(f"• {item}")

    st.divider()

    # =================================================
    # DATABASE INFORMATION
    # =================================================

    st.markdown(
        """
<h4>
<i class="bi bi-database-fill-check"></i>
Database Information
</h4>
""",
        unsafe_allow_html=True,
    )

    st.info(
        f"""
Offline breach detection is performed using a local password database.

Loaded Passwords : **{len(COMMON_PASSWORDS):,}**

No internet connection is required.

Your password is never transmitted to any external server.
"""
    )