# =====================================================
# SIDEBAR
# Version 5.1 Professional
# Part 1 / 3
# =====================================================

import streamlit as st
from session import set_page

DEFAULT_LENGTH = 12


def sidebar():

    current_page = st.session_state.get("page", "generator")

    page_names = {
        "generator": "Password Generator",
        "history": "Password History",
        "dashboard": "Analytics Dashboard",
        "vault": "Password Vault",
        "favorites": "Favorite Passwords",
        "expired": "Expired Passwords",
    }

    with st.sidebar:

        # =====================================================
        # BRANDING
        # =====================================================

        st.markdown(
            """
            <h2 style="margin-bottom:0;">
                <i class="bi bi-shield-lock-fill"></i>
                Smart Password Generator
            </h2>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Secure Password Management Platform")

        st.info(
            f"**Current Page**\n\n{page_names.get(current_page, 'Password Generator')}"
        )

        st.divider()

        # =====================================================
        # PASSWORD SETTINGS
        # =====================================================

        st.markdown(
            """
            <h4>
                <i class="bi bi-sliders2"></i>
                Password Settings
            </h4>
            """,
            unsafe_allow_html=True,
        )

        password_length = st.slider(
            "Password Length",
            min_value=8,
            max_value=64,
            value=DEFAULT_LENGTH,
            key="password_length_slider",
            help="Choose the password length.",
        )

        password_count = st.number_input(
            "Number of Passwords",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            key="password_count_input",
            help="Generate multiple passwords.",
        )

        st.divider()

        # =====================================================
        # CHARACTER OPTIONS
        # =====================================================

        st.markdown(
            """
            <h4>
                <i class="bi bi-key-fill"></i>
                Character Options
            </h4>
            """,
            unsafe_allow_html=True,
        )

        use_upper = st.checkbox(
            "Uppercase Letters (A-Z)",
            value=True,
            key="use_upper",
        )

        use_lower = st.checkbox(
            "Lowercase Letters (a-z)",
            value=True,
            key="use_lower",
        )

        use_numbers = st.checkbox(
            "Numbers (0-9)",
            value=True,
            key="use_numbers",
        )

        use_symbols = st.checkbox(
            "Special Characters",
            value=True,
            key="use_symbols",
        )

        avoid_similar = st.checkbox(
            "Avoid Similar Characters",
            key="avoid_similar",
            help="Exclude characters like O, 0, l and I.",
        )

        exclude_chars = st.text_input(
            "Exclude Characters",
            placeholder="Example: O0Il",
            key="exclude_chars",
            help="Characters entered here will never appear in generated passwords.",
        )

        st.divider()

        # =====================================================
        # PASSWORD STYLE
        # =====================================================

        st.markdown(
            """
            <h4>
                <i class="bi bi-palette-fill"></i>
                Password Style
            </h4>
            """,
            unsafe_allow_html=True,
        )

        memorable = st.checkbox(
            "Generate Memorable Password",
            value=True,
            key="memorable_password",
            help="Generate passwords that are easier to remember.",
        )

        template_type = st.selectbox(
            "Template Type",
            [
                "Personal",
                "Banking",
                "Social Media",
                "Gaming",
                "WiFi",
                "Developer",
                "Business",
                "Email",
                "Shopping",
                "Entertainment",
                "Other",
            ],
            key="template_type",
            help="Choose a template based on usage.",
        )

        st.divider()

        # =====================================================
        # NAVIGATION
        # =====================================================

        st.markdown(
            """
            <h4>
                <i class="bi bi-compass-fill"></i>
                Navigation
            </h4>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Password Generator",
            icon=":material/home:",
            use_container_width=True,
            key="nav_generator",
            type="secondary",
        ):
            set_page("generator")
            st.rerun()

        if st.button(
            "Password History",
            icon=":material/history:",
            use_container_width=True,
            key="nav_history",
        ):
            set_page("history")
            st.rerun()

        if st.button(
            "Analytics Dashboard",
            icon=":material/analytics:",
            use_container_width=True,
            key="nav_dashboard",
        ):
            set_page("dashboard")
            st.rerun()

        if st.button(
            "Password Vault",
            icon=":material/folder_managed:",
            use_container_width=True,
            key="nav_vault",
        ):
            set_page("vault")
            st.rerun()

        st.divider()

        # =====================================================
        # VAULT
        # =====================================================

        st.markdown(
            """
            <h4>
                <i class="bi bi-safe2-fill"></i>
                Vault
            </h4>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Favorite Passwords",
            icon=":material/star:",
            use_container_width=True,
            key="nav_favorites",
        ):
            set_page("favorites")
            st.rerun()

        if st.button(
            "Expired Passwords",
            icon=":material/schedule:",
            use_container_width=True,
            key="nav_expired",
        ):
            set_page("expired")
            st.rerun()

        st.divider()

        # =====================================================
        # MAINTENANCE
        # =====================================================

        st.markdown(
            """
            <h4>
                <i class="bi bi-tools"></i>
                Maintenance
            </h4>
            """,
            unsafe_allow_html=True,
        )

        clear_history = st.button(
            "Clear Password History",
            icon=":material/delete_forever:",
            use_container_width=True,
            key="sidebar_clear",
            type="primary",
        )

        st.divider()

        # =====================================================
        # PROJECT INFORMATION
        # =====================================================

        st.markdown(
            """
            <h4>
                <i class="bi bi-info-circle-fill"></i>
                Project Information
            </h4>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            """
**Smart Password Generator**

Version **5.1 Professional**

**Developer:** Mohd Shahnawaz

Built with **Python • Streamlit • SQLite**
"""
        )

        st.divider()

    # =====================================================
    # RETURN SIDEBAR SETTINGS
    # =====================================================

    return {

        # -------------------------------------------------
        # Password Settings
        # -------------------------------------------------

        "password_length": password_length,
        "password_count": password_count,

        # -------------------------------------------------
        # Character Options
        # -------------------------------------------------

        "use_upper": use_upper,
        "use_lower": use_lower,
        "use_numbers": use_numbers,
        "use_symbols": use_symbols,
        "avoid_similar": avoid_similar,
        "exclude_chars": exclude_chars,

        # -------------------------------------------------
        # Password Style
        # -------------------------------------------------

        "memorable": memorable,
        "template_type": template_type,

        # -------------------------------------------------
        # Maintenance
        # -------------------------------------------------

        "clear_history": clear_history,
    }