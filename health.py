# =====================================================
# PASSWORD HEALTH REPORT
# Version 5.0 Professional
# =====================================================

from __future__ import annotations

import re
from typing import Dict, List

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
# PASSWORD HEALTH ANALYSIS
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
            re.search(r"(.)\1{2,}", password)
        ),
        "common": password.lower() in COMMON_PASSWORDS,
    }

    for sequence in SEQUENCES:

        for i in range(len(sequence) - 3):

            if sequence[i:i + 4] in password:

                report["sequential"] = True
                break

        if report["sequential"]:
            break

    return report

# =====================================================
# HEALTH SCORE
# =====================================================

def health_score(report: Dict[str, bool]) -> int:
    """
    Calculate password health score.
    """

    score = 100

    if not report["length"]:
        score -= 20

    if not report["uppercase"]:
        score -= 10

    if not report["lowercase"]:
        score -= 10

    if not report["numbers"]:
        score -= 10

    if not report["symbols"]:
        score -= 10

    if report["spaces"]:
        score -= 10

    if report["sequential"]:
        score -= 15

    if report["repeated"]:
        score -= 10

    if report["common"]:
        score -= 25

    return max(score, 0)

# =====================================================
# RECOMMENDATIONS
# =====================================================

def health_recommendations(report: Dict[str, bool]) -> List[str]:
    """
    Return improvement suggestions.
    """

    recommendations = []

    if not report["length"]:
        recommendations.append(
            "Increase password length to at least 12 characters."
        )

    if not report["uppercase"]:
        recommendations.append(
            "Include uppercase letters."
        )

    if not report["lowercase"]:
        recommendations.append(
            "Include lowercase letters."
        )

    if not report["numbers"]:
        recommendations.append(
            "Include numeric digits."
        )

    if not report["symbols"]:
        recommendations.append(
            "Include special characters."
        )

    if report["spaces"]:
        recommendations.append(
            "Avoid spaces in passwords."
        )

    if report["sequential"]:
        recommendations.append(
            "Avoid sequential characters."
        )

    if report["repeated"]:
        recommendations.append(
            "Avoid repeated characters."
        )

    if report["common"]:
        recommendations.append(
            "Choose a unique password."
        )

    return recommendations

# =====================================================
# HEALTH REPORT UI
# =====================================================

def show_health_report(password: str) -> None:
    """
    Display password health report.
    """

    report = password_health(password)

    score = health_score(report)

    st.markdown(
        """
### <i class="bi bi-heart-pulse-fill"></i>
Password Health Report
""",
        unsafe_allow_html=True,
    )

    st.progress(score / 100)

    st.metric(
        "Health Score",
        f"{score}/100",
    )

    st.divider()

    checks = [

        ("Minimum Length (12+)", report["length"]),

        ("Contains Uppercase", report["uppercase"]),

        ("Contains Lowercase", report["lowercase"]),

        ("Contains Numbers", report["numbers"]),

        ("Contains Symbols", report["symbols"]),
    ]

    for title, status in checks:

        if status:
            st.success(title)
        else:
            st.error(title)

    st.divider()

    warnings = []

    if report["spaces"]:
        warnings.append("Password contains spaces.")

    if report["sequential"]:
        warnings.append("Sequential characters detected.")

    if report["repeated"]:
        warnings.append("Repeated characters detected.")

    if report["common"]:
        warnings.append(
            "Password found in common password list."
        )

    if warnings:

        st.markdown(
            """
#### <i class="bi bi-exclamation-triangle-fill"></i>
Security Warnings
""",
            unsafe_allow_html=True,
        )

        for warning in warnings:
            st.warning(warning)

    else:

        st.success(
            "No security issues detected."
        )

    st.divider()

    recommendations = health_recommendations(report)

    st.markdown(
        """
#### <i class="bi bi-lightbulb-fill"></i>
Recommendations
""",
        unsafe_allow_html=True,
    )

    if recommendations:

        for item in recommendations:
            st.info(item)

    else:

        st.success(
            "Your password follows all recommended security practices."
        )

    st.divider()

    st.markdown(
        """
#### <i class="bi bi-clipboard-data-fill"></i>
Summary
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Checks Passed",
            sum(
                [
                    report["length"],
                    report["uppercase"],
                    report["lowercase"],
                    report["numbers"],
                    report["symbols"],
                ]
            ),
        )

    with col2:

        st.metric(
            "Warnings",
            len(warnings),
        )