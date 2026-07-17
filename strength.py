# =====================================================
# PASSWORD STRENGTH
# Version 4.0 Professional
# =====================================================

from __future__ import annotations

from typing import Dict, Final

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
        Lightweight fallback strength estimator.
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

# =====================================================
# STRENGTH CHECK
# =====================================================

def check_strength(
    password: str
) -> Dict[str, object]:
    """
    Analyze password strength.

    Returns
    -------
    dict
        score : int
        label : str
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

        min(

            score,

            4,

        ),

    )

    return {

        "score": score,

        "label": STRENGTH_LABELS[score],

    }

# =====================================================
# HELPER
# =====================================================

def is_strong_password(
    password: str
) -> bool:
    """
    Return True if password is
    Strong or Very Strong.
    """

    return (

        check_strength(

            password

        )["score"]

        >= 3

    )

# =====================================================
# INFORMATION
# =====================================================

def strength_info() -> Dict[str, object]:
    """
    Return module information.
    """

    return {

        "library": (

            "zxcvbn"

            if ZXCVBN_AVAILABLE

            else "fallback"

        ),

        "max_score": 4,

        "levels": list(

            STRENGTH_LABELS.values()

        ),

    }

# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    samples = [

        "123456",

        "Password",

        "Password123",

        "Password@123",

        "Mohd@Secure#2026",

    ]

    print("=" * 60)

    print("Password Strength Test")

    print("=" * 60)

    for password in samples:

        result = check_strength(password)

        print(

            f"{password:<22}"

            f" Score: {result['score']}"

            f"  Label: {result['label']}"

        )

    print()

    print(strength_info())

    print("=" * 60)