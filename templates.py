# =====================================================
# PASSWORD TEMPLATES
# Version 4.1 Professional
# =====================================================

from __future__ import annotations

import secrets

from typing import Callable
from typing import Final
from typing import TypeAlias

# =====================================================
# TYPE DEFINITIONS
# =====================================================

TemplateFunction: TypeAlias = Callable[[str], list[str]]

# =====================================================
# CONSTANTS
# =====================================================

SPECIAL: Final[tuple[str, ...]] = (

    "@",

    "#",

    "$",

    "%",

    "&",

    "*",

    "+",

)

SUFFIXES: Final[tuple[str, ...]] = (

    "AI",

    "Secure",

    "Tech",

    "Dev",

    "Pro",

    "2026",

    "007",

    "786",

    "Login",

    "Official",

)

AI_SUFFIXES: Final[tuple[str, ...]] = (

    "AI",

    "Tech",

)

DEV_SUFFIXES: Final[tuple[str, ...]] = (

    "Dev",

    "Pro",

)

# =====================================================
# HELPERS
# =====================================================

def clean_base(base: str) -> str:
    """
    Remove leading and trailing spaces.
    """

    return base.strip()


def random_symbol() -> str:
    """
    Return a random special symbol.
    """

    return secrets.choice(SPECIAL)


def random_3_digit() -> int:
    """
    Return a random 3-digit number.
    """

    return secrets.randbelow(900) + 100


def random_4_digit() -> int:
    """
    Return a random 4-digit number.
    """

    return secrets.randbelow(9000) + 1000


def random_suffix() -> str:
    """
    Return a random suffix.
    """

    return secrets.choice(SUFFIXES)


def unique(passwords: list[str]) -> list[str]:
    """
    Remove duplicate passwords while preserving order.
    """

    return list(dict.fromkeys(passwords))


# =====================================================
# PERSONAL
# =====================================================

def personal(base: str) -> list[str]:
    """
    Personal password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@123",

        f"{base}#{random_3_digit()}",

        f"{base}@786",

        f"{base}2026",

        f"{base}{random_symbol()}",

    ])


# =====================================================
# BANKING
# =====================================================

def banking(base: str) -> list[str]:
    """
    Banking password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@2026",

        f"{base}${random_4_digit()}",

        f"Bank@{base}",

        f"{base}!Money",

        f"{base}#Secure",

    ])


# =====================================================
# SOCIAL MEDIA
# =====================================================

def social(base: str) -> list[str]:
    """
    Social media password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Instagram",

        f"{base}@Facebook",

        f"{base}@Social",

        f"{base}#Follow",

        f"{base}!Like",

    ])
    
# =====================================================
# GAMING
# =====================================================

def gaming(base: str) -> list[str]:
    """
    Gaming password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}Gaming",

        f"{base}_Pro",

        f"{base}#OP",

        f"{base}@Legend",

        f"{base}X",

    ])


# =====================================================
# WIFI
# =====================================================

def wifi(base: str) -> list[str]:
    """
    WiFi password templates.
    """

    base = clean_base(base)

    return unique([

        f"WiFi@{base}",

        f"{base}Router",

        f"{base}@Home",

        f"{base}Net123",

        f"{base}#Internet",

    ])


# =====================================================
# DEVELOPER
# =====================================================

def developer(base: str) -> list[str]:
    """
    Developer password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Python",

        f"{base}@AI",

        f"{base}@Code",

        f"{base}Dev123",

        f"{base}#Git",

    ])


# =====================================================
# MEMORABLE
# =====================================================

def memorable(base: str) -> list[str]:
    """
    Generate memorable password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@123",

        f"{base}#{secrets.choice(('007', '786'))}",

        f"{base}@2026",

        f"{base}_{secrets.choice(AI_SUFFIXES)}",

        f"{base}-{secrets.choice(DEV_SUFFIXES)}",

        f"{base}{random_suffix()}",

        f"{base}@{random_suffix()}",

        f"{base}#{random_suffix()}",

        f"{random_symbol()}{base}",

        f"{base}{random_symbol()}",

    ])


# =====================================================
# BUSINESS
# =====================================================

def business(base: str) -> list[str]:
    """
    Business password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Office",

        f"{base}@Business",

        f"{base}#Company",

        f"{base}@Work",

        f"{base}2026",

    ])


# =====================================================
# EMAIL
# =====================================================

def email(base: str) -> list[str]:
    """
    Email account password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Mail",

        f"{base}@Email",

        f"{base}#Inbox",

        f"{base}@Secure",

        f"{base}{random_symbol()}",

    ])


# =====================================================
# SHOPPING
# =====================================================

def shopping(base: str) -> list[str]:
    """
    Shopping account password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Amazon",

        f"{base}@Flipkart",

        f"{base}@Store",

        f"{base}#Buy",

        f"{base}{random_3_digit()}",

    ])
    
# =====================================================
# TEMPLATE REGISTRY
# =====================================================

TEMPLATES: Final[dict[str, TemplateFunction]] = {

    "Personal": personal,

    "Banking": banking,

    "Social Media": social,

    "Gaming": gaming,

    "WiFi": wifi,

    "Developer": developer,

    "Business": business,

    "Email": email,

    "Shopping": shopping,

    "Memorable": memorable,

}

# =====================================================
# GET TEMPLATE
# =====================================================

def get_template(
    template_name: str,
    base: str,
) -> list[str]:
    """
    Return passwords from the selected template.

    Falls back to Personal template if
    the requested template is unavailable.
    """

    template_name = template_name.strip()

    generator = TEMPLATES.get(

        template_name,

        personal,

    )

    return generator(base)


# =====================================================
# AVAILABLE TEMPLATES
# =====================================================

def available_templates() -> list[str]:
    """
    Return all available template names.
    """

    return sorted(TEMPLATES.keys())


# =====================================================
# TEMPLATE EXISTS
# =====================================================

def template_exists(
    template_name: str,
) -> bool:
    """
    Check whether a template exists.
    """

    return template_name.strip() in TEMPLATES


# =====================================================
# RANDOM TEMPLATE
# =====================================================

def random_template() -> str:
    """
    Return a random template name.
    """

    return secrets.choice(

        tuple(TEMPLATES.keys())

    )


# =====================================================
# TEMPLATE COUNT
# =====================================================

def template_count() -> int:
    """
    Return total number of templates.
    """

    return len(TEMPLATES)


# =====================================================
# MODULE INFORMATION
# =====================================================

def module_info() -> dict[str, object]:
    """
    Return module information.
    """

    return {

        "version": "4.1 Professional",

        "templates": template_count(),

        "available": available_templates(),

    }


# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Password Templates Module")

    print("=" * 60)

    print(f"Version : {module_info()['version']}")

    print(f"Templates : {template_count()}")

    print()

    for name in available_templates():

        print(f"[{name}]")

        passwords = get_template(

            name,

            "Shahnawaz",

        )

        for password in passwords:

            print(" ", password)

        print()

    print("=" * 60)

    print("Random Template")

    print(random_template())

    print("=" * 60)

    assert template_exists("Personal")

    assert template_exists("Gaming")

    assert not template_exists("Unknown")

    assert len(personal("Test")) > 0

    assert len(memorable("Test")) > 0

    print("All tests passed successfully.")

    print("=" * 60)