# =====================================================
# PASSWORD HEALTH REPORT
# Version 4.0 Professional
# =====================================================

import re
from typing import Dict

import streamlit as st

# =====================================================
# CONSTANTS
# =====================================================

MIN_PASSWORD_LENGTH = 12

COMMON_PASSWORDS = {

    "password",

    "password123",

    "admin",

    "welcome",

    "letmein",

    "qwerty",

    "123456",

    "12345678",

    "abc123",

}

SEQUENCES = [

    "0123456789",

    "123456789",

    "abcdefghijklmnopqrstuvwxyz",

    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",

]

# =====================================================
# PASSWORD HEALTH
# =====================================================

def password_health(password: str) -> Dict[str, bool]:
    """
    Analyze password health.
    """

    report = {

        "length": len(password) >= MIN_PASSWORD_LENGTH,

        "uppercase": any(c.isupper() for c in password),

        "lowercase": any(c.islower() for c in password),

        "numbers": any(c.isdigit() for c in password),

        "symbols": any(not c.isalnum() for c in password),

        "spaces": " " in password,

        "sequential": False,

        "repeated": bool(

            re.search(

                r"(.)\1{2,}",

                password

            )

        ),

        "common": password.lower() in COMMON_PASSWORDS,

    }

    # ---------------------------------------------
    # Sequential Characters
    # ---------------------------------------------

    for sequence in SEQUENCES:

        for index in range(len(sequence) - 3):

            if sequence[index:index + 4] in password:

                report["sequential"] = True

                break

        if report["sequential"]:

            break

    return report


# =====================================================
# HEALTH REPORT UI
# =====================================================

def show_health_report(password: str) -> None:
    """
    Display password health report.
    """

    report = password_health(password)

    st.markdown("""
### <i class="bi bi-heart-pulse-fill"></i> Password Health Report
""", unsafe_allow_html=True)

    checks = [

        ("Minimum Length (12+)", report["length"]),

        ("Contains Uppercase Letter", report["uppercase"]),

        ("Contains Lowercase Letter", report["lowercase"]),

        ("Contains Number", report["numbers"]),

        ("Contains Special Character", report["symbols"]),

    ]

    for label, passed in checks:

        if passed:

            st.success(label)

        else:

            st.error(label)

    warnings = []

    if report["spaces"]:

        warnings.append("Password contains spaces.")

    if report["sequential"]:

        warnings.append("Sequential characters detected.")

    if report["repeated"]:

        warnings.append("Repeated characters detected.")

    if report["common"]:

        warnings.append("Password exists in the common password list.")

    if warnings:

        st.markdown("#### Security Warnings")

        for item in warnings:

            st.warning(item)

    else:

        st.success(
            "No health issues detected."
        )