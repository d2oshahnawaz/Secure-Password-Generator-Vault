# =====================================================
# PASSWORD SCORE
# Version 4.0 Professional
# =====================================================

from __future__ import annotations

from typing import Final

import streamlit as st

from health import password_health

# =====================================================
# CONSTANTS
# =====================================================

MAX_SCORE: Final[int] = 100

LENGTH_WEIGHT: Final[int] = 20
CHARACTER_WEIGHT: Final[int] = 40
ENTROPY_WEIGHT: Final[int] = 20
DIVERSITY_WEIGHT: Final[int] = 10
SECURITY_WEIGHT: Final[int] = 10

# =====================================================
# CALCULATE SCORE
# =====================================================

def calculate_score(
    password: str,
    entropy: float
) -> int:
    """
    Calculate password security score.

    Returns
    -------
    int
        Score between 0 and 100.
    """

    report = password_health(password)

    score = 0

    # -------------------------------------------------
    # Password Length (20)
    # -------------------------------------------------

    length = len(password)

    if length >= 16:

        score += LENGTH_WEIGHT

    elif length >= 12:

        score += 15

    elif length >= 10:

        score += 10

    else:

        score += 5

    # -------------------------------------------------
    # Character Categories (40)
    # -------------------------------------------------

    if report["uppercase"]:

        score += 10

    if report["lowercase"]:

        score += 10

    if report["numbers"]:

        score += 10

    if report["symbols"]:

        score += 10

    # -------------------------------------------------
    # Entropy (20)
    # -------------------------------------------------

    if entropy >= 80:

        score += ENTROPY_WEIGHT

    elif entropy >= 60:

        score += 15

    elif entropy >= 40:

        score += 10

    else:

        score += 5

    # -------------------------------------------------
    # Diversity Bonus (10)
    # -------------------------------------------------

    if (

        report["uppercase"]

        and report["lowercase"]

        and report["numbers"]

        and report["symbols"]

    ):

        score += DIVERSITY_WEIGHT

    # -------------------------------------------------
    # Security Bonus (10)
    # -------------------------------------------------

    if (

        not report["sequential"]

        and not report["repeated"]

        and not report["common"]

        and not report["spaces"]

    ):

        score += SECURITY_WEIGHT

    return min(score, MAX_SCORE)

# =====================================================
# SCORE LABEL
# =====================================================

def get_score_label(
    score: int
) -> tuple[str, str]:
    """
    Return score label and status.
    """

    if score >= 95:

        return (
            "Excellent (★★★★★)",
            "success",
        )

    if score >= 85:

        return (
            "Very Strong (★★★★☆)",
            "success",
        )

    if score >= 70:

        return (
            "Strong (★★★☆☆)",
            "info",
        )

    if score >= 55:

        return (
            "Moderate (★★☆☆☆)",
            "warning",
        )

    if score >= 35:

        return (
            "Weak (★☆☆☆☆)",
            "warning",
        )

    return (

        "Very Weak (☆☆☆☆☆)",

        "error",

    )

# =====================================================
# SHOW SCORE
# =====================================================

def show_score(
    password: str,
    entropy: float
) -> None:
    """
    Display password score.
    """

    score = calculate_score(
        password,
        entropy,
    )

    st.markdown(
        """
### <i class="bi bi-award-fill"></i> Password Security Score
""",
        unsafe_allow_html=True,
    )

    st.progress(score / MAX_SCORE)

    st.metric(

        "Overall Score",

        f"{score}/{MAX_SCORE}",

    )

    label, status = get_score_label(
        score
    )

    if status == "success":

        st.success(label)

    elif status == "info":

        st.info(label)

    elif status == "warning":

        st.warning(label)

    else:

        st.error(label)