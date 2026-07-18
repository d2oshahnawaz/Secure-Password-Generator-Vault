# =====================================================
# PASSWORD TEMPLATES
# Version 5.0 Professional
# Part 1/4
# =====================================================

from __future__ import annotations

import secrets

from typing import Callable
from typing import Dict
from typing import Final
from typing import List
from typing import TypeAlias

# =====================================================
# TYPE DEFINITIONS
# =====================================================

TemplateFunction: TypeAlias = Callable[[str], List[str]]

# =====================================================
# PASSWORD COMPLEXITY
# =====================================================

COMPLEXITY_LEVELS: Final[List[str]] = [

    "Basic",

    "Standard",

    "Strong",

    "Maximum",

]

# =====================================================
# SPECIAL CHARACTERS
# =====================================================

SPECIAL: Final[tuple[str, ...]] = (

    "@",

    "#",

    "$",

    "%",

    "&",

    "*",

    "+",

    "!",

    "?",

)

# =====================================================
# SUFFIXES
# =====================================================

SUFFIXES: Final[tuple[str, ...]] = (

    "AI",

    "Secure",

    "Tech",

    "Dev",

    "Pro",

    "2026",

    "2027",

    "007",

    "786",

    "Login",

    "Official",

    "Cloud",

    "Admin",

    "Prime",

)

# =====================================================
# PROFESSIONAL SUFFIXES
# =====================================================

DEV_SUFFIXES: Final[tuple[str, ...]] = (

    "Dev",

    "Code",

    "Python",

    "Git",

    "Pro",

)

BUSINESS_SUFFIXES: Final[tuple[str, ...]] = (

    "Office",

    "Business",

    "Corp",

    "Enterprise",

    "Company",

)

AI_SUFFIXES: Final[tuple[str, ...]] = (

    "AI",

    "ML",

    "LLM",

    "GenAI",

)

# =====================================================
# TEMPLATE DESCRIPTIONS
# =====================================================

TEMPLATE_DESCRIPTIONS: Final[Dict[str, str]] = {

    "Personal":
        "General purpose personal passwords.",

    "Banking":
        "Secure passwords for banking accounts.",

    "Business":
        "Professional office passwords.",

    "Developer":
        "Developer oriented passwords.",

    "Gaming":
        "Gaming account passwords.",

    "Social Media":
        "Passwords for social platforms.",

    "Email":
        "Secure email passwords.",

    "Shopping":
        "Shopping website passwords.",

    "WiFi":
        "Wireless network passwords.",

    "Cloud":
        "Cloud service passwords.",

    "Database":
        "Database credentials.",

    "Server":
        "Server administrator passwords.",

    "Education":
        "School and university accounts.",

    "Finance":
        "Financial applications.",

    "Crypto":
        "Cryptocurrency wallets.",

    "GitHub":
        "GitHub repositories.",

    "AWS":
        "Amazon Web Services.",

    "Azure":
        "Microsoft Azure.",

    "Google":
        "Google accounts.",

    "Microsoft":
        "Microsoft accounts.",

    "Enterprise":
        "Large organization accounts.",

    "Admin":
        "Administrative accounts.",

    "Memorable":
        "Easy to remember secure passwords.",

}

# =====================================================
# TEMPLATE CATEGORIES
# =====================================================

TEMPLATE_CATEGORIES: Final[Dict[str, List[str]]] = {

    "Personal": [

        "Personal",

        "Email",

        "Shopping",

        "Education",

        "Gaming",

        "Social Media",

    ],

    "Professional": [

        "Business",

        "Developer",

        "Enterprise",

        "Admin",

    ],

    "Technology": [

        "Cloud",

        "Server",

        "Database",

        "GitHub",

        "AWS",

        "Azure",

        "Google",

        "Microsoft",

    ],

    "Security": [

        "Banking",

        "Finance",

        "Crypto",

        "WiFi",

    ],

}

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def clean_base(
    base: str,
) -> str:
    """
    Normalize the base string.
    """

    return base.strip()

# -----------------------------------------------------

def unique(
    passwords: List[str],
) -> List[str]:
    """
    Remove duplicates while preserving order.
    """

    return list(dict.fromkeys(passwords))

# -----------------------------------------------------

def random_symbol() -> str:
    """
    Return a random special character.
    """

    return secrets.choice(SPECIAL)

# -----------------------------------------------------

def random_suffix() -> str:
    """
    Return random suffix.
    """

    return secrets.choice(SUFFIXES)

# -----------------------------------------------------

def random_3_digit() -> int:
    """
    Return random 3-digit number.
    """

    return secrets.randbelow(900) + 100

# -----------------------------------------------------

def random_4_digit() -> int:
    """
    Return random 4-digit number.
    """

    return secrets.randbelow(9000) + 1000

# -----------------------------------------------------

def complexity_level(
    password: str,
) -> str:
    """
    Estimate password complexity.
    """

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 1

    if score <= 1:
        return "Basic"

    if score == 2:
        return "Standard"

    if score == 3:
        return "Strong"

    return "Maximum"

# -----------------------------------------------------

def template_exists(
    template_name: str,
) -> bool:
    """
    Placeholder.
    Registry is created in Part 3.
    """

    return template_name.strip() in TEMPLATE_DESCRIPTIONS

# -----------------------------------------------------

def template_description(
    template_name: str,
) -> str:
    """
    Return template description.
    """

    return TEMPLATE_DESCRIPTIONS.get(

        template_name,

        "No description available.",

    )

# -----------------------------------------------------

def template_category(
    template_name: str,
) -> str:
    """
    Return template category.
    """

    for category, templates in TEMPLATE_CATEGORIES.items():

        if template_name in templates:

            return category

    return "Other"

# -----------------------------------------------------

def available_categories() -> List[str]:
    """
    Return all categories.
    """

    return sorted(

        TEMPLATE_CATEGORIES.keys()

    )
    
    # =====================================================
# TEMPLATE FUNCTIONS
# Version 5.0 Professional
# Part 2A-1
# =====================================================

# =====================================================
# PERSONAL
# =====================================================

def personal(base: str) -> List[str]:
    """
    Personal password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@123",

        f"{base}@2026",

        f"{base}{random_symbol()}",

        f"{base}#{random_3_digit()}",

        f"{base}{random_suffix()}",

        f"{random_symbol()}{base}",

        f"{base}{random_symbol()}{random_3_digit()}",

        f"{base}Secure",

    ])


# =====================================================
# BANKING
# =====================================================

def banking(base: str) -> List[str]:
    """
    Banking password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Secure",

        f"{base}${random_4_digit()}",

        f"Bank@{base}",

        f"{base}#Money",

        f"{base}@Vault",

        f"{base}@Finance",

        f"{base}#{random_suffix()}",

        f"{random_symbol()}{base}2026",

    ])


# =====================================================
# BUSINESS
# =====================================================

def business(base: str) -> List[str]:
    """
    Business password templates.
    """

    base = clean_base(base)

    suffix = secrets.choice(BUSINESS_SUFFIXES)

    return unique([

        f"{base}@Business",

        f"{base}@Office",

        f"{base}@Work",

        f"{base}#{suffix}",

        f"{base}{random_symbol()}{random_3_digit()}",

        f"{suffix}{base}",

        f"{base}@Enterprise",

        f"{base}2026",

    ])


# =====================================================
# DEVELOPER
# =====================================================

def developer(base: str) -> List[str]:
    """
    Developer password templates.
    """

    base = clean_base(base)

    suffix = secrets.choice(DEV_SUFFIXES)

    return unique([

        f"{base}@Python",

        f"{base}@Code",

        f"{base}@Git",

        f"{base}@AI",

        f"{base}#{suffix}",

        f"{base}{random_symbol()}{random_4_digit()}",

        f"{suffix}@{base}",

        f"{base}@SecureDev",

    ])


# =====================================================
# GAMING
# =====================================================

def gaming(base: str) -> List[str]:
    """
    Gaming password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}Gaming",

        f"{base}@Legend",

        f"{base}#OP",

        f"{base}Pro",

        f"{base}X",

        f"{base}{random_symbol()}GG",

        f"{base}{random_3_digit()}",

        f"{random_symbol()}{base}Winner",

    ])
    
    # =====================================================
# TEMPLATE FUNCTIONS
# Version 5.0 Professional
# Part 2A-2
# =====================================================

# =====================================================
# SOCIAL MEDIA
# =====================================================

def social(base: str) -> List[str]:
    """
    Social media password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Instagram",

        f"{base}@Facebook",

        f"{base}@Social",

        f"{base}@Follow",

        f"{base}#Creator",

        f"{base}{random_symbol()}2026",

        f"{base}{random_symbol()}{random_3_digit()}",

        f"{random_symbol()}{base}Media",

    ])


# =====================================================
# EMAIL
# =====================================================

def email(base: str) -> List[str]:
    """
    Email account password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Mail",

        f"{base}@Email",

        f"{base}@Inbox",

        f"{base}@Secure",

        f"{base}@Primary",

        f"{base}{random_symbol()}{random_3_digit()}",

        f"{random_symbol()}{base}Mail",

        f"{base}Mail2026",

    ])


# =====================================================
# SHOPPING
# =====================================================

def shopping(base: str) -> List[str]:
    """
    Shopping account password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Amazon",

        f"{base}@Flipkart",

        f"{base}@Store",

        f"{base}@Cart",

        f"{base}#Shopping",

        f"{base}{random_symbol()}{random_3_digit()}",

        f"{random_symbol()}{base}Buy",

        f"{base}Deals2026",

    ])


# =====================================================
# WIFI
# =====================================================

def wifi(base: str) -> List[str]:
    """
    Wi-Fi password templates.
    """

    base = clean_base(base)

    return unique([

        f"WiFi@{base}",

        f"{base}@Router",

        f"{base}@Network",

        f"{base}#Internet",

        f"{base}HomeNet",

        f"{base}{random_symbol()}{random_4_digit()}",

        f"Net{random_symbol()}{base}",

        f"{base}Router2026",

    ])


# =====================================================
# MEMORABLE
# =====================================================

def memorable(base: str) -> List[str]:
    """
    Generate memorable secure password templates.
    """

    base = clean_base(base)

    ai_suffix = secrets.choice(AI_SUFFIXES)

    dev_suffix = secrets.choice(DEV_SUFFIXES)

    return unique([

        f"{base}@123",

        f"{base}@2026",

        f"{base}#{random_3_digit()}",

        f"{base}_{ai_suffix}",

        f"{base}-{dev_suffix}",

        f"{base}{random_suffix()}",

        f"{base}@{random_suffix()}",

        f"{base}#{random_suffix()}",

        f"{random_symbol()}{base}",

        f"{base}{random_symbol()}",

        f"{base}{random_symbol()}{random_3_digit()}",

        f"{base}Secure",

    ])
    
    # =====================================================
# TEMPLATE FUNCTIONS
# Version 5.0 Professional
# Part 2B
# =====================================================

# =====================================================
# CLOUD
# =====================================================

def cloud(base: str) -> List[str]:
    """
    Cloud service password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Cloud",

        f"{base}@SecureCloud",

        f"{base}#Cloud",

        f"{base}Cloud{random_3_digit()}",

        f"{random_symbol()}{base}Cloud",

        f"{base}{random_symbol()}Cloud",

        f"{base}@Storage",

        f"{base}Cloud2026",

    ])


# =====================================================
# DATABASE
# =====================================================

def database(base: str) -> List[str]:
    """
    Database password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@DB",

        f"{base}@Database",

        f"{base}#SQL",

        f"{base}DB{random_4_digit()}",

        f"{base}@Postgres",

        f"{base}@MySQL",

        f"{random_symbol()}{base}DB",

        f"{base}SecureDB",

    ])


# =====================================================
# SERVER
# =====================================================

def server(base: str) -> List[str]:
    """
    Server administrator templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Server",

        f"{base}@Linux",

        f"{base}#Root",

        f"{base}Server{random_3_digit()}",

        f"{base}@Admin",

        f"{random_symbol()}{base}Root",

        f"{base}{random_symbol()}SSH",

        f"{base}Server2026",

    ])


# =====================================================
# FINANCE
# =====================================================

def finance(base: str) -> List[str]:
    """
    Finance password templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Finance",

        f"{base}@Money",

        f"{base}#Secure",

        f"{base}Wallet{random_3_digit()}",

        f"{base}@Account",

        f"{random_symbol()}{base}Finance",

        f"{base}{random_symbol()}Fund",

        f"{base}Finance2026",

    ])


# =====================================================
# CRYPTO
# =====================================================

def crypto(base: str) -> List[str]:
    """
    Cryptocurrency wallet templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Crypto",

        f"{base}@Wallet",

        f"{base}#BTC",

        f"{base}ETH{random_3_digit()}",

        f"{base}@Blockchain",

        f"{random_symbol()}{base}Coin",

        f"{base}{random_symbol()}Ledger",

        f"{base}Crypto2026",

    ])


# =====================================================
# GITHUB
# =====================================================

def github(base: str) -> List[str]:
    """
    GitHub account templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@GitHub",

        f"{base}@Git",

        f"{base}#Repo",

        f"{base}Commit{random_3_digit()}",

        f"{base}@Code",

        f"{random_symbol()}{base}Git",

        f"{base}{random_symbol()}Push",

        f"{base}Git2026",

    ])


# =====================================================
# AWS
# =====================================================

def aws(base: str) -> List[str]:
    """
    AWS account templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@AWS",

        f"{base}@EC2",

        f"{base}#S3",

        f"{base}IAM{random_3_digit()}",

        f"{base}@Lambda",

        f"{random_symbol()}{base}AWS",

        f"{base}{random_symbol()}Cloud",

        f"{base}AWS2026",

    ])


# =====================================================
# AZURE
# =====================================================

def azure(base: str) -> List[str]:
    """
    Microsoft Azure templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Azure",

        f"{base}@Cloud",

        f"{base}#Azure",

        f"{base}AD{random_3_digit()}",

        f"{base}@Microsoft",

        f"{random_symbol()}{base}Azure",

        f"{base}{random_symbol()}Tenant",

        f"{base}Azure2026",

    ])


# =====================================================
# GOOGLE
# =====================================================

def google(base: str) -> List[str]:
    """
    Google account templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Google",

        f"{base}@Gmail",

        f"{base}#Drive",

        f"{base}Docs{random_3_digit()}",

        f"{base}@Workspace",

        f"{random_symbol()}{base}Google",

        f"{base}{random_symbol()}Mail",

        f"{base}Google2026",

    ])


# =====================================================
# MICROSOFT
# =====================================================

def microsoft(base: str) -> List[str]:
    """
    Microsoft account templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Microsoft",

        f"{base}@Office",

        f"{base}#365",

        f"{base}Teams{random_3_digit()}",

        f"{base}@Outlook",

        f"{random_symbol()}{base}MS",

        f"{base}{random_symbol()}Office",

        f"{base}MS2026",

    ])


# =====================================================
# ENTERPRISE
# =====================================================

def enterprise(base: str) -> List[str]:
    """
    Enterprise account templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Enterprise",

        f"{base}@Corporate",

        f"{base}#Secure",

        f"{base}Corp{random_4_digit()}",

        f"{base}@Company",

        f"{random_symbol()}{base}Enterprise",

        f"{base}{random_symbol()}Business",

        f"{base}Enterprise2026",

    ])


# =====================================================
# ADMIN
# =====================================================

def admin(base: str) -> List[str]:
    """
    Administrative account templates.
    """

    base = clean_base(base)

    return unique([

        f"{base}@Admin",

        f"{base}@Root",

        f"{base}#System",

        f"{base}Admin{random_4_digit()}",

        f"{base}@Control",

        f"{random_symbol()}{base}Admin",

        f"{base}{random_symbol()}Secure",

        f"{base}Admin2026",

    ])
    
    # =====================================================
# TEMPLATE REGISTRY
# Version 5.0 Professional
# Part 3/4
# =====================================================

TEMPLATES: Dict[str, TemplateFunction] = {

    "Personal": personal,

    "Banking": banking,

    "Business": business,

    "Developer": developer,

    "Gaming": gaming,

    "Social Media": social,

    "Email": email,

    "Shopping": shopping,

    "WiFi": wifi,

    "Memorable": memorable,

    "Cloud": cloud,

    "Database": database,

    "Server": server,

    "Finance": finance,

    "Crypto": crypto,

    "GitHub": github,

    "AWS": aws,

    "Azure": azure,

    "Google": google,

    "Microsoft": microsoft,

    "Enterprise": enterprise,

    "Admin": admin,

}

# =====================================================
# GET TEMPLATE
# =====================================================

def get_template(
    template_name: str,
    base: str,
) -> List[str]:
    """
    Generate passwords using the selected template.
    Falls back to Personal if template is unavailable.
    """

    template_name = template_name.strip()

    generator = TEMPLATES.get(
        template_name,
        personal,
    )

    return unique(generator(base))


# =====================================================
# AVAILABLE TEMPLATES
# =====================================================

def available_templates() -> List[str]:
    """
    Return available template names.
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
        available_templates()
    )


# =====================================================
# TEMPLATE COUNT
# =====================================================

def template_count() -> int:
    """
    Return total templates.
    """

    return len(TEMPLATES)


# =====================================================
# TEMPLATE INFORMATION
# =====================================================

def template_info(
    template_name: str,
) -> Dict[str, object]:
    """
    Return metadata for a template.
    """

    return {

        "name": template_name,

        "exists":
            template_exists(template_name),

        "description":
            template_description(template_name),

        "category":
            template_category(template_name),

    }


# =====================================================
# REGISTER TEMPLATE
# =====================================================

def register_template(
    name: str,
    function: TemplateFunction,
) -> None:
    """
    Register a custom template.
    """

    name = name.strip()

    if not name:
        raise ValueError(
            "Template name cannot be empty."
        )

    TEMPLATES[name] = function


# =====================================================
# REMOVE TEMPLATE
# =====================================================

def remove_template(
    name: str,
) -> bool:
    """
    Remove a registered template.
    """

    if name in TEMPLATES:

        del TEMPLATES[name]

        return True

    return False


# =====================================================
# MULTIPLE TEMPLATE GENERATOR
# =====================================================

def generate_multiple_templates(
    base: str,
    template_names: List[str],
) -> Dict[str, List[str]]:
    """
    Generate passwords from multiple templates.
    """

    results: Dict[str, List[str]] = {}

    for template in template_names:

        results[template] = get_template(
            template,
            base,
        )

    return results


# =====================================================
# TEMPLATE SUGGESTIONS
# =====================================================

def suggest_template(
    purpose: str,
) -> List[str]:
    """
    Suggest templates based on usage.
    """

    purpose = purpose.lower().strip()

    mapping = {

        "bank": [

            "Banking",

            "Finance",

            "Crypto",

        ],

        "office": [

            "Business",

            "Enterprise",

            "Admin",

        ],

        "developer": [

            "Developer",

            "GitHub",

            "AWS",

            "Azure",

        ],

        "cloud": [

            "Cloud",

            "AWS",

            "Azure",

            "Google",

        ],

        "database": [

            "Database",

            "Server",

        ],

        "email": [

            "Email",

        ],

        "shopping": [

            "Shopping",

        ],

        "gaming": [

            "Gaming",

        ],

        "wifi": [

            "WiFi",

        ],

        "social": [

            "Social Media",

        ],

        "student": [

            "Education",

            "Personal",

        ],

    }

    for keyword, templates in mapping.items():

        if keyword in purpose:

            return templates

    return [

        "Personal",

        "Memorable",

    ]


# =====================================================
# TEMPLATE METADATA
# =====================================================

def template_metadata() -> Dict[str, object]:
    """
    Return complete metadata.
    """

    return {

        "count": template_count(),

        "templates":
            available_templates(),

        "categories":
            available_categories(),

        "complexity_levels":
            COMPLEXITY_LEVELS,

    }


# =====================================================
# TEMPLATE REPORT
# =====================================================

def template_report() -> Dict[str, object]:
    """
    Return complete module report.
    """

    return {

        "version":
            "5.0 Professional",

        "total_templates":
            template_count(),

        "categories":
            TEMPLATE_CATEGORIES,

        "descriptions":
            TEMPLATE_DESCRIPTIONS,

        "metadata":
            template_metadata(),

    }


# =====================================================
# MODULE INFORMATION
# =====================================================

def module_info() -> Dict[str, object]:
    """
    Return module information.
    """

    return {

        "module":
            "templates",

        "version":
            "5.0 Professional",

        "templates":
            template_count(),

        "categories":
            len(TEMPLATE_CATEGORIES),

        "available":
            available_templates(),

    }
    
    # =====================================================
# SELF TEST
# Version 5.0 Professional
# Part 4/4
# =====================================================

def run_self_test() -> bool:
    """
    Run basic module validation tests.

    Returns
    -------
    bool
        True if all tests pass.
    """

    sample = "Shahnawaz"

    # ---------------------------------------------
    # Registry
    # ---------------------------------------------

    assert template_exists("Personal")
    assert template_exists("Developer")
    assert template_exists("Business")
    assert template_exists("AWS")
    assert template_exists("GitHub")

    assert not template_exists("Unknown")

    # ---------------------------------------------
    # Available Templates
    # ---------------------------------------------

    templates = available_templates()

    assert len(templates) == template_count()

    assert "Personal" in templates

    # ---------------------------------------------
    # Password Generation
    # ---------------------------------------------

    for template in templates:

        passwords = get_template(
            template,
            sample,
        )

        assert isinstance(passwords, list)

        assert len(passwords) > 0

        assert len(passwords) == len(
            unique(passwords)
        )

    # ---------------------------------------------
    # Categories
    # ---------------------------------------------

    assert template_category(
        "Developer"
    ) == "Professional"

    assert template_category(
        "Cloud"
    ) == "Technology"

    # ---------------------------------------------
    # Description
    # ---------------------------------------------

    assert isinstance(
        template_description(
            "Developer"
        ),
        str,
    )

    # ---------------------------------------------
    # Metadata
    # ---------------------------------------------

    metadata = template_metadata()

    assert metadata["count"] == template_count()

    assert isinstance(
        metadata["templates"],
        list,
    )

    # ---------------------------------------------
    # Suggestions
    # ---------------------------------------------

    assert len(
        suggest_template(
            "developer"
        )
    ) > 0

    assert len(
        suggest_template(
            "cloud"
        )
    ) > 0

    # ---------------------------------------------
    # Multiple Generation
    # ---------------------------------------------

    generated = generate_multiple_templates(

        sample,

        [

            "Personal",

            "Developer",

            "Business",

        ],

    )

    assert len(generated) == 3

    # ---------------------------------------------
    # Complexity
    # ---------------------------------------------

    assert complexity_level(
        "abc"
    ) == "Basic"

    assert complexity_level(
        "Password123"
    ) in COMPLEXITY_LEVELS

    return True


# =====================================================
# EXAMPLE USAGE
# =====================================================

def example_usage() -> None:
    """
    Demonstrate module usage.
    """

    base = "Shahnawaz"

    print("=" * 70)

    print("Password Templates Example")

    print("=" * 70)

    print()

    for template in available_templates():

        print(f"[{template}]")

        for password in get_template(
            template,
            base,
        ):

            print(" ", password)

        print()

    print("=" * 70)


# =====================================================
# MODULE DIAGNOSTICS
# =====================================================

def diagnostics() -> Dict[str, object]:
    """
    Return diagnostic information.
    """

    return {

        "module":
            "templates",

        "version":
            "5.0 Professional",

        "status":
            "Healthy",

        "templates":
            template_count(),

        "categories":
            len(
                TEMPLATE_CATEGORIES
            ),

        "complexity_levels":
            COMPLEXITY_LEVELS,

        "self_test":
            run_self_test(),

    }


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("=" * 70)

    print("Password Templates")
    print("Version 5.0 Professional")

    print("=" * 70)

    info = module_info()

    print(f"Version      : {info['version']}")
    print(f"Templates    : {info['templates']}")
    print(f"Categories   : {info['categories']}")

    print()

    example_usage()

    print()

    print("Diagnostics")

    print("-" * 70)

    for key, value in diagnostics().items():

        print(f"{key:<20}: {value}")

    print()

    if run_self_test():

        print("✓ All tests passed successfully.")

    print("=" * 70)