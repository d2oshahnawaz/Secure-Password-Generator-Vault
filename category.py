# =====================================================
# PASSWORD CATEGORY
# Version 5.0 Professional
# =====================================================

from typing import Dict, List
import streamlit as st

# =====================================================
# CATEGORY CONFIGURATION
# =====================================================

CATEGORY_CONFIG: Dict[str, Dict[str, str]] = {
    "Personal": {
        "color": "#2563EB",
        "icon": "bi-person-fill",
    },
    "Banking": {
        "color": "#16A34A",
        "icon": "bi-bank",
    },
    "Social Media": {
        "color": "#9333EA",
        "icon": "bi-share-fill",
    },
    "Gaming": {
        "color": "#EA580C",
        "icon": "bi-controller",
    },
    "WiFi": {
        "color": "#0891B2",
        "icon": "bi-wifi",
    },
    "Developer": {
        "color": "#0F172A",
        "icon": "bi-code-slash",
    },
    "Work": {
        "color": "#475569",
        "icon": "bi-briefcase-fill",
    },
    "Email": {
        "color": "#DB2777",
        "icon": "bi-envelope-fill",
    },
    "Other": {
        "color": "#64748B",
        "icon": "bi-folder-fill",
    },
}

# =====================================================
# CATEGORY LIST
# =====================================================

CATEGORIES: List[str] = list(CATEGORY_CONFIG.keys())

# =====================================================
# GET CATEGORIES
# =====================================================

def get_categories() -> List[str]:
    """
    Return all available categories.
    """
    return CATEGORIES.copy()

# =====================================================
# VALIDATE CATEGORY
# =====================================================

def validate_category(category: str) -> bool:
    """
    Validate category.
    """
    return category in CATEGORY_CONFIG

# =====================================================
# GET CATEGORY INFO
# =====================================================

def get_category_info(category: str) -> Dict[str, str]:
    """
    Return category metadata.
    """
    return CATEGORY_CONFIG.get(
        category,
        CATEGORY_CONFIG["Other"],
    )

# =====================================================
# CATEGORY SELECTOR
# =====================================================

def select_category(default: str = "Personal") -> str:
    """
    Display category selector.
    """

    default_index = (
        CATEGORIES.index(default)
        if default in CATEGORIES
        else 0
    )

    return st.selectbox(
        label="Password Category",
        options=CATEGORIES,
        index=default_index,
        help="Select the category for this password.",
    )

# =====================================================
# CATEGORY BADGE
# =====================================================

def category_badge(category: str) -> None:
    """
    Display colored category badge.
    """

    info = get_category_info(category)

    st.markdown(
        f"""
<div style="
display:inline-flex;
align-items:center;
gap:8px;
padding:8px 14px;
background:{info['color']};
color:white;
border-radius:10px;
font-weight:600;
font-size:14px;
margin:4px 0;
">

<i class="bi {info['icon']}"></i>

<span>{category}</span>

</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================
# CATEGORY CARD
# =====================================================

def category_card(category: str) -> None:
    """
    Display professional category card.
    """

    info = get_category_info(category)

    st.markdown(
        f"""
<div class="card">

<h4>
<i class="bi {info['icon']}" style="color:{info['color']}"></i>
{category}
</h4>

<p>
Selected password category.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================
# CATEGORY SUMMARY
# =====================================================

def show_category_summary(category: str) -> None:
    """
    Show category overview.
    """

    info = get_category_info(category)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Category",
            category,
        )

    with col2:
        st.metric(
            "Available Categories",
            len(CATEGORIES),
        )

    st.markdown(
        f"""
<div class="card">

<b>Category Color</b>

<div style="
width:100%;
height:18px;
border-radius:6px;
background:{info['color']};
margin-top:8px;
">
</div>

</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================
# ADD CUSTOM CATEGORY
# =====================================================

def add_category(
    name: str,
    color: str = "#64748B",
    icon: str = "bi-folder-fill",
) -> bool:
    """
    Add a custom category at runtime.
    """

    if not name or name in CATEGORY_CONFIG:
        return False

    CATEGORY_CONFIG[name] = {
        "color": color,
        "icon": icon,
    }

    CATEGORIES.append(name)

    return True

# =====================================================
# REMOVE CATEGORY
# =====================================================

def remove_category(name: str) -> bool:
    """
    Remove a custom category.
    Default categories cannot be removed.
    """

    default_categories = {
        "Personal",
        "Banking",
        "Social Media",
        "Gaming",
        "WiFi",
        "Developer",
        "Work",
        "Email",
        "Other",
    }

    if (
        name in default_categories
        or name not in CATEGORY_CONFIG
    ):
        return False

    CATEGORY_CONFIG.pop(name)
    CATEGORIES.remove(name)

    return True