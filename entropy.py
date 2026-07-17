# =====================================================
# PASSWORD ENTROPY CALCULATOR
# Version 4.0 Professional
# =====================================================

import math

# =====================================================
# CHARACTER SET SIZES
# =====================================================

LOWERCASE = 26
UPPERCASE = 26
DIGITS = 10
SYMBOLS = 32

# =====================================================
# ENTROPY CALCULATOR
# =====================================================

def calculate_entropy(password: str) -> float:
    """
    Calculate password entropy in bits.

    Formula:
        Entropy = Length × log2(Character Set Size)

    Parameters
    ----------
    password : str

    Returns
    -------
    float
        Password entropy (bits).
    """

    if not password:
        return 0.0

    charset = 0

    # Lowercase

    if any(ch.islower() for ch in password):
        charset += LOWERCASE

    # Uppercase

    if any(ch.isupper() for ch in password):
        charset += UPPERCASE

    # Numbers

    if any(ch.isdigit() for ch in password):
        charset += DIGITS

    # Symbols

    if any(not ch.isalnum() for ch in password):
        charset += SYMBOLS

    if charset == 0:
        return 0.0

    entropy = len(password) * math.log2(charset)

    return round(entropy, 2)


# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    passwords = [

        "password",

        "Password123",

        "Mohd@1234",

        "A@8kLp#2026",

        ""

    ]

    print("-" * 50)

    print("Password Entropy Test")

    print("-" * 50)

    for pwd in passwords:

        print(

            f"{pwd!r:<20}"

            f" -> "

            f"{calculate_entropy(pwd)} bits"

        )

    print("-" * 50)