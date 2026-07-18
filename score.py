# =====================================================
# PASSWORD SCORE
# Version 5.0 Professional
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
    entropy: float,
) -> int:
    """
    Calculate password security score (0-100).
    """

    report = password_health(password)

    score = 0

    # =================================================
    # LENGTH
    # =================================================

    length = len(password)

    if length >= 20:
        score += LENGTH_WEIGHT

    elif length >= 16:
        score += 18

    elif length >= 12:
        score += 15

    elif length >= 10:
        score += 10

    else:
        score += 5

    # =================================================
    # CHARACTER TYPES
    # =================================================

    if report["uppercase"]:
        score += 10

    if report["lowercase"]:
        score += 10

    if report["numbers"]:
        score += 10

    if report["symbols"]:
        score += 10

    # =================================================
    # ENTROPY
    # =================================================

    if entropy >= 100:
        score += ENTROPY_WEIGHT

    elif entropy >= 80:
        score += 18

    elif entropy >= 60:
        score += 15

    elif entropy >= 40:
        score += 10

    else:
        score += 5

    # =================================================
    # DIVERSITY BONUS
    # =================================================

    if (
        report["uppercase"]
        and report["lowercase"]
        and report["numbers"]
        and report["symbols"]
    ):
        score += DIVERSITY_WEIGHT

    # =================================================
    # SECURITY BONUS
    # =================================================

    if (
        not report["spaces"]
        and not report["common"]
        and not report["repeated"]
        and not report["sequential"]
    ):
        score += SECURITY_WEIGHT

    return min(score, MAX_SCORE)

# =====================================================
# SCORE LABEL
# =====================================================

def get_score_label(score: int) -> tuple[str, str]:

    if score >= 95:
        return "Excellent", "success"

    elif score >= 85:
        return "Very Strong", "success"

    elif score >= 70:
        return "Strong", "info"

    elif score >= 55:
        return "Moderate", "warning"

    elif score >= 35:
        return "Weak", "warning"

    return "Very Weak", "error"

# =====================================================
# SCORE COLOR
# =====================================================

def score_color(score: int) -> str:

    if score >= 95:
        return "#16A34A"

    elif score >= 85:
        return "#22C55E"

    elif score >= 70:
        return "#2563EB"

    elif score >= 55:
        return "#D97706"

    elif score >= 35:
        return "#EA580C"

    return "#DC2626"

# =====================================================
# SCORE BREAKDOWN
# =====================================================

def score_breakdown(
    password: str,
    entropy: float,
) -> dict:

    report = password_health(password)

    return {

        "Length": len(password),

        "Entropy": round(entropy, 2),

        "Uppercase": report["uppercase"],

        "Lowercase": report["lowercase"],

        "Numbers": report["numbers"],

        "Symbols": report["symbols"],

        "Sequential": report["sequential"],

        "Repeated": report["repeated"],

        "Common": report["common"],

        "Spaces": report["spaces"],

    }

# =====================================================
# SHOW SCORE
# =====================================================

def show_score(
    password: str,
    entropy: float,
) -> None:
    """
    Display password score.
    """

    score = calculate_score(
        password,
        entropy,
    )

    label, status = get_score_label(score)

    st.markdown(
        """
### <i class="bi bi-award-fill"></i>
Password Security Score
""",
        unsafe_allow_html=True,
    )

    st.progress(score / MAX_SCORE)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Overall Score",
            f"{score}/{MAX_SCORE}",
        )

    with col2:

        st.metric(
            "Rating",
            label,
        )

    if status == "success":
        st.success(label)

    elif status == "info":
        st.info(label)

    elif status == "warning":
        st.warning(label)

    else:
        st.error(label)

    st.divider()

    st.markdown(
        """
#### <i class="bi bi-bar-chart-fill"></i>
Score Breakdown
""",
        unsafe_allow_html=True,
    )

    breakdown = score_breakdown(
        password,
        entropy,
    )

    for key, value in breakdown.items():

        st.write(f"**{key}:** {value}")

# =====================================================
# SCORE REPORT
# =====================================================

def score_report(
    password: str,
    entropy: float,
) -> dict:
    """
    Return complete score report.
    """

    score = calculate_score(
        password,
        entropy,
    )

    label, _ = get_score_label(score)

    return {

        "score": score,

        "max_score": MAX_SCORE,

        "rating": label,

        "color": score_color(score),

        "details": score_breakdown(
            password,
            entropy,
        ),

    }

# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    password = "Mohd@1234"

    entropy = 68.45

    print("=" * 60)

    print("Password Score Test")

    print("=" * 60)

    print(score_report(password, entropy))

    print("=" * 60)