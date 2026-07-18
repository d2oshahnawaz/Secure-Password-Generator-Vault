# =====================================================
# PASSWORD RECOMMENDATIONS
# Version 5.0 Professional
# =====================================================

from __future__ import annotations

from typing import List

import streamlit as st

from health import password_health
from score import calculate_score

# =====================================================
# CONSTANTS
# =====================================================

MIN_PASSWORD_LENGTH = 12

SPECIAL_CHARACTERS = "@#$%&*+!?_-"

# =====================================================
# GENERATE RECOMMENDATIONS
# =====================================================

def get_recommendations(
    password: str,
    entropy: float,
) -> List[str]:
    """
    Generate password security recommendations.
    """

    report = password_health(password)

    score = calculate_score(
        password,
        entropy,
    )

    recommendations: List[str] = []

    # -------------------------------------------------
    # Length
    # -------------------------------------------------

    if len(password) < MIN_PASSWORD_LENGTH:

        recommendations.append(
            f"Increase password length to at least {MIN_PASSWORD_LENGTH} characters."
        )

    # -------------------------------------------------
    # Character Types
    # -------------------------------------------------

    if not report["uppercase"]:

        recommendations.append(
            "Add at least one uppercase letter."
        )

    if not report["lowercase"]:

        recommendations.append(
            "Add at least one lowercase letter."
        )

    if not report["numbers"]:

        recommendations.append(
            "Include at least one numeric digit."
        )

    if not report["symbols"]:

        recommendations.append(
            f"Include at least one special character ({SPECIAL_CHARACTERS})."
        )

    # -------------------------------------------------
    # Security Checks
    # -------------------------------------------------

    if report["sequential"]:

        recommendations.append(
            "Avoid sequential patterns such as 1234 or abcd."
        )

    if report["repeated"]:

        recommendations.append(
            "Avoid repeating the same character multiple times."
        )

    if report["common"]:

        recommendations.append(
            "Do not use common or dictionary-based passwords."
        )

    if report["spaces"]:

        recommendations.append(
            "Avoid using spaces in passwords."
        )

    # -------------------------------------------------
    # Overall Recommendation
    # -------------------------------------------------

    if score >= 95:

        recommendations.append(
            "Excellent! This password follows modern security best practices."
        )

    elif score >= 80:

        recommendations.append(
            "Strong password. Only minor improvements are possible."
        )

    elif score >= 60:

        recommendations.append(
            "Good password. Increasing randomness will improve security."
        )

    else:

        recommendations.append(
            "Weak password. Consider generating a stronger password."
        )

    return recommendations


# =====================================================
# DISPLAY RECOMMENDATIONS
# =====================================================

def show_recommendations(
    password: str,
    entropy: float,
) -> None:
    """
    Display password recommendations.
    """

    score = calculate_score(
        password,
        entropy,
    )

    st.markdown(
        """
### <i class="bi bi-lightbulb-fill"></i>
Password Recommendations
""",
        unsafe_allow_html=True,
    )

    st.metric(
        "Security Score",
        f"{score}/100",
    )

    st.progress(score / 100)

    st.divider()

    recommendations = get_recommendations(
        password,
        entropy,
    )

    for recommendation in recommendations:

        if recommendation.startswith("Excellent"):

            st.success(recommendation)

        elif recommendation.startswith("Strong"):

            st.success(recommendation)

        elif recommendation.startswith("Good"):

            st.info(recommendation)

        elif recommendation.startswith("Weak"):

            st.error(recommendation)

        else:

            st.warning(recommendation)

    st.divider()

    st.markdown(
        """
#### <i class="bi bi-check-circle-fill"></i>
Password Security Tips
""",
        unsafe_allow_html=True,
    )

    tips = [

        "Use a unique password for every account.",

        "Enable Multi-Factor Authentication (MFA).",

        "Store passwords securely in Password Vault.",

        "Avoid personal information such as names or birthdays.",

        "Update important passwords regularly.",

        "Never reuse passwords across different websites.",

    ]

    for tip in tips:

        st.info(tip)