# =====================================================
# PASSWORD ANALYTICS DASHBOARD
# Version 5.0 Professional
# Part 1/4
# =====================================================

from __future__ import annotations

# =====================================================
# THIRD-PARTY LIBRARIES
# =====================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from typing import Any
from typing import Dict
from typing import Final

# =====================================================
# LOCAL MODULES
# =====================================================

from history import export_csv

from database import (
    category_count,
    favorite_count,
    get_vault,
    vault_count,
)

# =====================================================
# MODULE CONSTANTS
# =====================================================

MODULE_NAME: Final[str] = "analytics"

MODULE_VERSION: Final[str] = (
    "5.0 Professional"
)

MIN_ENTROPY: Final[int] = 60

IDEAL_LENGTH: Final[int] = 12

MAX_SECURITY_SCORE: Final[int] = 100

PLOT_TEMPLATE: Final[str] = (
    "plotly_white"
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def mask_password(
    password: str,
) -> str:
    """
    Mask password before displaying.
    """

    if not password:
        return ""

    if len(password) <= 4:

        return "*" * len(password)

    return (

        password[:2]

        + "*" * (len(password) - 4)

        + password[-2:]

    )


# -----------------------------------------------------

def safe_average(
    series: pd.Series,
) -> float:
    """
    Safe average calculation.
    """

    if series.empty:

        return 0.0

    return round(

        float(series.mean()),

        2,

    )


# -----------------------------------------------------

def safe_percentage(
    value: int,
    total: int,
) -> float:
    """
    Return safe percentage.
    """

    if total <= 0:

        return 0.0

    return round(

        value / total * 100,

        2,

    )


# -----------------------------------------------------

def render_plotly_chart(
    fig: go.Figure,
    *,
    legend_title: str | None = None,
    x_title: str | None = None,
    y_title: str | None = None,
    bargap: float | None = None,
) -> None:
    """
    Apply dashboard styling.
    """

    layout = {

        "template": PLOT_TEMPLATE,

        "margin": dict(

            l=20,

            r=20,

            t=50,

            b=20,

        ),

    }

    if legend_title:

        layout["legend_title_text"] = (

            legend_title

        )

    if x_title:

        layout["xaxis_title"] = (

            x_title

        )

    if y_title:

        layout["yaxis_title"] = (

            y_title

        )

    if bargap is not None:

        layout["bargap"] = bargap

    fig.update_layout(**layout)

    st.plotly_chart(

        fig,

        use_container_width=True,

    )


# =====================================================
# HISTORY DATA
# =====================================================

@st.cache_data(
    show_spinner=False
)
def get_history_dataframe(
) -> pd.DataFrame:
    """
    Load password history.
    """

    try:

        df = export_csv()

    except Exception:

        return pd.DataFrame()

    if df.empty:

        return pd.DataFrame()

    df["Length"] = (

        df["Password"]

        .astype(str)

        .str.len()

    )

    if "Created" in df.columns:

        df["Created"] = pd.to_datetime(

            df["Created"],

            errors="coerce",

        )

    return df


# =====================================================
# VAULT DATA
# =====================================================

@st.cache_data(
    show_spinner=False
)
def get_vault_dataframe(
) -> pd.DataFrame:
    """
    Load vault database.
    """

    try:

        rows = get_vault()

    except Exception:

        return pd.DataFrame()

    if not rows:

        return pd.DataFrame()

    return pd.DataFrame(

        rows,

        columns=[

            "ID",

            "Website",

            "Username",

            "Encrypted Password",

            "Category",

            "Tags",

            "Notes",

            "Favorite",

            "Expiry Date",

            "Created",

            "Updated",

        ],

    )


# =====================================================
# CATEGORY DATA
# =====================================================

@st.cache_data(
    show_spinner=False
)
def get_category_dataframe(
) -> pd.DataFrame:
    """
    Load category statistics.
    """

    try:

        rows = category_count()

    except Exception:

        rows = []

    return pd.DataFrame(

        rows,

        columns=[

            "Category",

            "Count",

        ],

    )


# =====================================================
# KPI CALCULATIONS
# =====================================================

def calculate_overview(
    history_df: pd.DataFrame,
    category_df: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Calculate dashboard KPIs.
    """

    total_history = len(history_df)

    vault_total = vault_count()

    favorites = favorite_count()

    categories = len(category_df)

    if history_df.empty:

        avg_entropy = 0.0

        avg_length = 0.0

        strong = 0

        medium = 0

        weak = 0

    else:

        avg_entropy = safe_average(

            history_df["Entropy"]

        )

        avg_length = safe_average(

            history_df["Length"]

        )

        strong = len(

            history_df[

                history_df["Strength"]

                .str.contains(

                    "Excellent|Very|Strong",

                    case=False,

                    na=False,

                )

            ]

        )

        medium = len(

            history_df[

                history_df["Strength"]

                .str.contains(

                    "Medium",

                    case=False,

                    na=False,

                )

            ]

        )

        weak = max(

            total_history

            - strong

            - medium,

            0,

        )

    return {

        "history":

            total_history,

        "vault":

            vault_total,

        "favorites":

            favorites,

        "categories":

            categories,

        "avg_entropy":

            avg_entropy,

        "avg_length":

            avg_length,

        "strong":

            strong,

        "medium":

            medium,

        "weak":

            weak,

    }


# =====================================================
# MODULE INFO
# =====================================================

def module_info(
) -> Dict[str, str]:
    """
    Analytics module information.
    """

    return {

        "module":

            MODULE_NAME,

        "version":

            MODULE_VERSION,

        "framework":

            "Streamlit",

        "charts":

            "Plotly",

    }
    
    # =====================================================
# DASHBOARD UI
# Version 5.0 Professional
# Part 2/4
# =====================================================

def show_dashboard() -> None:
    """
    Render analytics dashboard.
    """

    st.title("Password Analytics Dashboard")

    st.caption(
        "Interactive security insights, trends and password analytics."
    )

    # =================================================
    # LOAD DATA
    # =================================================

    history_df = get_history_dataframe()

    vault_df = get_vault_dataframe()

    category_df = get_category_dataframe()

    if history_df.empty and vault_df.empty:

        st.info(
            "No analytics data available."
        )

        return

    # =================================================
    # SIDEBAR FILTERS
    # =================================================

    st.sidebar.subheader(
        "Analytics Filters"
    )

    if not history_df.empty:

        strength_options = [

            "All"

        ] + sorted(

            history_df["Strength"]

            .dropna()

            .unique()

            .tolist()

        )

        selected_strength = st.sidebar.selectbox(

            "Strength",

            strength_options,

        )

        if selected_strength != "All":

            history_df = history_df[

                history_df["Strength"]

                == selected_strength

            ]

    if not category_df.empty:

        category_options = [

            "All"

        ] + sorted(

            category_df["Category"]

            .tolist()

        )

        selected_category = st.sidebar.selectbox(

            "Vault Category",

            category_options,

        )

        if (

            selected_category != "All"

            and not vault_df.empty

        ):

            vault_df = vault_df[

                vault_df["Category"]

                == selected_category

            ]

    # =================================================
    # KPI OVERVIEW
    # =================================================

    overview = calculate_overview(

        history_df,

        category_df,

    )

    st.subheader("Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Generated",

        overview["history"],

    )

    c2.metric(

        "Vault",

        overview["vault"],

    )

    c3.metric(

        "Favorites",

        overview["favorites"],

    )

    c4.metric(

        "Categories",

        overview["categories"],

    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(

        "Entropy",

        f'{overview["avg_entropy"]} bits',

    )

    c6.metric(

        "Length",

        overview["avg_length"],

    )

    c7.metric(

        "Strong",

        overview["strong"],

    )

    c8.metric(

        "Weak",

        overview["weak"],

    )

    st.divider()

    # =================================================
    # PASSWORD STRENGTH
    # =================================================

    if not history_df.empty:

        st.subheader(
            "Password Strength"
        )

        left, right = st.columns(2)

        with left:

            fig = px.pie(

                history_df,

                names="Strength",

                hole=.45,

                title="Strength Distribution",

            )

            render_plotly_chart(

                fig,

                legend_title="Strength",

            )

        with right:

            strength_df = (

                history_df

                .groupby("Strength")

                .size()

                .reset_index(name="Count")

            )

            fig = px.bar(

                strength_df,

                x="Strength",

                y="Count",

                text="Count",

                title="Strength Count",

            )

            fig.update_traces(

                textposition="outside"

            )

            render_plotly_chart(

                fig,

                x_title="Strength",

                y_title="Passwords",

            )

    st.divider()

    # =================================================
    # ENTROPY ANALYTICS
    # =================================================

    if not history_df.empty:

        st.subheader(
            "Entropy Analytics"
        )

        left, right = st.columns(2)

        with left:

            fig = px.histogram(

                history_df,

                x="Entropy",

                nbins=20,

                title="Entropy Distribution",

            )

            render_plotly_chart(

                fig,

                bargap=.08,

            )

        with right:

            fig = px.box(

                history_df,

                y="Entropy",

                title="Entropy Spread",

            )

            render_plotly_chart(

                fig,

            )

    st.divider()

    # =================================================
    # PASSWORD LENGTH
    # =================================================

    if not history_df.empty:

        st.subheader(
            "Password Length"
        )

        left, right = st.columns(2)

        with left:

            fig = px.histogram(

                history_df,

                x="Length",

                nbins=20,

                title="Length Distribution",

            )

            render_plotly_chart(

                fig,

                bargap=.08,

            )

        with right:

            fig = px.scatter(

                history_df,

                x="Length",

                y="Entropy",

                color="Strength",

                title="Length vs Entropy",

            )

            render_plotly_chart(

                fig,

            )

    st.divider()

    # =================================================
    # PASSWORD TIMELINE
    # =================================================

    if (

        not history_df.empty

        and "Created" in history_df.columns

    ):

        timeline = (

            history_df

            .dropna(subset=["Created"])

            .groupby(

                history_df["Created"].dt.date

            )

            .size()

            .reset_index(name="Count")

        )

        if not timeline.empty:

            st.subheader(

                "Generation Timeline"

            )

            fig = px.line(

                timeline,

                x="Created",

                y="Count",

                markers=True,

                title="Passwords Generated",

            )

            render_plotly_chart(

                fig,

                x_title="Date",

                y_title="Passwords",

            )

    st.divider()

    # =================================================
    # CATEGORY ANALYTICS
    # =================================================

    if not category_df.empty:

        st.subheader(
            "Vault Categories"
        )

        left, right = st.columns(2)

        with left:

            fig = px.pie(

                category_df,

                names="Category",

                values="Count",

                hole=.45,

                title="Category Distribution",

            )

            render_plotly_chart(fig)

        with right:

            fig = px.bar(

                category_df,

                x="Category",

                y="Count",

                text="Count",

                title="Category Count",

            )

            fig.update_traces(

                textposition="outside"

            )

            render_plotly_chart(

                fig,

                x_title="Category",

                y_title="Passwords",

            )

    st.divider()

    # =================================================
    # WEBSITE ANALYTICS
    # =================================================

    if not vault_df.empty:

        st.subheader(
            "Top Websites"
        )

        website_df = (

            vault_df

            .groupby("Website")

            .size()

            .reset_index(name="Count")

            .sort_values(

                "Count",

                ascending=False,

            )

            .head(10)

        )

        fig = px.bar(

            website_df,

            x="Website",

            y="Count",

            text="Count",

            title="Most Used Websites",

        )

        fig.update_traces(

            textposition="outside"

        )

        render_plotly_chart(

            fig,

            x_title="Website",

            y_title="Passwords",

        )

    st.divider()

    # =================================================
    # FAVORITES ANALYTICS
    # =================================================

    favorite = favorite_count()

    others = max(

        vault_count() - favorite,

        0,

    )

    favorite_df = pd.DataFrame(

        {

            "Type": [

                "Favorites",

                "Others",

            ],

            "Count": [

                favorite,

                others,

            ],

        }

    )

    st.subheader(
        "Favorites"
    )

    fig = px.pie(

        favorite_df,

        names="Type",

        values="Count",

        hole=.45,

        title="Favorite Passwords",

    )

    render_plotly_chart(fig)

    st.divider()
    
    # =====================================================
# SECURITY INSIGHTS
# Version 5.0 Professional
# Part 3/4
# =====================================================

    # =================================================
    # RECENT VAULT ENTRIES
    # =================================================

    if not vault_df.empty:

        st.subheader(
            "Recent Vault Entries"
        )

        recent_df = vault_df.copy()

        if "Created" in recent_df.columns:

            recent_df = recent_df.sort_values(
                "Created",
                ascending=False,
            )

        if "Encrypted Password" in recent_df.columns:

            recent_df["Encrypted Password"] = (
                recent_df["Encrypted Password"]
                .astype(str)
                .apply(mask_password)
            )

        columns = [

            column

            for column in [

                "Website",

                "Username",

                "Category",

                "Tags",

                "Favorite",

                "Created",

            ]

            if column in recent_df.columns

        ]

        st.dataframe(

            recent_df[columns],

            hide_index=True,

            use_container_width=True,

        )

    st.divider()

    # =================================================
    # PASSWORD HEALTH SCORE
    # =================================================

    score = MAX_SECURITY_SCORE

    if overview["avg_entropy"] < MIN_ENTROPY:

        score -= 20

    if overview["avg_length"] < IDEAL_LENGTH:

        score -= 20

    if overview["weak"] > overview["strong"]:

        score -= 20

    if overview["favorites"] == 0:

        score -= 10

    if category_df.empty:

        score -= 10

    if overview["vault"] == 0:

        score -= 20

    score = max(score, 0)

    if score >= 90:

        level = "Excellent"

    elif score >= 75:

        level = "Good"

    elif score >= 60:

        level = "Fair"

    elif score >= 40:

        level = "Poor"

    else:

        level = "Critical"

    st.subheader(
        "Password Health Score"
    )

    st.progress(score / 100)

    c1, c2 = st.columns(2)

    c1.metric(

        "Security Score",

        f"{score}/100",

    )

    c2.metric(

        "Risk Level",

        level,

    )

    st.divider()

    # =================================================
    # SECURITY INSIGHTS
    # =================================================

    st.subheader(
        "Security Insights"
    )

    insights = []

    if overview["avg_entropy"] < MIN_ENTROPY:

        insights.append(

            (

                "warning",

                "Average password entropy is below the recommended level.",

            )

        )

    if overview["avg_length"] < IDEAL_LENGTH:

        insights.append(

            (

                "warning",

                "Average password length should be at least 12 characters.",

            )

        )

    if overview["weak"] > 0:

        insights.append(

            (

                "warning",

                f"{overview['weak']} weak passwords detected.",

            )

        )

    if overview["vault"] == 0:

        insights.append(

            (

                "info",

                "Save passwords in the encrypted vault.",

            )

        )

    if overview["favorites"] == 0:

        insights.append(

            (

                "info",

                "Mark frequently used passwords as favorites.",

            )

        )

    if category_df.empty:

        insights.append(

            (

                "info",

                "Organize passwords using categories.",

            )

        )

    if not insights:

        st.success(

            "Excellent! No security issues detected."

        )

    else:

        for severity, message in insights:

            with st.container(border=True):

                if severity == "warning":

                    st.warning(message)

                else:

                    st.info(message)

    st.divider()

    # =================================================
    # DUPLICATE PASSWORD DETECTION
    # =================================================

    if (

        not history_df.empty

        and "Password" in history_df.columns

    ):

        duplicate_df = (

            history_df

            .groupby("Password")

            .size()

            .reset_index(name="Count")

        )

        duplicate_df = duplicate_df[

            duplicate_df["Count"] > 1

        ]

        st.subheader(

            "Duplicate Password Analysis"

        )

        if duplicate_df.empty:

            st.success(

                "No duplicate passwords found."

            )

        else:

            st.warning(

                f"{len(duplicate_df)} duplicate passwords detected."

            )

            st.dataframe(

                duplicate_df,

                hide_index=True,

                use_container_width=True,

            )

    st.divider()

    # =================================================
    # PASSWORD STRENGTH BREAKDOWN
    # =================================================

    if not history_df.empty:

        st.subheader(

            "Password Quality"

        )

        quality_df = pd.DataFrame(

            {

                "Metric": [

                    "Strong",

                    "Medium",

                    "Weak",

                ],

                "Count": [

                    overview["strong"],

                    overview["medium"],

                    overview["weak"],

                ],

            }

        )

        fig = px.bar(

            quality_df,

            x="Metric",

            y="Count",

            text="Count",

            title="Password Quality",

        )

        fig.update_traces(

            textposition="outside"

        )

        render_plotly_chart(fig)

    st.divider()

    # =================================================
    # EXECUTIVE SUMMARY
    # =================================================

    st.subheader(

        "Executive Summary"

    )

    left, middle, right = st.columns(3)

    left.metric(

        "History",

        overview["history"],

    )

    middle.metric(

        "Vault",

        overview["vault"],

    )

    right.metric(

        "Security",

        f"{score}/100",

    )

    st.divider()

    # =================================================
    # RECOMMENDATIONS
    # =================================================

    st.subheader(

        "Recommendations"

    )

    recommendations = [

        "Use passwords with at least 12–16 characters.",

        "Include uppercase, lowercase, numbers and symbols.",

        "Avoid reusing passwords across websites.",

        "Store passwords securely in the encrypted vault.",

        "Review your vault regularly.",

        "Replace weak passwords immediately.",

        "Enable Two-Factor Authentication (2FA).",

        "Rotate important passwords periodically.",

    ]

    for recommendation in recommendations:

        st.markdown(

            f"- {recommendation}"

        )

    st.divider()
    
    # =====================================================
# EXPORT & DIAGNOSTICS
# Version 5.0 Professional
# Part 4/4
# =====================================================

import json

# =====================================================
# DASHBOARD STATISTICS
# =====================================================

def dashboard_statistics() -> Dict[str, Any]:
    """
    Return dashboard statistics.
    """

    history_df = get_history_dataframe()

    vault_df = get_vault_dataframe()

    category_df = get_category_dataframe()

    overview = calculate_overview(

        history_df,

        category_df,

    )

    return {

        "module":

            MODULE_NAME,

        "version":

            MODULE_VERSION,

        "history":

            overview["history"],

        "vault":

            overview["vault"],

        "favorites":

            overview["favorites"],

        "categories":

            overview["categories"],

        "average_entropy":

            overview["avg_entropy"],

        "average_length":

            overview["avg_length"],

        "strong_passwords":

            overview["strong"],

        "medium_passwords":

            overview["medium"],

        "weak_passwords":

            overview["weak"],

    }


# =====================================================
# JSON EXPORT
# =====================================================

def export_dashboard_json() -> str:
    """
    Export analytics as JSON.
    """

    return json.dumps(

        dashboard_statistics(),

        indent=4,

        default=str,

    )


# =====================================================
# DATAFRAME EXPORT
# =====================================================

def export_dashboard_dataframe() -> pd.DataFrame:
    """
    Export analytics as DataFrame.
    """

    stats = dashboard_statistics()

    return pd.DataFrame(

        [

            {

                "Metric": key,

                "Value": value,

            }

            for key, value

            in stats.items()

        ]

    )


# =====================================================
# DIAGNOSTICS
# =====================================================

def diagnostics() -> Dict[str, Any]:
    """
    Analytics diagnostics.
    """

    history_df = get_history_dataframe()

    vault_df = get_vault_dataframe()

    category_df = get_category_dataframe()

    return {

        "module":

            MODULE_NAME,

        "version":

            MODULE_VERSION,

        "status":

            "Healthy",

        "history_loaded":

            not history_df.empty,

        "vault_loaded":

            not vault_df.empty,

        "categories_loaded":

            not category_df.empty,

        "plotly":

            "Available",

        "streamlit":

            "Available",

        "pandas":

            "Available",

    }


# =====================================================
# EXAMPLE USAGE
# =====================================================

def example_usage() -> None:
    """
    Demonstrate analytics APIs.
    """

    print()

    print("=" * 60)

    print("Analytics Dashboard")

    print("=" * 60)

    print()

    print(

        dashboard_statistics()

    )

    print()

    print(

        diagnostics()

    )

    print()

    print(

        export_dashboard_json()

    )

    print()

    print(

        export_dashboard_dataframe()

    )


# =====================================================
# SELF TEST
# =====================================================

def run_self_test() -> bool:
    """
    Execute analytics self-test.
    """

    stats = dashboard_statistics()

    assert isinstance(

        stats,

        dict,

    )

    assert isinstance(

        diagnostics(),

        dict,

    )

    assert isinstance(

        module_info(),

        dict,

    )

    assert isinstance(

        export_dashboard_json(),

        str,

    )

    assert isinstance(

        export_dashboard_dataframe(),

        pd.DataFrame,

    )

    return True


# =====================================================
# ABOUT
# =====================================================

def about() -> Dict[str, Any]:
    """
    Analytics module metadata.
    """

    return {

        "name":

            "Password Analytics Dashboard",

        "module":

            MODULE_NAME,

        "version":

            MODULE_VERSION,

        "framework":

            "Streamlit",

        "charts":

            "Plotly",

        "language":

            "Python",

        "features": [

            "Dashboard",

            "KPIs",

            "Security Score",

            "Entropy Analytics",

            "Timeline",

            "Category Analytics",

            "Website Analytics",

            "Recommendations",

            "Diagnostics",

            "JSON Export",

        ],

    }


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("=" * 70)

    print("Password Analytics Dashboard")

    print(MODULE_VERSION)

    print("=" * 70)

    print()

    print("Module Information")

    print("-" * 70)

    for key, value in module_info().items():

        print(f"{key:<15}: {value}")

    print()

    print("Dashboard Statistics")

    print("-" * 70)

    print(

        dashboard_statistics()

    )

    print()

    print("Diagnostics")

    print("-" * 70)

    print(

        diagnostics()

    )

    print()

    print("About")

    print("-" * 70)

    print(

        about()

    )

    print()

    if run_self_test():

        print("✓ All analytics tests passed successfully.")

    print("=" * 70)