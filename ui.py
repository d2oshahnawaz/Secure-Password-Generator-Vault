# =====================================================
# UI FUNCTIONS
# Version 5.0 Professional
# =====================================================

import streamlit as st

from database import (
    get_history,
    search_history,
    delete_history,
)

from history import (
    export_csv,
    export_txt,
    export_json,
    export_excel
)

from clipboard import render_copy_button


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def mask_password(password: str) -> str:
    """
    Mask password before displaying.

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
# PASSWORD HISTORY
# =====================================================

def show_history():

    st.header("Password History")

    st.caption(
        "Search, review and manage your generated passwords."
    )

    st.divider()

    # =================================================
    # SEARCH + FILTER
    # =================================================

    col1, col2 = st.columns([3, 1])

    with col1:

        keyword = st.text_input(
            "Search Password",
            placeholder="Search password...",
            key="history_search",
        )

    with col2:

        filter_option = st.selectbox(
            "Filter",
            [
                "All",
                "Strong",
                "Medium",
                "Weak",
            ],
            key="history_filter",
        )

    # =================================================
    # LOAD HISTORY
    # =================================================

    if keyword.strip():

        history = search_history(keyword.strip())

    else:

        history = get_history()

    if not history:

        st.info(
            "No password history available."
        )

        return

    # =================================================
    # FILTER HISTORY
    # =================================================

    if filter_option != "All":

        history = [

            row

            for row in history

            if filter_option.lower()
            in row[2].lower()

        ]

    # =================================================
    # METRICS
    # =================================================

    metric1, metric2 = st.columns(2)

    with metric1:

        st.metric(
            "Total Passwords",
            len(history),
        )

    with metric2:

        st.metric(
            "Showing",
            min(len(history), 20),
        )

    st.caption(
        "Displaying latest 20 passwords."
    )

    history = history[:20]

    st.divider()

    # =================================================
    # HISTORY CARDS
    # =================================================

    for row in history:

        with st.container(border=True):

            left, right = st.columns([4, 1])

            with left:

                st.subheader(
                    mask_password(row[1])
                )

            with right:

                st.metric(
                    "Strength",
                    row[2],
                )

            st.code(
                row[1],
                language="text",
            )

            # =================================================
            # PASSWORD DETAILS
            # =================================================

            detail1, detail2, detail3 = st.columns(3)

            with detail1:

                st.metric(
                    "Entropy",
                    f"{row[3]:.2f} bits",
                )

            with detail2:

                st.metric(
                    "Crack Time",
                    row[4],
                )

            with detail3:

                st.write("Created")

                st.caption(
                    str(row[5])
                )

            st.divider()

            # =================================================
            # ACTION BUTTONS
            # =================================================

            copy_col, delete_col = st.columns(2)

            # ---------------------------------------------
            # COPY PASSWORD
            # ---------------------------------------------

            with copy_col:

                render_copy_button(
                    password=row[1],
                    key=f"history_{row[0]}"
                )

            # ---------------------------------------------
            # DELETE PASSWORD
            # ---------------------------------------------

            with delete_col:

                if st.button(
                    "Delete Password",
                    key=f"delete_history_{row[0]}",
                    use_container_width=True,
                    type="secondary",
                ):

                    delete_history(row[0])

                    st.success(
                        "Password deleted successfully."
                    )

                    st.rerun()

    # =================================================
    # END OF PASSWORD HISTORY
    # =================================================

    st.success(
        f"Showing {len(history)} password(s)."
    )

    st.divider()

    # =====================================================
# EXPORT PASSWORD HISTORY
# =====================================================

def show_export():

    st.header("Export Password History")

    st.caption(
        "Download your password history in multiple formats."
    )

    st.divider()

    history_df = export_csv()

    if history_df.empty:

        st.info(
            "No password history available to export."
        )

        return

    total_records = len(history_df)

    metric1, metric2 = st.columns(2)

    with metric1:

        st.metric(
            "Available Records",
            total_records
        )

    with metric2:

        st.metric(
            "Export Formats",
            "4"
        )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    # ==========================================
    # CSV
    # ==========================================

    with col1:

        st.download_button(

            label="Download CSV",

            data=history_df.to_csv(index=False),

            file_name="password_history.csv",

            mime="text/csv",

            use_container_width=True,

            type="primary"

        )

    # ==========================================
    # TXT
    # ==========================================

    with col2:

        st.download_button(

            label="Download TXT",

            data=export_txt(),

            file_name="password_history.txt",

            mime="text/plain",

            use_container_width=True

        )

    # ==========================================
    # JSON
    # ==========================================

    with col3:

        st.download_button(

            label="Download JSON",

            data=export_json(),

            file_name="password_history.json",

            mime="application/json",

            use_container_width=True

        )
        
    # ==========================================
    # EXCEL
    # ==========================================

    with col4:

        st.download_button(

            label="Download Excel",

            data=export_excel(),

            file_name="password_history.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )

    st.success(
        "Export is ready. Choose any format to download."
    )

    st.divider()

    with st.expander(
        "Export Information",
        expanded=False
    ):

        st.markdown("""

**CSV**
- Spreadsheet compatible
- Microsoft Excel
- Google Sheets

**Excel (.xlsx)**
- Native Microsoft Excel format
- Preserves table structure
- Best for reports and analysis

**TXT**
- Plain text format
- Lightweight
- Easy to read

**JSON**
- Structured data
- Developer friendly
- Suitable for backups

        """)

# =====================================================
# EMPTY PAGE
# =====================================================

def empty_page(message: str):

    st.info(message)


# =====================================================
# SECTION TITLE
# =====================================================

def section_title(title: str):

    st.header(title)

    st.divider()


# =====================================================
# PROFESSIONAL FOOTER
# =====================================================

def show_footer():

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.caption("Smart Password Generator")

        st.caption("Secure • Fast • Reliable")

    with col2:

        st.caption("Version 5.0 Professional")

        st.caption("Python • Streamlit • SQLite")

    with col3:

        st.caption("Developed by")

        st.caption("© 2026 Mohd Shahnawaz")

    st.divider()

    st.markdown(
        """
<div style="text-align:center;
font-size:13px;
color:#9ca3af;
padding-top:5px;
padding-bottom:5px;">

Built with ❤️ using
<strong>Python</strong>,
<strong>Streamlit</strong>,
<strong>SQLite</strong>,
<strong>Cryptography</strong>,
<strong>Pandas</strong>,
<strong>Plotly</strong> &
<strong>zxcvbn</strong>

</div>
""",
        unsafe_allow_html=True,
    )


# =====================================================
# PAGE NOT AVAILABLE
# =====================================================

def page_not_ready():

    st.warning(
        """
This feature is currently under development.

It will be available in an upcoming release.
"""
    )


# =====================================================
# VERSION INFORMATION
# =====================================================

def show_version():

    with st.expander("Application Information", expanded=False):

        st.markdown(
            """
### Smart Password Generator

**Version:** 5.0 Professional

#### Features

- Secure Password Generator
- Password Strength Analysis
- Password Vault
- Password History
- Analytics Dashboard
- Password Export
- Browser Clipboard Support
- Streamlit Cloud Compatible
- SQLite Database
- Modern Responsive UI

#### Technologies

- Python
- Streamlit
- SQLite
- Cryptography
- Plotly
- Pandas
- zxcvbn
"""
        )


# =====================================================
# END OF FILE
# =====================================================