# =====================================================
# PASSWORD GENERATOR
# Version 5.0 Professional
# Part 1/4
# =====================================================

from __future__ import annotations

# -----------------------------------------------------
# Standard Library
# -----------------------------------------------------

import secrets
import string
from typing import Dict
from typing import Final
from typing import List

# -----------------------------------------------------
# Local Modules
# -----------------------------------------------------

import templates

# =====================================================
# CONSTANTS
# =====================================================

DEFAULT_LETTERS: Final[str] = "User"

DEFAULT_NUMBERS: Final[str] = "123"

DEFAULT_LENGTH: Final[int] = 16

MIN_PASSWORD_LENGTH: Final[int] = 8

MAX_PASSWORD_LENGTH: Final[int] = 128

DEFAULT_COUNT: Final[int] = 10

MAX_PASSWORD_COUNT: Final[int] = 100

SPECIAL_CHARACTERS: Final[str] = (
    "@#$%&*+-_=!?~"
)

SIMILAR_CHARACTERS: Final[str] = (
    "O0oIl1|"
)

UPPERCASE: Final[str] = (
    string.ascii_uppercase
)

LOWERCASE: Final[str] = (
    string.ascii_lowercase
)

DIGITS: Final[str] = (
    string.digits
)

# =====================================================
# INPUT HELPERS
# =====================================================

def sanitize_text(
    text: str,
) -> str:
    """
    Remove leading/trailing spaces.
    """

    return text.strip()


# -----------------------------------------------------

def extract_letters(
    text: str,
) -> str:
    """
    Extract alphabetic characters.
    """

    return "".join(

        character

        for character in sanitize_text(text)

        if character.isalpha()

    )


# -----------------------------------------------------

def extract_numbers(
    text: str,
) -> str:
    """
    Extract numeric characters.
    """

    return "".join(

        character

        for character in sanitize_text(text)

        if character.isdigit()

    )


# =====================================================
# VALIDATION
# =====================================================

def validate_length(
    length: int,
) -> int:
    """
    Validate password length.
    """

    return max(

        MIN_PASSWORD_LENGTH,

        min(

            length,

            MAX_PASSWORD_LENGTH,

        ),

    )


# -----------------------------------------------------

def validate_count(
    count: int,
) -> int:
    """
    Validate password count.
    """

    return max(

        1,

        min(

            count,

            MAX_PASSWORD_COUNT,

        ),

    )


# -----------------------------------------------------

def validate_charset(
    charset: str,
) -> str:
    """
    Ensure charset is usable.
    """

    if charset:

        return "".join(

            sorted(set(charset))

        )

    return (

        UPPERCASE

        + LOWERCASE

        + DIGITS

        + SPECIAL_CHARACTERS

    )


# =====================================================
# CHARACTER HELPERS
# =====================================================

def remove_excluded(
    text: str,
    excluded: str,
) -> str:
    """
    Remove excluded characters.
    """

    if not excluded:

        return text

    excluded = set(excluded)

    return "".join(

        character

        for character in text

        if character not in excluded

    )


# -----------------------------------------------------

def remove_similar(
    text: str,
) -> str:
    """
    Remove visually similar characters.
    """

    return "".join(

        character

        for character in text

        if character not in SIMILAR_CHARACTERS

    )


# =====================================================
# CHARACTER SET
# =====================================================

def build_charset(
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
    avoid_similar: bool,
    exclude_chars: str,
) -> str:
    """
    Build secure character set.
    """

    charset = ""

    if use_upper:

        charset += UPPERCASE

    if use_lower:

        charset += LOWERCASE

    if use_numbers:

        charset += DIGITS

    if use_symbols:

        charset += SPECIAL_CHARACTERS

    if not charset:

        charset = (

            UPPERCASE

            + LOWERCASE

            + DIGITS

        )

    if avoid_similar:

        charset = remove_similar(
            charset
        )

    charset = remove_excluded(

        charset,

        exclude_chars,

    )

    return validate_charset(
        charset
    )


# =====================================================
# PASSWORD HELPERS
# =====================================================

def make_password_length(
    password: str,
    length: int,
    charset: str,
) -> str:
    """
    Extend password to required length.
    """

    while len(password) < length:

        password += secrets.choice(
            charset
        )

    return password[:length]


# -----------------------------------------------------

def secure_shuffle(
    password: str,
) -> str:
    """
    Cryptographically secure shuffle.
    """

    characters = list(password)

    secrets.SystemRandom().shuffle(
        characters
    )

    return "".join(
        characters
    )


# =====================================================
# PASSWORD STATISTICS
# =====================================================

def password_stats(
    password: str,
) -> Dict[str, int]:
    """
    Return password statistics.
    """

    return {

        "length":
            len(password),

        "uppercase":
            sum(

                c.isupper()

                for c in password

            ),

        "lowercase":
            sum(

                c.islower()

                for c in password

            ),

        "digits":
            sum(

                c.isdigit()

                for c in password

            ),

        "special":
            sum(

                not c.isalnum()

                for c in password

            ),

        "unique":
            len(set(password)),

    }


# =====================================================
# MODULE INFORMATION
# =====================================================

GENERATOR_VERSION: Final[str] = (
    "5.0 Professional"
)

# =====================================================
# BASE PASSWORD BUILDER
# Version 5.0 Professional
# Part 2/4
# =====================================================

def build_base_password(
    user_input: str,
    extra_letters: str,
    extra_numbers: str,
) -> str:
    """
    Build a meaningful base password from
    user supplied data.
    """

    letters = extract_letters(
        user_input
    )

    numbers = extract_numbers(
        user_input
    )

    if not letters:

        letters = sanitize_text(
            extra_letters
        )

    if not letters:

        letters = DEFAULT_LETTERS

    if not numbers:

        numbers = sanitize_text(
            extra_numbers
        )

    if not numbers:

        numbers = DEFAULT_NUMBERS

    return letters.capitalize() + numbers


# =====================================================
# TEMPLATE PASSWORDS
# =====================================================

def get_template_passwords(
    base_password: str,
    template_name: str,
    memorable: bool,
) -> List[str]:
    """
    Generate template-based passwords.
    """

    if memorable:

        return templates.memorable(
            base_password
        )

    return templates.get_template(

        template_name,

        base_password,

    )


# =====================================================
# PASSWORD CLEANUP
# =====================================================

def clean_password(
    password: str,
    avoid_similar: bool,
    exclude_chars: str,
) -> str:
    """
    Clean generated password.
    """

    password = remove_excluded(

        password,

        exclude_chars,

    )

    if avoid_similar:

        translation = str.maketrans({

            "O": "Q",

            "o": "a",

            "0": "8",

            "I": "X",

            "l": "L",

            "1": "7",

            "|": "!",

        })

        password = password.translate(
            translation
        )

    return password


# =====================================================
# CHARACTER BALANCING
# =====================================================

def ensure_character_types(
    password: str,
    charset: str,
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
) -> str:
    """
    Ensure all requested character
    categories are present.
    """

    characters = list(password)

    if use_upper and not any(
        c.isupper()
        for c in characters
    ):

        characters.append(

            secrets.choice(
                UPPERCASE
            )

        )

    if use_lower and not any(
        c.islower()
        for c in characters
    ):

        characters.append(

            secrets.choice(
                LOWERCASE
            )

        )

    if use_numbers and not any(
        c.isdigit()
        for c in characters
    ):

        characters.append(

            secrets.choice(
                DIGITS
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

    return secure_shuffle(
        "".join(characters)
    )


# =====================================================
# PASSWORD VALIDATOR
# =====================================================

def validate_password(
    password: str,
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
) -> bool:
    """
    Validate generated password.
    """

    if use_upper and not any(
        c.isupper()
        for c in password
    ):
        return False

    if use_lower and not any(
        c.islower()
        for c in password
    ):
        return False

    if use_numbers and not any(
        c.isdigit()
        for c in password
    ):
        return False

    if use_symbols and not any(
        not c.isalnum()
        for c in password
    ):
        return False

    return True


# =====================================================
# PASSWORD OPTIMIZER
# =====================================================

def optimize_password(
    password: str,
    length: int,
    charset: str,
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
) -> str:
    """
    Optimize password before returning.
    """

    password = ensure_character_types(

        password,

        charset,

        use_upper,

        use_lower,

        use_numbers,

        use_symbols,

    )

    password = make_password_length(

        password,

        length,

        charset,

    )

    password = secure_shuffle(
        password
    )

    return password[:length]


# =====================================================
# TEMPLATE INFORMATION
# =====================================================

def available_templates() -> List[str]:
    """
    Return available template names.
    """

    return templates.available_templates()


# =====================================================
# GENERATOR INFORMATION
# =====================================================

def supported_charsets() -> Dict[str, str]:
    """
    Return supported character sets.
    """

    return {

        "uppercase":
            UPPERCASE,

        "lowercase":
            LOWERCASE,

        "digits":
            DIGITS,

        "symbols":
            SPECIAL_CHARACTERS,

    }
    
    # =====================================================
# PASSWORD GENERATION ENGINE
# Version 5.0 Professional
# Part 3/4
# =====================================================

import math

# =====================================================
# ENTROPY ESTIMATION
# =====================================================

def estimate_entropy(
    password: str,
    charset_size: int,
) -> float:
    """
    Estimate password entropy (bits).
    """

    if not password or charset_size <= 1:
        return 0.0

    return round(
        len(password)
        * math.log2(charset_size),
        2,
    )


# =====================================================
# SINGLE PASSWORD
# =====================================================

def generate_password(
    user_input: str,
    extra_letters: str,
    extra_numbers: str,
    length: int,
    use_upper: bool,
    use_lower: bool,
    use_numbers: bool,
    use_symbols: bool,
    avoid_similar: bool,
    exclude_chars: str,
    template_name: str = "Personal",
    memorable: bool = False,
) -> str:
    """
    Generate one optimized password.
    """

    length = validate_length(length)

    charset = build_charset(

        use_upper,

        use_lower,

        use_numbers,

        use_symbols,

        avoid_similar,

        exclude_chars,

    )

    base_password = build_base_password(

        user_input,

        extra_letters,

        extra_numbers,

    )

    template_passwords = get_template_passwords(

        base_password,

        template_name,

        memorable,

    )

    password = secrets.choice(
        template_passwords
    )

    password = clean_password(

        password,

        avoid_similar,

        exclude_chars,

    )

    password = optimize_password(

        password,

        length,

        charset,

        use_upper,

        use_lower,

        use_numbers,

        use_symbols,

    )

    if not validate_password(

        password,

        use_upper,

        use_lower,

        use_numbers,

        use_symbols,

    ):

        return generate_password(

            user_input,

            extra_letters,

            extra_numbers,

            length,

            use_upper,

            use_lower,

            use_numbers,

            use_symbols,

            avoid_similar,

            exclude_chars,

            template_name,

            memorable,

        )

    return password


# =====================================================
# MULTIPLE PASSWORDS
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
    template_name: str = "Personal",
    memorable: bool = False,
) -> List[str]:
    """
    Generate multiple unique passwords.
    """

    length = validate_length(length)

    count = validate_count(count)

    generated: set[str] = set()

    attempts = 0

    max_attempts = max(

        count * 20,

        100,

    )

    while (

        len(generated) < count

        and attempts < max_attempts

    ):

        attempts += 1

        generated.add(

            generate_password(

                user_input,

                extra_letters,

                extra_numbers,

                length,

                use_upper,

                use_lower,

                use_numbers,

                use_symbols,

                avoid_similar,

                exclude_chars,

                template_name,

                memorable,

            )

        )

    charset = build_charset(

        use_upper,

        use_lower,

        use_numbers,

        use_symbols,

        avoid_similar,

        exclude_chars,

    )

    while len(generated) < count:

        fallback = "".join(

            secrets.choice(charset)

            for _ in range(length)

        )

        generated.add(

            secure_shuffle(fallback)

        )

    return sorted(generated)


# =====================================================
# GENERATOR STATISTICS
# =====================================================

def generator_statistics(
    passwords: List[str],
) -> Dict[str, object]:
    """
    Return statistics for generated passwords.
    """

    if not passwords:

        return {}

    charset_size = len(

        UPPERCASE

        + LOWERCASE

        + DIGITS

        + SPECIAL_CHARACTERS

    )

    entropy_values = [

        estimate_entropy(

            password,

            charset_size,

        )

        for password in passwords

    ]

    lengths = [

        len(password)

        for password in passwords

    ]

    return {

        "count":
            len(passwords),

        "minimum_length":
            min(lengths),

        "maximum_length":
            max(lengths),

        "average_length":
            round(

                sum(lengths)

                / len(lengths),

                2,

            ),

        "minimum_entropy":
            min(entropy_values),

        "maximum_entropy":
            max(entropy_values),

        "average_entropy":
            round(

                sum(entropy_values)

                / len(entropy_values),

                2,

            ),

        "duplicates":
            len(passwords)
            != len(set(passwords)),

    }


# =====================================================
# MODULE INFORMATION
# =====================================================

def generator_info() -> Dict[str, object]:
    """
    Return generator information.
    """

    return {

        "module":
            "generator",

        "version":
            GENERATOR_VERSION,

        "templates":
            len(
                available_templates()
            ),

        "default_length":
            DEFAULT_LENGTH,

        "minimum_length":
            MIN_PASSWORD_LENGTH,

        "maximum_length":
            MAX_PASSWORD_LENGTH,

        "maximum_passwords":
            MAX_PASSWORD_COUNT,

        "supported_charsets":
            list(
                supported_charsets().keys()
            ),

    }
    
    # =====================================================
# DIAGNOSTICS
# Version 5.0 Professional
# Part 4/4
# =====================================================

def diagnostics() -> Dict[str, object]:
    """
    Return generator diagnostics.
    """

    return {

        "module":
            "generator",

        "version":
            GENERATOR_VERSION,

        "status":
            "Healthy",

        "default_length":
            DEFAULT_LENGTH,

        "minimum_length":
            MIN_PASSWORD_LENGTH,

        "maximum_length":
            MAX_PASSWORD_LENGTH,

        "maximum_passwords":
            MAX_PASSWORD_COUNT,

        "templates":
            len(
                available_templates()
            ),

        "supported_charsets":
            len(
                supported_charsets()
            ),

    }


# =====================================================
# SELF TEST
# =====================================================

def run_self_test() -> bool:
    """
    Execute generator self-test.
    """

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

        template_name="Developer",

        memorable=False,

    )

    assert len(passwords) == 5

    assert len(set(passwords)) == 5

    for password in passwords:

        assert len(password) == 16

        assert validate_password(

            password,

            True,

            True,

            True,

            True,

        )

    stats = generator_statistics(
        passwords
    )

    assert stats["count"] == 5

    assert isinstance(
        diagnostics(),
        dict,
    )

    assert isinstance(
        generator_info(),
        dict,
    )

    return True


# =====================================================
# EXAMPLE USAGE
# =====================================================

def example_usage() -> None:
    """
    Demonstrate generator usage.
    """

    passwords = generate_passwords(

        user_input="Shahnawaz123",

        extra_letters="",

        extra_numbers="",

        length=18,

        count=5,

        use_upper=True,

        use_lower=True,

        use_numbers=True,

        use_symbols=True,

        avoid_similar=False,

        exclude_chars="",

        template_name="Developer",

        memorable=False,

    )

    print()

    print("Generated Passwords")

    print("-" * 60)

    for index, password in enumerate(

        passwords,

        start=1,

    ):

        entropy = estimate_entropy(

            password,

            len(

                UPPERCASE

                + LOWERCASE

                + DIGITS

                + SPECIAL_CHARACTERS

            ),

        )

        print(

            f"{index:>2}. {password}"

        )

        print(

            f"    Entropy : {entropy:.2f} bits"

        )

        print(

            f"    Stats    : {password_stats(password)}"

        )

        print()


# =====================================================
# PERFORMANCE BENCHMARK
# =====================================================

def benchmark() -> Dict[str, object]:
    """
    Lightweight benchmark.
    """

    passwords = generate_passwords(

        user_input="Benchmark",

        extra_letters="",

        extra_numbers="",

        length=20,

        count=100,

        use_upper=True,

        use_lower=True,

        use_numbers=True,

        use_symbols=True,

        avoid_similar=False,

        exclude_chars="",

        template_name="Personal",

        memorable=False,

    )

    return {

        "generated":
            len(passwords),

        "duplicates":
            len(passwords)
            != len(set(passwords)),

        "average_entropy":
            round(

                sum(

                    estimate_entropy(

                        p,

                        len(

                            UPPERCASE
                            + LOWERCASE
                            + DIGITS
                            + SPECIAL_CHARACTERS

                        ),

                    )

                    for p in passwords

                ) / len(passwords),

                2,

            ),

    }


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("=" * 70)

    print("Password Generator")

    print("Version 5.0 Professional")

    print("=" * 70)

    print()

    print("Generator Information")

    print("-" * 70)

    for key, value in generator_info().items():

        print(f"{key:<20}: {value}")

    print()

    example_usage()

    print("Generator Statistics")

    print("-" * 70)

    print(

        benchmark()

    )

    print()

    print("Diagnostics")

    print("-" * 70)

    print(

        diagnostics()

    )

    print()

    if run_self_test():

        print("✓ All tests passed successfully.")

    print("=" * 70)