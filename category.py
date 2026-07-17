# =====================================================
# PASSWORD CATEGORY
# Version 4.0 Professional
# =====================================================

import streamlit as st


# =====================================================
# DEFAULT CATEGORIES
# =====================================================

CATEGORIES = [

    "Personal",

    "Banking",

    "Social Media",

    "Gaming",

    "WiFi",

    "Developer",

    "Work",

    "Email",

    "Other"

]


# =====================================================
# GET CATEGORIES
# =====================================================

def get_categories():
    """
    Return all available categories.
    """

    return CATEGORIES


# =====================================================
# CATEGORY SELECTOR
# =====================================================

def select_category(default="Personal"):
    """
    Display category selector.
    """

    return st.selectbox(

        "Category",

        CATEGORIES,

        index=CATEGORIES.index(default)
        if default in CATEGORIES
        else 0

    )


# =====================================================
# CATEGORY BADGE
# =====================================================

def category_badge(category):

    colors = {

        "Personal": "#2563EB",

        "Banking": "#16A34A",

        "Social Media": "#9333EA",

        "Gaming": "#EA580C",

        "WiFi": "#0891B2",

        "Developer": "#0F172A",

        "Work": "#475569",

        "Email": "#DB2777",

        "Other": "#64748B"

    }

    color = colors.get(category, "#64748B")

    st.markdown(

        f"""
        <span style="
            background:{color};
            color:white;
            padding:6px 12px;
            border-radius:8px;
            font-size:13px;
            font-weight:600;
        ">
            {category}
        </span>
        """,

        unsafe_allow_html=True

    )


# =====================================================
# VALIDATION
# =====================================================

def validate_category(category):

    return category in CATEGORIES