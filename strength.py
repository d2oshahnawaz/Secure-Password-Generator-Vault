# =====================================================
# PASSWORD STRENGTH
# Version 5.0 Professional
# =====================================================

from __future__ import annotations

from typing import Dict, Final, List

# =====================================================
# ZXCVBN IMPORT
# =====================================================

try:

    from zxcvbn import zxcvbn

    ZXCVBN_AVAILABLE: Final[bool] = True

except ImportError:

    ZXCVBN_AVAILABLE = False

    def zxcvbn(password: str) -> Dict[str, int]:
        """
        Lightweight fallback estimator.
        Returns a score between 0 and 4.
        """

        score = 0

        if len(password) >= 8:
            score += 1

        if len(password) >= 12:
            score += 1

        if any(c.islower() for c in password) and any(
            c.isupper() for c in password
        ):
            score += 1

        if any(c.isdigit() for c in password):
            score += 1

        if any(not c.isalnum() for c in password):
            score += 1

        return {
            "score": min(score, 4)
        }

# =====================================================
# CONSTANTS
# =====================================================

STRENGTH_LABELS: Final[Dict[int, str]] = {

    0: "Very Weak",

    1: "Weak",

    2: "Medium",

    3: "Strong",

    4: "Very Strong",

}

STRENGTH_COLORS: Final[Dict[int, str]] = {

    0: "#DC2626",

    1: "#F97316",

    2: "#EAB308",

    3: "#2563EB",

    4: "#16A34A",

}

# =====================================================
# CHECK STRENGTH
# =====================================================

def check_strength(
    password: str,
) -> Dict[str, object]:
    """
    Analyze password strength.
    """

    result = zxcvbn(password)

    score = int(
        result.get(
            "score",
            0,
        )
    )

    score = max(
        0,
        min(score, 4),
    )

    return {

        "score": score,

        "label": STRENGTH_LABELS[score],

        "color": STRENGTH_COLORS[score],

        "percentage": (score + 1) * 20,

    }

# =====================================================
# HELPER
# =====================================================

def is_strong_password(
    password: str,
) -> bool:
    """
    Return True if password is Strong or Very Strong.
    """

    return check_strength(password)["score"] >= 3

# =====================================================
# RECOMMENDATIONS
# =====================================================

def strength_recommendations(
    password: str,
) -> List[str]:
    """
    Return strength improvement suggestions.
    """

    recommendations: List[str] = []

    if len(password) < 12:
        recommendations.append(
            "Increase password length to at least 12 characters."
        )

    if not any(c.isupper() for c in password):
        recommendations.append(
            "Include uppercase letters."
        )

    if not any(c.islower() for c in password):
        recommendations.append(
            "Include lowercase letters."
        )

    if not any(c.isdigit() for c in password):
        recommendations.append(
            "Include numeric digits."
        )

    if not any(not c.isalnum() for c in password):
        recommendations.append(
            "Include special characters."
        )

    if not recommendations:
        recommendations.append(
            "Password follows recommended strength guidelines."
        )

    return recommendations

# =====================================================
# COMPLETE REPORT
# =====================================================

def strength_report(
    password: str,
) -> Dict[str, object]:
    """
    Return detailed strength report.
    """

    result = check_strength(password)

    return {

        "score": result["score"],

        "label": result["label"],

        "color": result["color"],

        "percentage": result["percentage"],

        "strong": result["score"] >= 3,

        "recommendations":
            strength_recommendations(password),

    }

# =====================================================
# INFORMATION
# =====================================================

def strength_info() -> Dict[str, object]:
    """
    Return module information.
    """

    return {

        "library":
            "zxcvbn"
            if ZXCVBN_AVAILABLE
            else "fallback",

        "max_score": 4,

        "levels":
            list(STRENGTH_LABELS.values()),

        "colors":
            STRENGTH_COLORS,

    }

# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    passwords = [

        "123456",

        "Password",

        "Password123",

        "Password@123",

        "Mohd@Secure#2026",

    ]

    print("=" * 60)

    print("Password Strength Test")

    print("=" * 60)

    for password in passwords:

        report = strength_report(password)

        print(

            f"{password:<22}"

            f" Score: {report['score']}"

            f"  Label: {report['label']}"

            f"  Strong: {report['strong']}"

        )

    print()

    print(strength_info())

    print("=" * 60)