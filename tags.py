# =====================================================
# PASSWORD TAGS
# Version 4.0 Professional
# =====================================================

from __future__ import annotations

from typing import Final, List

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

# =====================================================
# GET DEFAULT TAGS
# =====================================================

def get_default_tags() -> List[str]:
    """
    Return all default tags.
    """

    return DEFAULT_TAGS.copy()


# =====================================================
# VALIDATE TAG
# =====================================================

def validate_tag(tag: str) -> bool:
    """
    Validate a tag.
    """

    return bool(tag and tag.strip())


# =====================================================
# NORMALIZE TAG
# =====================================================

def normalize_tag(tag: str) -> str:
    """
    Normalize a tag.
    """

    return tag.strip().title()


# =====================================================
# ADD TAG
# =====================================================

def add_tag(
    tag: str,
    tags: List[str],
) -> List[str]:
    """
    Add a new tag.
    """

    tag = normalize_tag(tag)

    if validate_tag(tag) and tag not in tags:

        tags.append(tag)

    return sorted(tags)


# =====================================================
# REMOVE TAG
# =====================================================

def remove_tag(
    tag: str,
    tags: List[str],
) -> List[str]:
    """
    Remove a tag.
    """

    tag = normalize_tag(tag)

    if tag in tags:

        tags.remove(tag)

    return sorted(tags)


# =====================================================
# SEARCH TAGS
# =====================================================

def search_tags(
    keyword: str,
    tags: List[str],
) -> List[str]:
    """
    Search tags.
    """

    keyword = keyword.lower().strip()

    return [

        tag

        for tag in tags

        if keyword in tag.lower()

    ]


# =====================================================
# UNIQUE TAGS
# =====================================================

def unique_tags(
    tags: List[str],
) -> List[str]:
    """
    Remove duplicate tags.
    """

    return sorted(

        list(

            {

                normalize_tag(tag)

                for tag in tags

                if validate_tag(tag)

            }

        )

    )


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

    print("Total Tags :", tag_count(tags))

    print()

    print("Developer Search:")

    print(

        search_tags(

            "dev",

            tags,

        )

    )

    print()

    print("All Tags:")

    print(tags)

    print("=" * 60)