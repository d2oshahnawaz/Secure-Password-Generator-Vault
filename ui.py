# =====================================================
# UI FUNCTIONS
# Version 4.0 Professional
# =====================================================

import streamlit as st
import pyperclip

from database import (
    get_history,
    search_history,
    delete_history,
)

from history import (
    export_csv,
    export_txt,
    export_json,
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def mask_password(password: str) -> str:
    """
    Mask password before displaying.

    Example:
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
        "Search, review and manage generated passwords."
    )

    st.divider()

    # ==========================================
    # SEARCH + FILTER
    # ==========================================

    left, right = st.columns([3, 1])

    with left:

        keyword = st.text_input(
            "Search",
            placeholder="Search password...",
            key="history_search"
        )

    with right:

        filter_option = st.selectbox(

            "Filter",

            [

                "All",

                "Strong",

                "Medium",

                "Weak"

            ],

            key="history_filter"

        )

    # ==========================================
    # LOAD HISTORY
    # ==========================================

    if keyword:

        history = search_history(keyword)

    else:

        history = get_history()

    if not history:

        st.info(
            "No password history available."
        )

        return

    # ==========================================
    # FILTER DATA
    # ==========================================

    if filter_option != "All":

        history = [

            row

            for row in history

            if filter_option.lower()

            in row[2].lower()

        ]

    # ==========================================
    # METRICS
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Total Passwords",

            len(history)

        )

    with col2:

        st.metric(

            "Showing",

            min(len(history), 20)

        )

    st.caption(
        "Displaying latest 20 records."
    )

    history = history[:20]

    st.divider()

    # ==========================================
    # HISTORY CARDS
    # ==========================================

    for row in history:

        with st.container(border=True):

            top_left, top_right = st.columns([4, 1])

            with top_left:

                st.subheader(
                    mask_password(row[1])
                )

            with top_right:

                st.metric(
                    "Strength",
                    row[2]
                )

            st.code(
                row[1],
                language="text"
            )
            # ==========================================
            # PASSWORD DETAILS
            # ==========================================

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Entropy",
                    f"{row[3]:.2f} bits"
                )

            with c2:

                st.metric(
                    "Crack Time",
                    row[4]
                )

            with c3:

                st.write("Created")

                st.caption(
                    str(row[5])
                )

            st.divider()

            # ==========================================
            # ACTION BUTTONS
            # ==========================================

            btn1, btn2 = st.columns(2)

            # -----------------------------
            # COPY
            # -----------------------------

            with btn1:

                if st.button(

                    "Copy",

                    key=f"copy_history_{row[0]}",

                    use_container_width=True

                ):

                    try:

                        pyperclip.copy(row[1])

                        st.success(
                            "Password copied successfully."
                        )

                    except Exception:

                        st.code(
                            row[1],
                            language="text"
                        )

                        st.info(
                            "Clipboard unavailable. Copy manually."
                        )

            # -----------------------------
            # DELETE
            # -----------------------------

            with btn2:

                if st.button(

                    "Delete",

                    key=f"delete_history_{row[0]}",

                    use_container_width=True

                ):

                    delete_history(row[0])

                    st.success(
                        "Password deleted successfully."
                    )

                    st.rerun()
# =====================================================
# EXPORT PASSWORD HISTORY
# =====================================================

def show_export():

    st.divider()

    st.header("Export Password History")

    st.caption(
        "Download your password history in different formats."
    )

    csv_data = export_csv()

    col1, col2, col3 = st.columns(3)

    # ==========================================
    # CSV
    # ==========================================

    with col1:

        st.download_button(

            label="Download CSV",

            data=csv_data.to_csv(index=False),

            file_name="password_history.csv",

            mime="text/csv",

            use_container_width=True

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


# =====================================================
# EMPTY PAGE
# =====================================================

def empty_page(message):

    st.info(message)


# =====================================================
# SECTION TITLE
# =====================================================

def section_title(title):

    st.header(title)

    st.divider()


# =====================================================
# FOOTER
# =====================================================

def show_footer():

    st.divider()

    left, center, right = st.columns(3)

    with left:

        st.caption(
            "Smart Password Generator"
        )

    with center:

        st.caption(
            "Version 4.0"
        )

    with right:

        st.caption(
            "© 2026 Mohd Shahnawaz"
        )

    st.caption(
        "Built with Python • Streamlit • SQLite • Cryptography"
    )


# =====================================================
# PAGE NOT AVAILABLE
# =====================================================

def page_not_ready():

    st.info(
        "This feature will be available in a future update."
    )
    
