# =====================================================
# PASSWORD STATISTICS
# Version 4.1 Professional
# =====================================================

from __future__ import annotations

from typing import Dict

import plotly.express as px
import pandas as pd
import streamlit as st

from generator import password_stats

# =====================================================
# DISPLAY PASSWORD STATISTICS
# =====================================================

def show_password_stats(password: str) -> None:
    """
    Display detailed password statistics.
    """

    stats: Dict[str, int] = password_stats(password)

    st.markdown(
        """
### <i class="bi bi-bar-chart-fill"></i> Password Statistics
""",
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Length",
            stats["length"],
        )

        st.metric(
            "Uppercase",
            stats["uppercase"],
        )

    with col2:

        st.metric(
            "Lowercase",
            stats["lowercase"],
        )

        st.metric(
            "Numbers",
            stats["digits"],
        )

    with col3:

        st.metric(
            "Special",
            stats["special"],
        )

        diversity = sum([

            stats["uppercase"] > 0,

            stats["lowercase"] > 0,

            stats["digits"] > 0,

            stats["special"] > 0,

        ])

        st.metric(
            "Types",
            f"{diversity}/4",
        )

    st.divider()

    # -------------------------------------------------
    # Character Distribution
    # -------------------------------------------------

    chart_df = pd.DataFrame({

        "Category": [

            "Uppercase",

            "Lowercase",

            "Numbers",

            "Special",

        ],

        "Count": [

            stats["uppercase"],

            stats["lowercase"],

            stats["digits"],

            stats["special"],

        ],

    })

    fig = px.pie(

        chart_df,

        names="Category",

        values="Count",

        hole=0.60,

        title=f"Character Distribution ({stats['length']} Characters)",

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

        legend_title="Category",

        uirevision=str(hash(password)),

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.divider()

    # -------------------------------------------------
    # Character Diversity
    # -------------------------------------------------

    st.markdown(
        "#### Character Diversity"
    )

    progress = diversity / 4

    st.progress(

        progress,

        text=f"{diversity}/4 Character Types Used"

    )

    if diversity == 4:

        st.success(

            "Excellent! All four character categories are used."

        )

    elif diversity == 3:

        st.info(

            "Good diversity. Consider using all character categories."

        )

    elif diversity == 2:

        st.warning(

            "Moderate diversity. Add more character types."

        )

    else:

        st.error(

            "Poor diversity. Password should include uppercase, lowercase, numbers and symbols."

        )

    st.divider()

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    st.markdown(
        "#### Summary"
    )

    summary = [

        f"• Total Length : **{stats['length']}**",

        f"• Uppercase Letters : **{stats['uppercase']}**",

        f"• Lowercase Letters : **{stats['lowercase']}**",

        f"• Numbers : **{stats['digits']}**",

        f"• Special Characters : **{stats['special']}**",

    ]

    st.markdown("\n".join(summary))