# =====================================================
# PASSWORD RECOMMENDATIONS
# Version 4.0 Professional
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

SPECIAL_CHARACTERS = "@#$%&*+"

# =====================================================
# GET RECOMMENDATIONS
# =====================================================

def get_recommendations(
    password: str,
    entropy: float
) -> List[str]:
    """
    Generate security recommendations
    based on password health and score.
    """

    report = password_health(password)

    score = calculate_score(
        password,
        entropy
    )

    recommendations: List[str] = []

    # -------------------------------------------------
    # Length
    # -------------------------------------------------

    if len(password) < MIN_PASSWORD_LENGTH:

        recommendations.append(
            f"Increase the password length to at least {MIN_PASSWORD_LENGTH} characters."
        )

    # -------------------------------------------------
    # Character Categories
    # -------------------------------------------------

    if not report["uppercase"]:

        recommendations.append(
            "Add at least one uppercase letter (A-Z)."
        )

    if not report["lowercase"]:

        recommendations.append(
            "Add at least one lowercase letter (a-z)."
        )

    if not report["numbers"]:

        recommendations.append(
            "Include at least one numeric digit (0-9)."
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
            "Remove spaces from the password."
        )

    # -------------------------------------------------
    # Overall Assessment
    # -------------------------------------------------

    if score >= 95:

        recommendations.append(
            "Excellent! Your password follows modern security best practices."
        )

    elif score >= 80:

        recommendations.append(
            "Strong password. Minor improvements could make it even stronger."
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
    entropy: float
) -> None:
    """
    Display password recommendations.
    """

    st.markdown(
        """
### <i class="bi bi-lightbulb-fill"></i> Password Recommendations
""",
        unsafe_allow_html=True,
    )

    recommendations = get_recommendations(
        password,
        entropy,
    )

    for recommendation in recommendations:

        if recommendation.startswith("Excellent"):

            st.success(recommendation)

        elif recommendation.startswith("Strong"):

            st.info(recommendation)

        elif recommendation.startswith("Good"):

            st.info(recommendation)

        else:

            st.warning(recommendation)