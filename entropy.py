# =====================================================
# PASSWORD ENTROPY CALCULATOR
# Version 5.0 Professional
# =====================================================

from __future__ import annotations

import math
from typing import Dict

# =====================================================
# CHARACTER SET SIZES
# =====================================================

LOWERCASE = 26
UPPERCASE = 26
DIGITS = 10
SYMBOLS = 32

# =====================================================
# CHARACTER SET SIZE
# =====================================================

def character_set_size(password: str) -> int:
    """
    Calculate the effective character set size.
    """

    if not password:
        return 0

    charset = 0

    if any(ch.islower() for ch in password):
        charset += LOWERCASE

    if any(ch.isupper() for ch in password):
        charset += UPPERCASE

    if any(ch.isdigit() for ch in password):
        charset += DIGITS

    if any(not ch.isalnum() for ch in password):
        charset += SYMBOLS

    return charset


# =====================================================
# PASSWORD ENTROPY
# =====================================================

def calculate_entropy(password: str) -> float:
    """
    Calculate password entropy in bits.

    Formula:
        Entropy = Length × log2(Character Set Size)
    """

    if not password:
        return 0.0

    charset = character_set_size(password)

    if charset == 0:
        return 0.0

    entropy = len(password) * math.log2(charset)

    return round(entropy, 2)


# =====================================================
# SECURITY LEVEL
# =====================================================

def entropy_level(entropy: float) -> str:
    """
    Return entropy classification.
    """

    if entropy < 28:
        return "Very Weak"

    elif entropy < 36:
        return "Weak"

    elif entropy < 60:
        return "Moderate"

    elif entropy < 80:
        return "Strong"

    elif entropy < 100:
        return "Very Strong"

    return "Excellent"


# =====================================================
# PASSWORD STATISTICS
# =====================================================

def password_statistics(password: str) -> Dict[str, int]:
    """
    Return character statistics.
    """

    return {

        "length": len(password),

        "lowercase": sum(
            ch.islower()
            for ch in password
        ),

        "uppercase": sum(
            ch.isupper()
            for ch in password
        ),

        "digits": sum(
            ch.isdigit()
            for ch in password
        ),

        "symbols": sum(
            not ch.isalnum()
            for ch in password
        ),

    }


# =====================================================
# ENTROPY REPORT
# =====================================================

def entropy_report(password: str) -> Dict:
    """
    Generate a complete entropy report.
    """

    entropy = calculate_entropy(password)

    return {

        "password": password,

        "length": len(password),

        "charset_size": character_set_size(password),

        "entropy": entropy,

        "security_level": entropy_level(entropy),

        "statistics": password_statistics(password),

    }


# =====================================================
# SECURITY SCORE
# =====================================================

def entropy_score(password: str) -> int:
    """
    Return entropy score (0-100).
    """

    entropy = calculate_entropy(password)

    score = int(min(entropy / 128 * 100, 100))

    return max(score, 0)


# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    passwords = [

        "password",

        "Password123",

        "Mohd@1234",

        "A@8kLp#2026",

        "",

    ]

    print("=" * 60)

    print("Password Entropy Test")

    print("=" * 60)

    for pwd in passwords:

        report = entropy_report(pwd)

        print(f"\nPassword : {pwd!r}")

        print(f"Length   : {report['length']}")

        print(f"Charset  : {report['charset_size']}")

        print(f"Entropy  : {report['entropy']} bits")

        print(f"Level    : {report['security_level']}")

        print(f"Score    : {entropy_score(pwd)}/100")

    print("=" * 60)