# =====================================================
# PASSWORD TAGS
# Version 5.0 Professional
# =====================================================

from __future__ import annotations

from typing import Dict, Final, List

# =====================================================
# DEFAULT TAGS
# =====================================================

DEFAULT_TAGS: Final[List[str]] = [

    "Personal",
    "Work",
    "Banking",
    "Email",
    "Social Media",
    "Shopping",
    "Education",
    "Entertainment",
    "Gaming",
    "Developer",
    "Cloud",
    "Server",
    "Database",
    "Crypto",
    "Finance",
    "Travel",
    "Wi-Fi",
    "Business",
    "Custom",

]

POPULAR_TAGS: Final[List[str]] = [

    "Email",
    "Banking",
    "Developer",
    "Cloud",
    "Business",

]

# =====================================================
# DEFAULT TAGS
# =====================================================

def get_default_tags() -> List[str]:
    """
    Return default tags.
    """

    return sorted(DEFAULT_TAGS.copy())

# =====================================================
# VALIDATE
# =====================================================

def validate_tag(tag: str) -> bool:
    """
    Validate tag.
    """

    return bool(tag and tag.strip())

# =====================================================
# NORMALIZE
# =====================================================

def normalize_tag(tag: str) -> str:
    """
    Normalize tag.
    """

    return tag.strip().title()

# =====================================================
# UNIQUE
# =====================================================

def unique_tags(
    tags: List[str],
) -> List[str]:
    """
    Remove duplicates.
    """

    return sorted({

        normalize_tag(tag)

        for tag in tags

        if validate_tag(tag)

    })

# =====================================================
# ADD
# =====================================================

def add_tag(
    tag: str,
    tags: List[str],
) -> List[str]:
    """
    Add tag.
    """

    tag = normalize_tag(tag)

    if validate_tag(tag):

        if tag not in tags:

            tags.append(tag)

    return unique_tags(tags)

# =====================================================
# REMOVE
# =====================================================

def remove_tag(
    tag: str,
    tags: List[str],
) -> List[str]:
    """
    Remove tag.
    """

    tag = normalize_tag(tag)

    if tag in tags:

        tags.remove(tag)

    return unique_tags(tags)

# =====================================================
# SEARCH
# =====================================================

def search_tags(
    keyword: str,
    tags: List[str],
) -> List[str]:
    """
    Search tags.
    """

    keyword = keyword.lower().strip()

    return sorted([

        tag

        for tag in tags

        if keyword in tag.lower()

    ])

# =====================================================
# SUGGESTIONS
# =====================================================

def suggest_tags(
    keyword: str,
) -> List[str]:
    """
    Suggest matching default tags.
    """

    return search_tags(
        keyword,
        get_default_tags(),
    )

# =====================================================
# POPULAR TAGS
# =====================================================

def popular_tags() -> List[str]:
    """
    Return popular tags.
    """

    return POPULAR_TAGS.copy()

# =====================================================
# TAG EXISTS
# =====================================================

def tag_exists(
    tag: str,
    tags: List[str],
) -> bool:
    """
    Check whether tag exists.
    """

    return normalize_tag(tag) in unique_tags(tags)

# =====================================================
# TAG COUNT
# =====================================================

def tag_count(
    tags: List[str],
) -> int:
    """
    Return total tags.
    """

    return len(unique_tags(tags))

# =====================================================
# TAG CATEGORIES
# =====================================================

def tag_categories() -> Dict[str, List[str]]:
    """
    Return grouped tags.
    """

    return {

        "Personal": [

            "Personal",
            "Education",
            "Gaming",
            "Entertainment",
            "Travel",

        ],

        "Professional": [

            "Work",
            "Business",
            "Developer",

        ],

        "Technology": [

            "Cloud",
            "Server",
            "Database",
            "Crypto",

        ],

        "Accounts": [

            "Email",
            "Banking",
            "Finance",
            "Shopping",
            "Social Media",
            "Wi-Fi",

        ],

    }

# =====================================================
# TAG REPORT
# =====================================================

def tag_report(
    tags: List[str],
) -> Dict[str, object]:
    """
    Return tag statistics.
    """

    tags = unique_tags(tags)

    return {

        "total_tags": len(tags),

        "popular_tags": popular_tags(),

        "available_categories":
            list(tag_categories().keys()),

        "tags": tags,

    }

# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    tags = get_default_tags()

    tags = add_tag(
        "Github",
        tags,
    )

    tags = add_tag(
        "AWS",
        tags,
    )

    print("=" * 60)

    print("Password Tags Module")

    print("=" * 60)

    print(tag_report(tags))

    print()

    print("Search 'dev'")

    print(search_tags("dev", tags))

    print()

    print("Suggestions 'cl'")

    print(suggest_tags("cl"))

    print()

    print("Categories")

    print(tag_categories())

    print("=" * 60)