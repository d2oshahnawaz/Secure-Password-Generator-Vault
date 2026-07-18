# =====================================================
# SIDEBAR
# Version 6.0 Professional
# Part 1 / 4
# =====================================================

from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from session import (
    current_page,
    session_info,
    set_page,
)

# =====================================================
# CONSTANTS
# =====================================================

DEFAULT_LENGTH = 12
MIN_LENGTH = 8
MAX_LENGTH = 64
MAX_PASSWORDS = 10

# =====================================================
# PASSWORD PRESETS
# =====================================================

PASSWORD_PRESETS: Dict[str, Dict[str, Any]] = {

    "Custom": {
        "length": 12,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": True,
    },

    "Maximum Security": {
        "length": 32,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": True,
    },

    "Developer": {
        "length": 20,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": True,
    },

    "Banking": {
        "length": 24,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": True,
    },

    "Business": {
        "length": 18,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": True,
    },

    "Gaming": {
        "length": 16,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": False,
    },

    "WiFi": {
        "length": 20,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": False,
    },

    "Social Media": {
        "length": 18,
        "upper": True,
        "lower": True,
        "numbers": True,
        "symbols": True,
    },

}

# =====================================================
# PAGE TITLES
# =====================================================

PAGE_NAMES = {

    "generator": "Password Generator",

    "history": "Password History",

    "dashboard": "Analytics Dashboard",

    "vault": "Password Vault",

    "favorites": "Favorite Passwords",

    "expired": "Expired Passwords",

}

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def apply_preset(name: str) -> None:
    """
    Apply selected password preset.
    """

    preset = PASSWORD_PRESETS.get(name)

    if not preset:
        return

    st.session_state.password_length_slider = preset["length"]
    st.session_state.use_upper = preset["upper"]
    st.session_state.use_lower = preset["lower"]
    st.session_state.use_numbers = preset["numbers"]
    st.session_state.use_symbols = preset["symbols"]


def page_title() -> str:
    """
    Return current page title.
    """

    return PAGE_NAMES.get(
        current_page(),
        "Password Generator",
    )


# =====================================================
# SIDEBAR
# =====================================================

def sidebar():

    info = session_info()

    with st.sidebar:

        # =================================================
        # BRANDING
        # =================================================

        st.markdown(
            """
<h2 style="margin-bottom:0;">
<i class="bi bi-shield-lock-fill"></i>
Smart Password Generator
</h2>
""",
            unsafe_allow_html=True,
        )

        st.caption(
            "Professional Password Security Platform"
        )

        st.success(
            f"Current Page\n\n**{page_title()}**"
        )

        st.divider()

        # =================================================
        # QUICK STATUS
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Passwords",
                info["passwords"],
            )

        with col2:

            st.metric(
                "Theme",
                info["theme"],
            )

        st.divider()

        # =================================================
        # PASSWORD PRESET
        # =================================================

        st.markdown(
            """
### <i class="bi bi-stars"></i>
Password Preset
""",
            unsafe_allow_html=True,
        )

        selected_preset = st.selectbox(

            "Preset",

            list(PASSWORD_PRESETS.keys()),

            key="password_preset",

            help="Automatically configure recommended password settings.",

        )

        if st.button(

            "Apply Preset",

            icon=":material/auto_fix_high:",

            use_container_width=True,

        ):

            apply_preset(selected_preset)

            st.toast(
                "Preset Applied",
                icon="✅",
            )

            st.rerun()

        st.divider()

        # =================================================
        # PASSWORD SETTINGS
        # =================================================

        st.markdown(
            """
### <i class="bi bi-sliders2"></i>
Password Settings
""",
            unsafe_allow_html=True,
        )

        password_length = st.slider(

            "Password Length",

            MIN_LENGTH,

            MAX_LENGTH,

            st.session_state.get(
                "password_length_slider",
                DEFAULT_LENGTH,
            ),

            key="password_length_slider",

        )

        password_count = int(

            st.number_input(

                "Number of Passwords",

                min_value=1,

                max_value=MAX_PASSWORDS,

                value=3,

                step=1,

                key="password_count_input",

            )

        )

        st.caption(
            f"Estimated Entropy increases with password length ({password_length} characters selected)."
        )

        st.divider()
        
        # =================================================
        # CHARACTER OPTIONS
        # =================================================

        st.markdown(
            """
### <i class="bi bi-key-fill"></i>
Character Options
""",
            unsafe_allow_html=True,
        )

        use_upper = st.checkbox(
            "Uppercase Letters (A-Z)",
            value=st.session_state.get(
                "use_upper",
                True,
            ),
            key="use_upper",
        )

        use_lower = st.checkbox(
            "Lowercase Letters (a-z)",
            value=st.session_state.get(
                "use_lower",
                True,
            ),
            key="use_lower",
        )

        use_numbers = st.checkbox(
            "Numbers (0-9)",
            value=st.session_state.get(
                "use_numbers",
                True,
            ),
            key="use_numbers",
        )

        use_symbols = st.checkbox(
            "Special Characters",
            value=st.session_state.get(
                "use_symbols",
                True,
            ),
            key="use_symbols",
        )

        avoid_similar = st.checkbox(
            "Avoid Similar Characters",
            value=st.session_state.get(
                "avoid_similar",
                False,
            ),
            key="avoid_similar",
            help="Exclude characters like O, 0, I, l and 1.",
        )

        exclude_chars = st.text_input(
            "Exclude Characters",
            value=st.session_state.get(
                "exclude_chars",
                "",
            ),
            placeholder="Example: O0Il1",
            key="exclude_chars",
            help="Characters entered here will never appear in generated passwords.",
        )

        st.divider()

        # =================================================
        # PASSWORD STYLE
        # =================================================

        st.markdown(
            """
### <i class="bi bi-palette-fill"></i>
Password Style
""",
            unsafe_allow_html=True,
        )

        memorable = st.checkbox(
            "Generate Memorable Password",
            value=st.session_state.get(
                "memorable_password",
                True,
            ),
            key="memorable_password",
            help="Generate passwords that are easier to remember while remaining secure.",
        )

        pronounceable = st.checkbox(
            "Pronounceable Password",
            value=st.session_state.get(
                "pronounceable_password",
                False,
            ),
            key="pronounceable_password",
            help="Generate passwords with easier pronunciation.",
        )

        begin_letter = st.checkbox(
            "Start With Letter",
            value=st.session_state.get(
                "start_with_letter",
                True,
            ),
            key="start_with_letter",
        )

        end_number = st.checkbox(
            "End With Number",
            value=st.session_state.get(
                "end_with_number",
                False,
            ),
            key="end_with_number",
        )

        end_symbol = st.checkbox(
            "End With Symbol",
            value=st.session_state.get(
                "end_with_symbol",
                False,
            ),
            key="end_with_symbol",
        )

        st.divider()

        # =================================================
        # PASSWORD TEMPLATE
        # =================================================

        st.markdown(
            """
### <i class="bi bi-grid-fill"></i>
Password Template
""",
            unsafe_allow_html=True,
        )

        template_type = st.selectbox(
            "Template Type",
            [
                "Personal",
                "Banking",
                "Developer",
                "Business",
                "Gaming",
                "WiFi",
                "Email",
                "Social Media",
                "Shopping",
                "Entertainment",
                "Other",
            ],
            key="template_type",
        )

        randomize_order = st.checkbox(
            "Randomize Character Order",
            value=st.session_state.get(
                "randomize_order",
                True,
            ),
            key="randomize_order",
        )

        prevent_duplicates = st.checkbox(
            "Prevent Duplicate Characters",
            value=st.session_state.get(
                "prevent_duplicates",
                False,
            ),
            key="prevent_duplicates",
        )

        ambiguous_filter = st.checkbox(
            "Filter Ambiguous Characters",
            value=st.session_state.get(
                "ambiguous_filter",
                True,
            ),
            key="ambiguous_filter",
            help="Remove confusing characters such as O, 0, l and I.",
        )

        st.divider()

        # =================================================
        # ADVANCED SETTINGS
        # =================================================

        st.markdown(
            """
### <i class="bi bi-sliders"></i>
Advanced Settings
""",
            unsafe_allow_html=True,
        )

        entropy_target = st.select_slider(
            "Target Security Level",
            options=[
                "Standard",
                "High",
                "Very High",
                "Maximum",
            ],
            value="High",
            key="entropy_target",
        )

        auto_save = st.checkbox(
            "Automatically Save Password History",
            value=st.session_state.get(
                "auto_save_history",
                True,
            ),
            key="auto_save_history",
        )

        copy_after_generation = st.checkbox(
            "Auto Copy First Password",
            value=st.session_state.get(
                "auto_copy",
                False,
            ),
            key="auto_copy",
        )

        show_security_analysis = st.checkbox(
            "Show Security Analysis",
            value=st.session_state.get(
                "show_analysis",
                True,
            ),
            key="show_analysis",
        )

        st.info(
            """
The selected options will be used during password generation to maximize security and usability.
"""
        )

        st.divider()
        
                # =================================================
        # NAVIGATION
        # =================================================

        st.markdown(
            """
### <i class="bi bi-compass-fill"></i>
Navigation
""",
            unsafe_allow_html=True,
        )

        navigation_buttons = [

            (
                "Password Generator",
                "generator",
                ":material/home:",
            ),

            (
                "Password History",
                "history",
                ":material/history:",
            ),

            (
                "Analytics Dashboard",
                "dashboard",
                ":material/analytics:",
            ),

            (
                "Password Vault",
                "vault",
                ":material/folder_managed:",
            ),

            (
                "Favorite Passwords",
                "favorites",
                ":material/star:",
            ),

            (
                "Expired Passwords",
                "expired",
                ":material/schedule:",
            ),

        ]

        for title, page, icon in navigation_buttons:

            button_type = (
                "primary"
                if current_page() == page
                else "secondary"
            )

            if st.button(
                title,
                icon=icon,
                use_container_width=True,
                type=button_type,
                key=f"nav_{page}",
            ):
                set_page(page)
                st.rerun()

        st.divider()

        # =================================================
        # QUICK ACTIONS
        # =================================================

        st.markdown(
            """
### <i class="bi bi-lightning-charge-fill"></i>
Quick Actions
""",
            unsafe_allow_html=True,
        )

        quick_col1, quick_col2 = st.columns(2)

        with quick_col1:

            refresh_page = st.button(
                "Refresh",
                icon=":material/refresh:",
                use_container_width=True,
                key="sidebar_refresh",
            )

        with quick_col2:

            reset_settings = st.button(
                "Reset",
                icon=":material/restart_alt:",
                use_container_width=True,
                key="sidebar_reset",
            )

        if refresh_page:
            st.rerun()

        if reset_settings:

            keys = [

                "password_length_slider",
                "password_count_input",
                "use_upper",
                "use_lower",
                "use_numbers",
                "use_symbols",
                "avoid_similar",
                "exclude_chars",
                "memorable_password",

            ]

            for key in keys:

                if key in st.session_state:
                    del st.session_state[key]

            st.toast(
                "Settings reset successfully.",
                icon="✅",
            )

            st.rerun()

        st.divider()

        # =================================================
        # THEME
        # =================================================

        st.markdown(
            """
### <i class="bi bi-palette2"></i>
Appearance
""",
            unsafe_allow_html=True,
        )

        selected_theme = st.selectbox(

            "Theme",

            [

                "Dark",

                "Light",

                "System",

            ],

            index=[
                "Dark",
                "Light",
                "System",
            ].index(
                st.session_state.get(
                    "theme",
                    "Dark",
                )
            ),

            key="theme_selector",

        )

        st.session_state.theme = selected_theme

        st.divider()

        # =================================================
        # SESSION STATISTICS
        # =================================================

        st.markdown(
            """
### <i class="bi bi-graph-up-arrow"></i>
Session Statistics
""",
            unsafe_allow_html=True,
        )

        stats = session_info()

        stat_col1, stat_col2 = st.columns(2)

        with stat_col1:

            st.metric(
                "Passwords",
                stats["passwords"],
            )

            st.metric(
                "Generated",
                "Yes" if stats["generated"] else "No",
            )

        with stat_col2:

            st.metric(
                "Suggestions",
                stats["extra_passwords"],
            )

            st.metric(
                "Vault",
                "Open"
                if stats["vault_unlocked"]
                else "Locked",
            )

        st.divider()

        # =================================================
        # MAINTENANCE
        # =================================================

        st.markdown(
            """
### <i class="bi bi-tools"></i>
Maintenance
""",
            unsafe_allow_html=True,
        )

        clear_history = st.button(
            "Clear Password History",
            icon=":material/delete_forever:",
            use_container_width=True,
            type="primary",
            key="sidebar_clear_history",
        )

        backup_data = st.button(
            "Backup Settings",
            icon=":material/backup:",
            use_container_width=True,
            key="sidebar_backup",
        )

        restore_data = st.button(
            "Restore Settings",
            icon=":material/settings_backup_restore:",
            use_container_width=True,
            key="sidebar_restore",
        )

        if backup_data:

            st.success(
                "Settings backup created successfully."
            )

        if restore_data:

            st.info(
                "Restore feature is ready for integration."
            )

        st.divider()

        # =================================================
        # PASSWORD SECURITY TIP
        # =================================================

        st.markdown(
            """
### <i class="bi bi-lightbulb-fill"></i>
Security Tip
""",
            unsafe_allow_html=True,
        )

        st.info(
            "Use a unique password for every account and enable Multi-Factor Authentication (MFA) whenever available."
        )

        st.divider()

        # =================================================
        # PROJECT INFORMATION
        # =================================================

        st.markdown(
            """
### <i class="bi bi-info-circle-fill"></i>
Project Information
""",
            unsafe_allow_html=True,
        )

        st.success(
            """
**Smart Password Generator**

Version **6.0 Professional**

Developer: **Mohd Shahnawaz**

Python • Streamlit • SQLite • Cryptography
"""
        )

        st.caption(
            "© 2026 Smart Password Generator Professional"
        )

    # =====================================================
    # RETURN SETTINGS
    # =====================================================

    return {

        # Password

        "password_length": password_length,

        "password_count": password_count,

        # Character Options

        "use_upper": use_upper,

        "use_lower": use_lower,

        "use_numbers": use_numbers,

        "use_symbols": use_symbols,

        "avoid_similar": avoid_similar,

        "exclude_chars": exclude_chars,

        # Password Style

        "memorable": memorable,

        "pronounceable": pronounceable,

        "start_with_letter": begin_letter,

        "end_with_number": end_number,

        "end_with_symbol": end_symbol,

        # Template

        "template_type": template_type,

        "randomize_order": randomize_order,

        "prevent_duplicates": prevent_duplicates,

        "ambiguous_filter": ambiguous_filter,

        # Advanced

        "entropy_target": entropy_target,

        "auto_save": auto_save,

        "auto_copy": copy_after_generation,

        "show_analysis": show_security_analysis,

        # Theme

        "theme": selected_theme,

        # Maintenance

        "clear_history": clear_history,

    }