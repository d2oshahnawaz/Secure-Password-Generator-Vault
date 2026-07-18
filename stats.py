# =====================================================
# PASSWORD STATISTICS
# Version 6.0 Professional
# Part 1
# Imports + Helpers + Report Functions
# =====================================================

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd
import plotly.express as px
import streamlit as st

from generator import password_stats

# =====================================================
# CONSTANTS
# =====================================================

CATEGORIES = [
    "Uppercase",
    "Lowercase",
    "Numbers",
    "Special",
]

# =====================================================
# PASSWORD REPORT
# =====================================================

def statistics_report(password: str) -> Dict[str, float]:
    """
    Generate a complete statistics report
    for the supplied password.
    """

    stats = password_stats(password)

    length = max(stats.get("length", 0), 1)

    diversity = sum([
        stats.get("uppercase", 0) > 0,
        stats.get("lowercase", 0) > 0,
        stats.get("digits", 0) > 0,
        stats.get("special", 0) > 0,
    ])

    return {

        "length": stats.get("length", 0),

        "uppercase": stats.get("uppercase", 0),

        "lowercase": stats.get("lowercase", 0),

        "digits": stats.get("digits", 0),

        "special": stats.get("special", 0),

        "diversity": diversity,

        "uppercase_percent": round(
            stats.get("uppercase", 0) / length * 100,
            2,
        ),

        "lowercase_percent": round(
            stats.get("lowercase", 0) / length * 100,
            2,
        ),

        "digits_percent": round(
            stats.get("digits", 0) / length * 100,
            2,
        ),

        "special_percent": round(
            stats.get("special", 0) / length * 100,
            2,
        ),

    }

# =====================================================
# DATAFRAME HELPERS
# =====================================================

def build_count_dataframe(
    report: Dict[str, float],
) -> pd.DataFrame:
    """
    Character count dataframe.
    """

    return pd.DataFrame({

        "Category": CATEGORIES,

        "Count": [

            report["uppercase"],

            report["lowercase"],

            report["digits"],

            report["special"],

        ],

    })


def build_percentage_dataframe(
    report: Dict[str, float],
) -> pd.DataFrame:
    """
    Character percentage dataframe.
    """

    return pd.DataFrame({

        "Category": CATEGORIES,

        "Percentage": [

            report["uppercase_percent"],

            report["lowercase_percent"],

            report["digits_percent"],

            report["special_percent"],

        ],

    })

# =====================================================
# CHART BUILDERS
# =====================================================

def create_pie_chart(
    dataframe: pd.DataFrame,
):
    """
    Create donut chart.
    """

    fig = px.pie(

        dataframe,

        names="Category",

        values="Count",

        hole=0.60,

        title="Character Distribution",

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label",

    )

    fig.update_layout(

        height=360,

        margin=dict(

            l=20,

            r=20,

            t=50,

            b=20,

        ),

        legend_title="Character Type",

    )

    return fig


def create_bar_chart(
    dataframe: pd.DataFrame,
):
    """
    Create character count bar chart.
    """

    fig = px.bar(

        dataframe,

        x="Category",

        y="Count",

        text="Count",

        title="Character Count",

    )

    fig.update_traces(

        textposition="outside",

    )

    fig.update_layout(

        height=350,

        showlegend=False,

        margin=dict(

            l=20,

            r=20,

            t=50,

            b=20,

        ),

    )

    return fig

# =====================================================
# MAIN UI
# =====================================================

def show_password_stats(
    password: str,
    key: Optional[str] = None,
) -> None:
    """
    Display complete password statistics.

    (Part 2 continues...)
    """
    pass

    # =================================================
    # PASSWORD REPORT
    # =================================================

    report = statistics_report(password)

    st.markdown(
        """
### <i class="bi bi-bar-chart-fill"></i>
Password Statistics
""",
        unsafe_allow_html=True,
    )

    # =================================================
    # METRICS
    # =================================================

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            "Length",
            report["length"],
        )

        st.metric(
            "Uppercase",
            report["uppercase"],
        )

    with metric2:

        st.metric(
            "Lowercase",
            report["lowercase"],
        )

        st.metric(
            "Numbers",
            report["digits"],
        )

    with metric3:

        st.metric(
            "Special",
            report["special"],
        )

        st.metric(
            "Types",
            f"{report['diversity']}/4",
        )

    st.divider()

    # =================================================
    # DATAFRAME
    # =================================================

    count_df = build_count_dataframe(report)

    # =================================================
    # PIE CHART
    # =================================================

    pie_chart = create_pie_chart(count_df)

    st.plotly_chart(
        pie_chart,
        use_container_width=True,
        theme="streamlit",
        key=f"{key}_pie" if key else None,
    )

    st.divider()

    # =================================================
    # BAR CHART
    # =================================================

    bar_chart = create_bar_chart(count_df)

    st.plotly_chart(
        bar_chart,
        use_container_width=True,
        theme="streamlit",
        key=f"{key}_bar" if key else None,
    )

    st.divider()

    # =================================================
    # CHARACTER DIVERSITY
    # =================================================

    st.markdown(
        """
#### <i class="bi bi-diagram-3-fill"></i>
Character Diversity
""",
        unsafe_allow_html=True,
    )

    diversity_progress = report["diversity"] / 4

    st.progress(
        diversity_progress,
        text=f"{report['diversity']}/4 Character Types",
    )

    if report["diversity"] == 4:

        st.success(
            "Excellent character diversity. Your password contains all major character categories."
        )

    elif report["diversity"] == 3:

        st.info(
            "Good character diversity. Consider adding one more character type for maximum security."
        )

    elif report["diversity"] == 2:

        st.warning(
            "Moderate diversity. Using more character categories will significantly improve password strength."
        )

    else:

        st.error(
            "Poor diversity. Include uppercase, lowercase, numbers and special characters."
        )

    st.divider()

        # =================================================
    # CHARACTER PERCENTAGE
    # =================================================

    st.markdown(
        """
#### <i class="bi bi-percent"></i>
Character Percentage
""",
        unsafe_allow_html=True,
    )

    percentage_df = build_percentage_dataframe(report)

    st.dataframe(
        percentage_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # =================================================
    # SECURITY SUMMARY
    # =================================================

    st.markdown(
        """
#### <i class="bi bi-clipboard-data-fill"></i>
Summary
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
- **Password Length:** {report['length']}
- **Uppercase Letters:** {report['uppercase']}
- **Lowercase Letters:** {report['lowercase']}
- **Numbers:** {report['digits']}
- **Special Characters:** {report['special']}
- **Character Diversity:** {report['diversity']}/4
"""
    )

    st.divider()

    # =================================================
    # SECURITY STATUS
    # =================================================

    if report["length"] >= 16 and report["diversity"] == 4:

        st.success(
            "Excellent! This password has excellent character diversity and length."
        )

    elif report["length"] >= 12 and report["diversity"] >= 3:

        st.info(
            "Good password. Adding one more character category can improve security further."
        )

    elif report["length"] >= 8:

        st.warning(
            "Average password. Increase the length and include more character types."
        )

    else:

        st.error(
            "Weak password. Use at least 12–16 characters with uppercase, lowercase, numbers and special characters."
        )

    # =================================================
    # RAW STATISTICS (Expandable)
    # =================================================

    with st.expander(
        "View Raw Statistics",
        expanded=False,
    ):

        st.json(report)

    # =================================================
    # END OF PASSWORD STATISTICS
    # =================================================