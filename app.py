# =====================================================
# APP
# Smart Password Generator
# Version 6.0 Professional
# Part 1
# =====================================================

# =====================================================
# IMPORTS
# =====================================================

from pathlib import Path
import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Password Generator",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# LOAD CUSTOM CSS
# =====================================================

def load_css() -> None:
    css_path = Path("style.css")

    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


load_css()

# =====================================================
# BOOTSTRAP ICONS
# =====================================================

st.markdown(
    """
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
""",
    unsafe_allow_html=True,
)

# =====================================================
# PROJECT MODULES
# =====================================================

from session import initialize_session
from sidebar import sidebar

from generator import generate_passwords

from strength import check_strength
from entropy import calculate_entropy
from cracktime import crack_time

from stats import show_password_stats
from health import show_health_report
from score import show_score
from recommend import show_recommendations
from breach import show_breach_check

from analytics import show_dashboard
from vault import show_vault

from clipboard import render_copy_button

from database import (
    save_password,
    clear_history,
    vault_count,
    favorite_count,
)

from ui import (
    show_history,
    show_export,
    show_footer,
)

# =====================================================
# INITIALIZE SESSION
# =====================================================

initialize_session()

# =====================================================
# SIDEBAR SETTINGS
# =====================================================

settings = sidebar()

# =====================================================
# USER SETTINGS
# =====================================================

password_length = settings.get("password_length", 16)
password_count = settings.get("password_count", 5)

use_upper = settings.get("use_upper", True)
use_lower = settings.get("use_lower", True)
use_numbers = settings.get("use_numbers", True)
use_symbols = settings.get("use_symbols", True)

avoid_similar = settings.get("avoid_similar", False)
exclude_chars = settings.get("exclude_chars", "")

template_type = settings.get("template_type", "Random")
memorable = settings.get("memorable", False)

# =====================================================
# SESSION DEFAULTS
# =====================================================

DEFAULT_SESSION = {
    "generated": False,
    "passwords": [],
    "page": "generator",
    "show_favorites": False,
    "show_expired": False,
    "search_keyword": "",
    "extra_passwords": [],
}

for key, value in DEFAULT_SESSION.items():
    st.session_state.setdefault(key, value)

# =====================================================
# MAINTENANCE
# =====================================================

if settings.get("clear_history", False):
    clear_history()
    st.success("Password history cleared successfully.")
    st.rerun()

# =====================================================
# PAGE ROUTING
# =====================================================

page = st.session_state.page

if page == "dashboard":
    show_dashboard()
    st.stop()

if page == "vault":
    st.session_state.show_favorites = False
    st.session_state.show_expired = False
    show_vault()
    st.stop()

if page == "favorites":
    st.session_state.show_favorites = True
    st.session_state.show_expired = False
    show_vault()
    st.stop()

if page == "expired":
    st.session_state.show_favorites = False
    st.session_state.show_expired = True
    show_vault()
    st.stop()

if page == "history":
    show_history()
    st.divider()
    show_export()
    st.stop()

# =====================================================
# GENERATOR LAYOUT
# =====================================================

left, right = st.columns(
    [2.2, 1],
    gap="large",
)

# =====================================================
# GENERATOR PAGE
# Version 6.0 Professional
# Part 2A-1a
# =====================================================

# =====================================================
# LEFT PANEL
# =====================================================

with left:

    st.markdown(
        """
<h2>
<i class="bi bi-shield-lock-fill"></i>
Generate Secure Password
</h2>
""",
        unsafe_allow_html=True,
    )

    st.write(
        "Create strong and secure passwords using your own keywords and custom settings."
    )

    st.divider()

    # -------------------------------------------------
    # USER INPUT
    # -------------------------------------------------

    user_input = st.text_input(
        label="Password Idea",
        placeholder="Example: Mohd123, BankPassword, OfficeLogin...",
        help=(
            "Enter a word, phrase or combination that "
            "will be used as the base for password generation."
        ),
    )

    extra_letters = ""
    extra_numbers = ""

    # -------------------------------------------------
    # LETTER VALIDATION
    # -------------------------------------------------

    if user_input and not any(ch.isalpha() for ch in user_input):

        st.warning(
            "⚠ No alphabetic characters detected."
        )

        extra_letters = st.text_input(
            "Additional Letters",
            placeholder="Example: ABC, Secure, Tech",
            help="Required because your input contains no letters.",
        )

    # -------------------------------------------------
    # NUMBER VALIDATION
    # -------------------------------------------------

    if user_input and not any(ch.isdigit() for ch in user_input):

        st.warning(
            "⚠ No numeric characters detected."
        )

        extra_numbers = st.text_input(
            "Additional Numbers",
            placeholder="Example: 123, 2026, 786",
            help="Required because your input contains no numbers.",
        )

    st.divider()

    # -------------------------------------------------
    # GENERATE BUTTON
    # -------------------------------------------------

    generate_clicked = st.button(
        "Generate Secure Password",
        key="generate_password",
        type="primary",
        use_container_width=True,
    )

    # -------------------------------------------------
    # PASSWORD GENERATION
    # -------------------------------------------------

    if generate_clicked:

        # ---------------------------------------------
        # COMPLETE INPUT VALIDATION
        # ---------------------------------------------

        if not user_input.strip():

            st.error(
                "⚠ Please enter a Password Idea."
            )

            st.stop()

        if (
            not any(ch.isalpha() for ch in user_input)
            and not extra_letters.strip()
        ):

            st.error(
                "Please enter at least one alphabetic character."
            )

            st.stop()

        if (
            not any(ch.isdigit() for ch in user_input)
            and not extra_numbers.strip()
        ):

            st.error(
                "Please enter at least one numeric character."
            )

            st.stop()

        # ---------------------------------------------
        # GENERATE PASSWORDS
        # ---------------------------------------------

        with st.spinner("Generating secure passwords..."):

            passwords = generate_passwords(
                user_input=user_input,
                extra_letters=extra_letters,
                extra_numbers=extra_numbers,
                length=password_length,
                count=password_count,
                use_upper=use_upper,
                use_lower=use_lower,
                use_numbers=use_numbers,
                use_symbols=use_symbols,
                avoid_similar=avoid_similar,
                exclude_chars=exclude_chars,
                template_name=template_type,
                memorable=memorable,
            )

        # ---------------------------------------------
        # STORE SESSION DATA
        # ---------------------------------------------

        st.session_state.passwords = passwords
        st.session_state.generated = True
        
        # =================================================
        # SAVE PASSWORD HISTORY
        # =================================================

        saved_count = 0

        for password in passwords:

            strength = check_strength(password)
            entropy = calculate_entropy(password)

            try:

                save_password(
                    password=password,
                    strength=strength["label"],
                    entropy=entropy,
                    crack_time=crack_time(entropy),
                )

                saved_count += 1

            except Exception as error:

                st.warning(
                    f"Unable to save password history: {error}"
                )

        # =================================================
        # GENERATION SUCCESS
        # =================================================

        st.success(
            f"Successfully generated "
            f"{len(passwords)} secure password(s)."
        )

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:

            st.metric(
                label="Passwords Generated",
                value=len(passwords),
            )

        with summary_col2:

            st.metric(
                label="Saved to History",
                value=saved_count,
            )

        with summary_col3:

            st.metric(
                label="Template",
                value=template_type,
            )

        st.divider()

        # =================================================
        # GENERATION INFORMATION
        # =================================================

        st.markdown(
            """
<div class="card">

<h4>
<i class="bi bi-shield-check"></i>
Generation Summary
</h4>

<p>
Your passwords were generated successfully using the
selected security settings.
</p>

<ul>

<li> Password strength will be analyzed automatically.</li>

<li> Entropy and estimated crack time are calculated.</li>

<li> Passwords are stored in Password History.</li>

<li> You can save important passwords into Password Vault.</li>

<li> Additional security recommendations are shown below.</li>

</ul>

</div>
""",
            unsafe_allow_html=True,
        )
        
    # -------------------------------------------------
    # PASSWORD TIPS
    # -------------------------------------------------

    st.markdown(
        """
<div class="card">

<h3>
<i class="bi bi-lightbulb-fill"></i>
Password Tips
</h3>

<ul>

<li>Use passwords with at least <b>16 characters</b>.</li>

<li>Include uppercase, lowercase, numbers and symbols.</li>

<li>Avoid names, birthdays and dictionary words.</li>

<li>Use a unique password for every account.</li>

<li>Save important passwords in the Password Vault.</li>

<li>Update passwords regularly for better security.</li>

</ul>

</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================
# RIGHT PANEL
# Version 6.0 Professional
# Part 2A-2
# =====================================================

with right:

    # -------------------------------------------------
    # CURRENT SETTINGS
    # -------------------------------------------------

    st.markdown(
        f"""
<div class="card">

<h3>
<i class="bi bi-sliders"></i>
Current Settings
</h3>

<table style="width:100%; line-height:2;">

<tr>
<td><b>Password Length</b></td>
<td>{password_length}</td>
</tr>

<tr>
<td><b>Password Count</b></td>
<td>{password_count}</td>
</tr>

<tr>
<td><b>Uppercase Letters</b></td>
<td>{"<i class='bi bi-check-circle-fill'></i> Enabled" if use_upper else "<i class='bi bi-x-circle-fill'></i> Disabled"}</td>
</tr>

<tr>
<td><b>Lowercase Letters</b></td>
<td>{"<i class='bi bi-check-circle-fill'></i> Enabled" if use_lower else "<i class='bi bi-x-circle-fill'></i> Disabled"}</td>
</tr>

<tr>
<td><b>Numbers</b></td>
<td>{"<i class='bi bi-check-circle-fill'></i> Enabled" if use_numbers else "<i class='bi bi-x-circle-fill'></i> Disabled"}</td>
</tr>

<tr>
<td><b>Symbols</b></td>
<td>{"<i class='bi bi-check-circle-fill'></i> Enabled" if use_symbols else "<i class='bi bi-x-circle-fill'></i> Disabled"}</td>
</tr>

<tr>
<td><b>Avoid Similar</b></td>
<td>{"<i class='bi bi-check-circle-fill'></i> Yes" if avoid_similar else "<i class='bi bi-x-circle-fill'></i> No"}</td>
</tr>

<tr>
<td><b>Excluded Characters</b></td>
<td>{exclude_chars if exclude_chars else "-"}</td>
</tr>

<tr>
<td><b>Template</b></td>
<td>{template_type}</td>
</tr>

<tr>
<td><b>Memorable Mode</b></td>
<td>{"Enabled" if memorable else "Disabled"}</td>
</tr>

</table>

</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    # -------------------------------------------------
    # QUICK OVERVIEW
    # -------------------------------------------------

    st.markdown(
        """
<h3>
<i class="bi bi-speedometer2"></i>
Quick Overview
</h3>
""",
        unsafe_allow_html=True,
    )

    overview1, overview2 = st.columns(2)

    with overview1:

        st.metric(
            "Generated",
            len(st.session_state.get("passwords", [])),
        )

    with overview2:

        st.metric(
            "Template",
            template_type,
        )

    st.divider()

    # -------------------------------------------------
    # LIVE DATABASE STATS
    # -------------------------------------------------

    st.markdown(
        """
<h3>
<i class="bi bi-database-fill"></i>
Database Statistics
</h3>
""",
        unsafe_allow_html=True,
    )

    try:
        vault_total = vault_count()
    except Exception:
        vault_total = 0

    try:
        favorite_total = favorite_count()
    except Exception:
        favorite_total = 0

    stats1, stats2 = st.columns(2)

    with stats1:

        st.metric(
            "Vault",
            vault_total,
        )

    with stats2:

        st.metric(
            "Favorites",
            favorite_total,
        )

    st.divider()
    
    # =====================================================
    # QUICK ACCESS
    # =====================================================

    st.markdown(
        """
        <h2>
        <i class="bi bi-grid-fill"></i>
        Quick Access
        </h2>
        """,
        unsafe_allow_html=True,
    )

    quick_col1, quick_col2, quick_col3 = st.columns(3)

    with quick_col1:
        if st.button(
            "Dashboard",
            key="quick_dashboard",
            use_container_width=True,
        ):
            st.session_state.page = "dashboard"
            st.rerun()

    with quick_col2:
        if st.button(
            "Password Vault",
            key="quick_vault",
            use_container_width=True,
        ):
            st.session_state.page = "vault"
            st.rerun()

    with quick_col3:
        if st.button(
            "Password History",
            key="quick_history",
            use_container_width=True,
        ):
            st.session_state.page = "history"
            st.rerun()

# =====================================================
# GENERATED PASSWORDS
# Version 6.0 Professional
# Part 3A-1
# =====================================================

passwords = st.session_state.get("passwords", [])

if (
    st.session_state.get("generated", False)
    and passwords
):

    st.divider()

    st.markdown(
        """
<h2>
<i class="bi bi-files"></i>
Generated Passwords
</h2>
""",
        unsafe_allow_html=True,
    )

    columns = st.columns(3)

    for index, password in enumerate(passwords):

        with columns[index % 3]:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True,
            )

            # -----------------------------------------
            # CARD TITLE
            # -----------------------------------------

            st.markdown(
                f"""
<h4>
<i class="bi bi-key-fill"></i>
Password {index + 1}
</h4>
""",
                unsafe_allow_html=True,
            )

            # -----------------------------------------
            # PASSWORD
            # -----------------------------------------

            st.code(
                password,
                language="text",
            )

            # -----------------------------------------
            # COPY PASSWORD
            # -----------------------------------------

            render_copy_button(
                password=password,
                key=f"generated_password_{index}",
            )

            st.divider()

            # -----------------------------------------
            # STRENGTH
            # -----------------------------------------

            strength = check_strength(password)

            progress = (strength["score"] + 1) / 5

            st.progress(progress)

            if strength["score"] <= 1:

                st.error(
                    strength["label"]
                )

            elif strength["score"] == 2:

                st.warning(
                    strength["label"]
                )

            else:

                st.success(
                    strength["label"]
                )

            # -----------------------------------------
            # ENTROPY
            # -----------------------------------------

            entropy = calculate_entropy(
                password
            )

            metric_col1, metric_col2 = st.columns(2)

            with metric_col1:

                st.metric(
                    label="Entropy",
                    value=f"{entropy:.2f} bits",
                )

            with metric_col2:

                st.metric(
                    label="Crack Time",
                    value=crack_time(entropy),
                )

            st.divider()

            # -----------------------------------------
            # SECURITY ANALYSIS
            # Version 6.0 Professional
            # Part 3A-2
            # -----------------------------------------

            st.markdown(
                """
<h4>
<i class="bi bi-shield-check"></i>
Security Analysis
</h4>
""",
                unsafe_allow_html=True,
            )

            # -----------------------------------------
            # PASSWORD STATISTICS
            # -----------------------------------------

            show_password_stats(
                password,
                key=f"stats_{index}"
            )

            st.divider()

            # -----------------------------------------
            # PASSWORD HEALTH
            # -----------------------------------------

            show_health_report(password)

            st.divider()

            # -----------------------------------------
            # SECURITY SCORE
            # -----------------------------------------

            show_score(
                password=password,
                entropy=entropy,
            )

            st.divider()

            # -----------------------------------------
            # BREACH CHECK
            # -----------------------------------------

            show_breach_check(password)

            st.divider()

            # -----------------------------------------
            # RECOMMENDATIONS
            # -----------------------------------------

            show_recommendations(
                password=password,
                entropy=entropy,
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

    st.divider()

# =====================================================
# GENERATION SUMMARY
# Version 6.0 Professional
# Part 3A-3
# =====================================================

total_passwords = len(passwords)

strong_passwords = sum(
    1
    for password in passwords
    if check_strength(password)["score"] >= 3
)

average_entropy = (
    sum(
        calculate_entropy(password)
        for password in passwords
    ) / total_passwords
    if total_passwords
    else 0
)

st.markdown(
    """
<h2>
<i class="bi bi-bar-chart"></i>
Generation Summary
</h2>
""",
    unsafe_allow_html=True,
)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:

    st.metric(
        label="Generated Passwords",
        value=total_passwords,
    )

with summary_col2:

    st.metric(
        label="Strong Passwords",
        value=strong_passwords,
    )

with summary_col3:

    st.metric(
        label="Average Entropy",
        value=f"{average_entropy:.2f} bits",
    )

# -------------------------------------------------
# SUMMARY INFORMATION
# -------------------------------------------------

st.markdown(
    """
<div class="card">

<h4>
<i class="bi bi-info-circle"></i>
Summary
</h4>

<p>

This summary provides an overview of the passwords generated
during the current session.

</p>

<ul>

<li>Total generated passwords are displayed above.</li>

<li>Strong passwords are those with a security score of 3 or higher.</li>

<li>Average entropy indicates the overall randomness of the generated passwords.</li>

<li>Use Password History or Password Vault to manage generated passwords securely.</li>

</ul>

</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# =====================================================
# SMART PASSWORD SUGGESTIONS
# Version 6.0 Professional
# Part 3B-1
# =====================================================

if st.session_state.get("generated", False):

    st.markdown(
        """
<h2>
<i class="bi bi-lightbulb"></i>
Smart Password Suggestions
</h2>
""",
        unsafe_allow_html=True,
    )

    st.write(
        "Generate additional password suggestions using your current settings."
    )

    suggestion_col1, suggestion_col2 = st.columns(2)

    # -------------------------------------------------
    # GENERATE ONE MORE
    # -------------------------------------------------

    with suggestion_col1:

        if st.button(
            "Generate One More",
            key="generate_extra",
            use_container_width=True,
        ):

            extra_password = generate_passwords(
                user_input=user_input,
                extra_letters=extra_letters,
                extra_numbers=extra_numbers,
                length=password_length,
                count=1,
                use_upper=use_upper,
                use_lower=use_lower,
                use_numbers=use_numbers,
                use_symbols=use_symbols,
                avoid_similar=avoid_similar,
                exclude_chars=exclude_chars,
                template_name=template_type,
                memorable=memorable,
            )[0]

            st.session_state.extra_passwords.append(
                extra_password
            )

    # -------------------------------------------------
    # CLEAR SUGGESTIONS
    # -------------------------------------------------

    with suggestion_col2:

        if st.button(
            "Clear Suggestions",
            key="clear_extra",
            use_container_width=True,
        ):

            st.session_state.extra_passwords.clear()

    # -------------------------------------------------
    # DISPLAY SUGGESTIONS
    # -------------------------------------------------

    if st.session_state.extra_passwords:

        st.divider()

        st.markdown(
            """
<h3>
<i class="bi bi-stars"></i>
Suggested Passwords
</h3>
""",
            unsafe_allow_html=True,
        )

        suggestion_columns = st.columns(2)

        for index, password in enumerate(
            st.session_state.extra_passwords
        ):

            with suggestion_columns[index % 2]:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
<h4>
<i class="bi bi-key-fill"></i>
Suggestion {index + 1}
</h4>
""",
                    unsafe_allow_html=True,
                )

                st.code(
                    password,
                    language="text",
                )

                render_copy_button(
                    password=password,
                    key=f"suggestion_copy_{index}",
                )

                st.divider()

                strength = check_strength(password)

                entropy = calculate_entropy(password)

                metric1, metric2 = st.columns(2)

                with metric1:

                    st.metric(
                        "Strength",
                        strength["label"],
                    )

                with metric2:

                    st.metric(
                        "Entropy",
                        f"{entropy:.2f} bits",
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )

# =====================================================
# ABOUT PROJECT
# Version 6.0 Professional
# Part 3B-2
# =====================================================

st.divider()

st.markdown(
    """
<h2>
<i class="bi bi-info-circle-fill"></i>
About Smart Password Generator
</h2>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="card">

<p>

<b>Smart Password Generator</b> is a professional password
generation and management application built with
Python, Streamlit and SQLite.

The application helps users generate secure passwords,
analyze password strength, estimate password entropy,
manage a secure password vault and maintain password history.

</p>

<h4>Core Features</h4>

<ul>

<li>Secure Password Generation</li>

<li>Password Strength Analysis</li>

<li>Entropy Calculation</li>

<li>Crack Time Estimation</li>

<li>Password History</li>

<li>Password Vault</li>

<li>Password Health Report</li>

<li>Password Breach Detection</li>

<li>Analytics Dashboard</li>

<li>Export & Backup Support</li>

</ul>

</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# =====================================================
# APPLICATION SUMMARY
# =====================================================

try:
    vault_total = vault_count()
except Exception:
    vault_total = 0

try:
    favorite_total = favorite_count()
except Exception:
    favorite_total = 0

generated_total = len(
    st.session_state.get("passwords", [])
)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:

    st.metric(
        label="Generated Passwords",
        value=generated_total,
    )

with summary_col2:

    st.metric(
        label="Passwords in Vault",
        value=vault_total,
    )

with summary_col3:

    st.metric(
        label="Favorite Passwords",
        value=favorite_total,
    )

# =====================================================
# FOOTER
# =====================================================

show_footer()

# =====================================================
# END OF FILE
# Smart Password Generator
# Version 6.0 Professional
# =====================================================