# =====================================================
# PASSWORD GENERATOR
# Version 4.0 Professional
# =====================================================

# -----------------------------------------------------
# Standard Library
# -----------------------------------------------------

import secrets
import string
from typing import Dict, List

# -----------------------------------------------------
# Local Modules
# -----------------------------------------------------

import templates

# =====================================================
# CONSTANTS
# =====================================================

DEFAULT_LETTERS = "User"

DEFAULT_NUMBERS = "123"

SPECIAL_CHARACTERS = "@#$%&*+"

SIMILAR_CHARACTERS = "O0Il1"

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def extract_letters(text: str) -> str:
    """
    Extract alphabetic characters.
    """

    return "".join(

        character

        for character in text

        if character.isalpha()

    )


def extract_numbers(text: str) -> str:
    """
    Extract numeric characters.
    """

    return "".join(

        character

        for character in text

        if character.isdigit()

    )


# =====================================================
# PASSWORD LENGTH
# =====================================================

def make_password_length(
    password: str,
    length: int,
    charset: str
) -> str:
    """
    Extend password until required length.
    """

    while len(password) < length:

        password += secrets.choice(charset)

    return password[:length]


# =====================================================
# REMOVE EXCLUDED CHARACTERS
# =====================================================

def remove_excluded(
    text: str,
    excluded: str
) -> str:
    """
    Remove excluded characters.
    """

    if not excluded:

        return text

    return "".join(

        character

        for character in text

        if character not in excluded

    )


# =====================================================
# PASSWORD STATISTICS
# =====================================================

def password_stats(password: str) -> Dict[str, int]:
    """
    Return password statistics.
    """

    return {

        "length": len(password),

        "uppercase": sum(

            character.isupper()

            for character in password

        ),

        "lowercase": sum(

            character.islower()

            for character in password

        ),

        "digits": sum(

            character.isdigit()

            for character in password

        ),

        "special": sum(

            not character.isalnum()

            for character in password

        ),

    }


# =====================================================
# CHARACTER SET
# =====================================================

def build_charset(
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
    avoid_similar: bool,
    exclude_chars: str
) -> str:
    """
    Build character set.
    """

    charset = ""

    if use_upper:

        charset += string.ascii_uppercase

    if use_lower:

        charset += string.ascii_lowercase

    if use_numbers:

        charset += string.digits

    if use_symbols:

        charset += SPECIAL_CHARACTERS

    if not charset:

        charset = (

            string.ascii_letters

            + string.digits

        )

    if avoid_similar:

        charset = "".join(

            character

            for character in charset

            if character not in SIMILAR_CHARACTERS

        )

    charset = remove_excluded(

        charset,

        exclude_chars

    )

    return charset

# =====================================================
# BASE PASSWORD
# =====================================================

def build_base_password(
    user_input: str,
    extra_letters: str,
    extra_numbers: str
) -> str:
    """
    Build base password from user input.
    """

    letters = extract_letters(user_input)

    numbers = extract_numbers(user_input)

    if not letters:

        letters = (

            extra_letters.strip()

            if extra_letters.strip()

            else DEFAULT_LETTERS

        )

    if not numbers:

        numbers = (

            extra_numbers.strip()

            if extra_numbers.strip()

            else DEFAULT_NUMBERS

        )

    return letters.capitalize() + numbers


# =====================================================
# TEMPLATE SELECTION
# =====================================================

def get_template_passwords(
    base_password: str,
    template_type: str,
    memorable: bool
) -> List[str]:
    """
    Return template passwords.
    """

    if memorable:

        return templates.memorable(
            base_password
        )

    return templates.get_template(

        template_type,

        base_password,

    )


# =====================================================
# ENSURE CHARACTER TYPES
# =====================================================

def ensure_character_types(
    password: str,
    charset: str,
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool
) -> str:
    """
    Ensure password contains all
    selected character categories.
    """

    characters = list(password)

    if use_upper and not any(
        c.isupper()
        for c in characters
    ):

        characters.append(

            secrets.choice(
                string.ascii_uppercase
            )

        )

    if use_lower and not any(
        c.islower()
        for c in characters
    ):

        characters.append(

            secrets.choice(
                string.ascii_lowercase
            )

        )

    if use_numbers and not any(
        c.isdigit()
        for c in characters
    ):

        characters.append(

            secrets.choice(
                string.digits
            )

        )

    if use_symbols and not any(
        not c.isalnum()
        for c in characters
    ):

        characters.append(

            secrets.choice(
                SPECIAL_CHARACTERS
            )

        )

    # ---------------------------------------------
    # Shuffle securely
    # ---------------------------------------------

    secrets.SystemRandom().shuffle(
        characters
    )

    password = "".join(
        characters
    )

    password = make_password_length(

        password,

        max(
            len(password),
            len(characters)
        ),

        charset

    )

    return password


# =====================================================
# FINAL CLEANUP
# =====================================================

def clean_password(
    password: str,
    avoid_similar: bool,
    exclude_chars: str
) -> str:
    """
    Final password cleanup.
    """

    password = remove_excluded(

        password,

        exclude_chars

    )

    if avoid_similar:

        translation = str.maketrans({

            "O": "Q",

            "o": "a",

            "I": "X",

            "l": "L",

            "0": "8",

            "1": "7"

        })

        password = password.translate(
            translation
        )

    return password

# =====================================================
# PASSWORD GENERATOR
# =====================================================

def generate_passwords(
    user_input: str,
    extra_letters: str,
    extra_numbers: str,
    length: int,
    count: int,
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
    avoid_similar: bool,
    exclude_chars: str,
    template_type: str = "Personal",
    memorable: bool = False
) -> List[str]:
    """
    Generate multiple secure passwords.

    Returns
    -------
    List[str]
        List of generated passwords.
    """

    # -------------------------------------------------
    # Minimum Password Length
    # -------------------------------------------------

    length = max(length, 8)

    # -------------------------------------------------
    # Character Set
    # -------------------------------------------------

    charset = build_charset(

        use_upper,

        use_lower,

        use_numbers,

        use_symbols,

        avoid_similar,

        exclude_chars

    )

    if not charset:

        charset = (

            string.ascii_letters

            + string.digits

            + SPECIAL_CHARACTERS

        )

    # -------------------------------------------------
    # Base Password
    # -------------------------------------------------

    base_password = build_base_password(

        user_input,

        extra_letters,

        extra_numbers

    )

    # -------------------------------------------------
    # Template Passwords
    # -------------------------------------------------

    template_passwords = get_template_passwords(

        base_password,

        template_type,

        memorable

    )

    # -------------------------------------------------
    # Final Password List
    # -------------------------------------------------

    final_passwords: List[str] = []

    attempts = 0

    maximum_attempts = max(

        100,

        count * 20

    )

    # -------------------------------------------------
    # Generate Passwords
    # -------------------------------------------------

    while (

        len(final_passwords) < count

        and attempts < maximum_attempts

    ):

        attempts += 1

        password = secrets.choice(

            template_passwords

        )

        # ---------------------------------------------
        # Cleanup
        # ---------------------------------------------

        password = clean_password(

            password,

            avoid_similar,

            exclude_chars

        )

        # ---------------------------------------------
        # Required Character Types
        # ---------------------------------------------

        password = ensure_character_types(

            password,

            charset,

            use_upper,

            use_lower,

            use_numbers,

            use_symbols

        )

        # ---------------------------------------------
        # Required Length
        # ---------------------------------------------

        password = make_password_length(

            password,

            length,

            charset

        )

        # ---------------------------------------------
        # Secure Shuffle
        # ---------------------------------------------

        characters = list(password)

        secrets.SystemRandom().shuffle(

            characters

        )

        password = "".join(

            characters

        )

        password = password[:length]

        # ---------------------------------------------
        # Avoid Duplicate Passwords
        # ---------------------------------------------

        if password not in final_passwords:

            final_passwords.append(

                password

            )

    # -------------------------------------------------
    # Fallback
    # -------------------------------------------------

    while len(final_passwords) < count:

        random_password = "".join(

            secrets.choice(charset)

            for _ in range(length)

        )

        if random_password not in final_passwords:

            final_passwords.append(

                random_password

            )

    return final_passwords

# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print(" Smart Password Generator - Version 4.0 Professional")
    print("=" * 60)

    passwords = generate_passwords(

        user_input="Mohd123",

        extra_letters="",

        extra_numbers="",

        length=16,

        count=5,

        use_upper=True,

        use_lower=True,

        use_numbers=True,

        use_symbols=True,

        avoid_similar=False,

        exclude_chars="",

        template_type="Developer",

        memorable=False

    )

    print("\nGenerated Passwords\n")

    for index, password in enumerate(passwords, start=1):

        print(f"{index}. {password}")

        stats = password_stats(password)

        print(
            f"   Length     : {stats['length']}"
        )

        print(
            f"   Uppercase  : {stats['uppercase']}"
        )

        print(
            f"   Lowercase  : {stats['lowercase']}"
        )

        print(
            f"   Digits     : {stats['digits']}"
        )

        print(
            f"   Symbols    : {stats['special']}"
        )

        print("-" * 40)

    print("\nGenerator Test Completed Successfully.")

    print("=" * 60)