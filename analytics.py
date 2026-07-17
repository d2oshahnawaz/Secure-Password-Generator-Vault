# =====================================================
# PASSWORD ANALYTICS DASHBOARD
# Version 4.0 Professional
# =====================================================

# -----------------------------------------------------
# Third-Party Libraries
# -----------------------------------------------------

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------------------------------
# Local Modules
# -----------------------------------------------------

from history import export_csv

from database import (
    vault_count,
    favorite_count,
    category_count,
    get_vault,
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def mask_password(password: str) -> str:
    """
    Mask a password before displaying.

    Example
    -------
    Mohd@123456
        ↓
    Mo*******56
    """

    password = str(password)

    if len(password) <= 4:
        return "*" * len(password)

    return (
        password[:2]
        + "*" * (len(password) - 4)
        + password[-2:]
    )


# =====================================================
# HISTORY DATA
# =====================================================

@st.cache_data(show_spinner=False)
def get_dashboard_data():
    """
    Load password history as a DataFrame.
    """

    try:

        df = export_csv()

    except Exception:

        return None

    if df.empty:
        return None

    # Password Length

    df["Length"] = (
        df["Password"]
        .astype(str)
        .str.len()
    )

    # Created Date

    if "Created" in df.columns:

        df["Created"] = pd.to_datetime(

            df["Created"],

            errors="coerce"

        )

    return df


# =====================================================
# VAULT DATA
# =====================================================

@st.cache_data(show_spinner=False)
def get_vault_dataframe():
    """
    Load vault data into a DataFrame.
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

@st.cache_data(show_spinner=False)
def get_category_dataframe():
    """
    Load category statistics.
    """

    try:

        data = category_count()

    except Exception:

        return pd.DataFrame(

            columns=[

                "Category",

                "Count",

            ]

        )

    if not data:

        return pd.DataFrame(

            columns=[

                "Category",

                "Count",

            ]

        )

    return pd.DataFrame(

        data,

        columns=[

            "Category",

            "Count",

        ],

    )


# =====================================================
# DASHBOARD
# =====================================================

def show_dashboard():

    st.title("Password Analytics Dashboard")

    st.caption(
        "Interactive analytics and security insights for generated passwords and vault data."
    )
    
    # =====================================================
    # LOAD DATA
    # =====================================================

    history_df = get_dashboard_data()

    vault_df = get_vault_dataframe()

    category_df = get_category_dataframe()

    # =====================================================
    # NO DATA AVAILABLE
    # =====================================================

    if history_df is None and vault_df.empty:

        st.info(
            "No analytics data available. Generate or save passwords to view analytics."
        )

        return

    # =====================================================
    # DEFAULT VALUES
    # =====================================================

    history_total = 0

    vault_total = vault_count()

    favorites = favorite_count()

    category_total = len(category_df)

    avg_entropy = 0.0

    avg_length = 0.0

    strong_passwords = 0

    weak_passwords = 0

    medium_passwords = 0

    # =====================================================
    # HISTORY ANALYTICS
    # =====================================================

    if history_df is not None:

        history_total = len(history_df)

        avg_entropy = round(

            history_df["Entropy"].mean(),

            2

        )

        avg_length = round(

            history_df["Length"].mean(),

            2

        )

        strong_passwords = len(

            history_df[

                history_df["Strength"].str.contains(

                    "Strong|Excellent|Very",

                    case=False,

                    na=False

                )

            ]

        )

        medium_passwords = len(

            history_df[

                history_df["Strength"].str.contains(

                    "Medium",

                    case=False,

                    na=False

                )

            ]

        )

        weak_passwords = max(

            history_total

            - strong_passwords

            - medium_passwords,

            0

        )

    # =====================================================
    # DASHBOARD OVERVIEW
    # =====================================================

    st.subheader("Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Generated",

            history_total

        )

    with c2:

        st.metric(

            "Vault",

            vault_total

        )

    with c3:

        st.metric(

            "Favorites",

            favorites

        )

    with c4:

        st.metric(

            "Categories",

            category_total

        )

    c5, c6, c7, c8 = st.columns(4)

    with c5:

        st.metric(

            "Average Entropy",

            f"{avg_entropy} bits"

        )

    with c6:

        st.metric(

            "Average Length",

            f"{avg_length}"

        )

    with c7:

        st.metric(

            "Strong",

            strong_passwords

        )

    with c8:

        st.metric(

            "Weak",

            weak_passwords

        )

    st.divider()
    
    # =====================================================
    # PASSWORD STRENGTH DISTRIBUTION
    # =====================================================

    if history_df is not None:

        st.subheader("Password Strength Distribution")

        fig = px.pie(

            history_df,

            names="Strength",

            hole=0.45,

            title="Password Strength"

        )

        fig.update_layout(

            template="plotly_white",

            legend_title_text="Strength",

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # =====================================================
    # PASSWORD ENTROPY DISTRIBUTION
    # =====================================================

    if history_df is not None:

        st.subheader("Entropy Distribution")

        fig = px.histogram(

            history_df,

            x="Entropy",

            nbins=20,

            title="Password Entropy"

        )

        fig.update_layout(

            template="plotly_white",

            bargap=0.10,

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # =====================================================
    # PASSWORD LENGTH DISTRIBUTION
    # =====================================================

    if history_df is not None:

        st.subheader("Password Length Distribution")

        fig = px.histogram(

            history_df,

            x="Length",

            nbins=15,

            title="Password Length"

        )

        fig.update_layout(

            template="plotly_white",

            bargap=0.10,

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()
    
    # =====================================================
    # PASSWORD GENERATION TIMELINE
    # =====================================================

    if history_df is not None:

        if "Created" in history_df.columns:

            timeline = (

                history_df

                .dropna(subset=["Created"])

                .groupby(

                    history_df["Created"].dt.date

                )

                .size()

                .reset_index(name="Count")

            )

            if len(timeline) > 1:

                st.subheader(
                    "Password Generation Timeline"
                )

                fig = px.line(

                    timeline,

                    x="Created",

                    y="Count",

                    markers=True,

                    title="Passwords Generated Over Time"

                )

                fig.update_layout(

                    template="plotly_white",

                    xaxis_title="Date",

                    yaxis_title="Passwords",

                    margin=dict(
                        l=20,
                        r=20,
                        t=50,
                        b=20
                    )

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

    st.divider()

    # =====================================================
    # CATEGORY ANALYTICS
    # =====================================================

    if not category_df.empty:

        st.subheader(
            "Vault Category Analytics"
        )

        left_chart, right_chart = st.columns(2)

        # ---------------------------------------------
        # CATEGORY PIE CHART
        # ---------------------------------------------

        with left_chart:

            fig = px.pie(

                category_df,

                names="Category",

                values="Count",

                hole=0.45,

                title="Category Distribution"

            )

            fig.update_layout(

                template="plotly_white",

                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                )

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

        # ---------------------------------------------
        # CATEGORY BAR CHART
        # ---------------------------------------------

        with right_chart:

            fig = px.bar(

                category_df,

                x="Category",

                y="Count",

                text="Count",

                title="Passwords per Category"

            )

            fig.update_traces(

                textposition="outside"

            )

            fig.update_layout(

                template="plotly_white",

                xaxis_title="Category",

                yaxis_title="Passwords",

                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                )

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

    st.divider()
    
    # =====================================================
    # FAVORITES ANALYTICS
    # =====================================================

    st.subheader("Favorites Overview")

    favorite = favorite_count()

    normal = max(
        vault_total - favorite,
        0
    )

    favorite_df = pd.DataFrame(
        {
            "Type": [
                "Favorites",
                "Others"
            ],
            "Count": [
                favorite,
                normal
            ]
        }
    )

    fig = px.pie(

        favorite_df,

        names="Type",

        values="Count",

        hole=0.45,

        title="Favorite Passwords"

    )

    fig.update_layout(

        template="plotly_white",

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # =====================================================
    # WEBSITE ANALYTICS
    # =====================================================

    if not vault_df.empty:

        st.subheader(
            "Website Analytics"
        )

        website_df = (

            vault_df

            .groupby("Website")

            .size()

            .reset_index(name="Count")

            .sort_values(

                "Count",

                ascending=False

            )

            .head(10)

        )

        fig = px.bar(

            website_df,

            x="Website",

            y="Count",

            text="Count",

            title="Top Websites"

        )

        fig.update_traces(

            textposition="outside"

        )

        fig.update_layout(

            template="plotly_white",

            xaxis_title="Website",

            yaxis_title="Passwords",

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # =====================================================
    # RECENT VAULT ENTRIES
    # =====================================================

    if not vault_df.empty:

        st.subheader(
            "Recent Vault Entries"
        )

        table = vault_df.copy()

        table = table.sort_values(

            "Created",

            ascending=False

        )

        table["Encrypted Password"] = (

            table["Encrypted Password"]

            .apply(mask_password)

        )

        st.dataframe(

            table[
                [

                    "Website",

                    "Username",

                    "Category",

                    "Tags",

                    "Favorite",

                    "Created"

                ]

            ],

            hide_index=True,

            use_container_width=True

        )

    st.divider()
    
    # =====================================================
    # SECURITY INSIGHTS
    # =====================================================

    st.subheader("Security Insights")

    insights = []

    if history_df is not None:

        if avg_entropy < 60:

            insights.append(
                (
                    "warning",
                    "Increase password entropy for stronger security."
                )
            )

        if avg_length < 12:

            insights.append(
                (
                    "warning",
                    "Use passwords with at least 12 characters."
                )
            )

        if strong_passwords < max(history_total * 0.70, 1):

            insights.append(
                (
                    "warning",
                    "Generate more Strong or Excellent passwords."
                )
            )

    if favorites == 0:

        insights.append(
            (
                "info",
                "Mark important passwords as Favorites for quick access."
            )
        )

    if category_df.empty:

        insights.append(
            (
                "info",
                "Organize your vault using categories."
            )
        )

    if vault_total == 0:

        insights.append(
            (
                "info",
                "Save generated passwords to the encrypted vault."
            )
        )

    if not insights:

        st.success(
            "Excellent! No security issues detected."
        )

    else:

        for level, message in insights:

            with st.container(border=True):

                if level == "warning":

                    st.warning(message)

                else:

                    st.info(message)

    st.divider()

    # =====================================================
    # DASHBOARD HEALTH SCORE
    # =====================================================

    score = 100

    if avg_entropy < 60:
        score -= 20

    if avg_length < 12:
        score -= 20

    if favorites == 0:
        score -= 10

    if category_df.empty:
        score -= 10

    if vault_total == 0:
        score -= 20

    score = max(score, 0)

    st.subheader("Dashboard Health Score")

    st.progress(score / 100)

    st.metric(
        "Overall Security Score",
        f"{score}/100"
    )

    st.divider()

    # =====================================================
    # DASHBOARD SUMMARY
    # =====================================================

    st.subheader("Dashboard Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "History Passwords",
            history_total
        )

        st.metric(
            "Vault Passwords",
            vault_total
        )

    with c2:

        st.metric(
            "Favorites",
            favorites
        )

        st.metric(
            "Categories",
            category_total
        )

    with c3:

        st.metric(
            "Average Entropy",
            f"{avg_entropy} bits"
        )

        st.metric(
            "Average Length",
            avg_length
        )

    st.divider()

    # =====================================================
    # QUICK RECOMMENDATIONS
    # =====================================================

    st.subheader("Recommendations")

    recommendations = [

        "Use passwords with at least 12–16 characters.",

        "Include uppercase, lowercase, numbers and symbols.",

        "Use a unique password for every account.",

        "Store passwords in the encrypted vault.",

        "Review your vault periodically.",

        "Replace weak passwords immediately."

    ]

    for item in recommendations:

        st.markdown(f"- {item}")

    st.divider()

    # =====================================================
    # FOOTER
    # =====================================================

    st.caption(
        "Smart Password Generator • Version 4.0 Professional"
    )