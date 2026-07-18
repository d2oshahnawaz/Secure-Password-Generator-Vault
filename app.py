# =====================================================
# APP
# Version 5.0 Professional
# Part 1A
# =====================================================

# =====================================================
# IMPORTS
# =====================================================

from pathlib import Path
import secrets

import streamlit as st

# =====================================================
# PAGE CONFIG
# (Must be first Streamlit command)
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

def load_css():

    css_path = Path("style.css")

    if css_path.exists():

        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


load_css()

# =====================================================
# LOAD BOOTSTRAP ICONS
# =====================================================

st.markdown(
    """
<link
rel="stylesheet"
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

# Browser Clipboard API
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
# SIDEBAR
# Version 5.0 Professional
# Part 1B
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

st.session_state.setdefault("generated", False)

st.session_state.setdefault("passwords", [])

st.session_state.setdefault("page", "generator")

st.session_state.setdefault("show_favorites", False)

st.session_state.setdefault("show_expired", False)

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

page = st.session_state.get("page", "generator")

# -----------------------------------------------------
# DASHBOARD
# -----------------------------------------------------

if page == "dashboard":

    show_dashboard()

    st.stop()

# -----------------------------------------------------
# PASSWORD VAULT
# -----------------------------------------------------

elif page == "vault":

    st.session_state.show_favorites = False
    st.session_state.show_expired = False

    show_vault()

    st.stop()

# -----------------------------------------------------
# FAVORITES
# -----------------------------------------------------

elif page == "favorites":

    st.session_state.show_favorites = True
    
    st.session_state.show_expired = False

    show_vault()

    st.stop()

# -----------------------------------------------------
# EXPIRED PASSWORDS
# -----------------------------------------------------

elif page == "expired":

    st.session_state.show_expired = True
    
    st.session_state.show_favorites = False

    show_vault()

    st.stop()

# -----------------------------------------------------
# PASSWORD HISTORY
# -----------------------------------------------------

elif page == "history":

    show_history()

    st.divider()

    show_export()

    st.stop()

# =====================================================
# GENERATOR PAGE STARTS HERE
# =====================================================

left, right = st.columns(
    [2, 1],
    gap="large",
)

# =====================================================
# GENERATOR PAGE
# Version 5.0 Professional
# Part 2A-1
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
        help="Enter any word, phrase or combination that you want to use as the base.",
    )

    extra_letters = ""
    
    extra_numbers = ""

    # -------------------------------------------------
    # LETTER VALIDATION
    # -------------------------------------------------

    if user_input and not any(ch.isalpha() for ch in user_input):

        st.warning("No alphabetic characters detected.")

        extra_letters = st.text_input(
            "Additional Letters",
            placeholder="Example: ABC, Tech, Secure",
        )

    # -------------------------------------------------
    # NUMBER VALIDATION
    # -------------------------------------------------

    if user_input and not any(ch.isdigit() for ch in user_input):

        st.warning("No numeric characters detected.")

        extra_numbers = st.text_input(
            "Additional Numbers",
            placeholder="Example: 123, 2026, 786",
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
        # INPUT VALIDATION
        # ---------------------------------------------

        if user_input:

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

        with st.spinner("Generating passwords..."):

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
                template_type=template_type,
                memorable=memorable,
            )

        st.session_state.passwords = passwords
        st.session_state.generated = True
        
                # -------------------------------------------------
        # STORE GENERATED PASSWORDS
        # -------------------------------------------------

        st.session_state.passwords = passwords
        st.session_state.generated = True

        # -------------------------------------------------
        # SAVE PASSWORD HISTORY
        # -------------------------------------------------

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

        # -------------------------------------------------
        # GENERATION SUMMARY
        # -------------------------------------------------

        st.success(
            f"{len(passwords)} secure password(s) generated successfully."
        )

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:

            st.metric(
                label="Passwords",
                value=len(passwords),
            )

        with summary_col2:

            st.metric(
                label="Saved",
                value=saved_count,
            )

        with summary_col3:

            st.metric(
                label="Template",
                value=template_type,
            )

        st.divider()

        # -------------------------------------------------
        # SECURITY INFORMATION
        # -------------------------------------------------

        st.markdown(
            """
<div class="card">

<h4>
<i class="bi bi-shield-check"></i>
Generation Summary
</h4>

<ul>

<li>Passwords generated using the selected security settings.</li>

<li>Strength analysis will be displayed for every generated password.</li>

<li>Entropy and crack-time estimation are calculated automatically.</li>

<li>Generated passwords are available in Password History.</li>

<li>Passwords can also be stored inside Password Vault.</li>

</ul>

</div>
""",
            unsafe_allow_html=True,
        )

# =====================================================
# RIGHT PANEL
# Version 5.0 Professional
# Part 2B
# =====================================================

with right:

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
<td>{"Enabled" if use_upper else "Disabled"}</td>
</tr>

<tr>
<td><b>Lowercase Letters</b></td>
<td>{"Enabled" if use_lower else "Disabled"}</td>
</tr>

<tr>
<td><b>Numbers</b></td>
<td>{"Enabled" if use_numbers else "Disabled"}</td>
</tr>

<tr>
<td><b>Special Characters</b></td>
<td>{"Enabled" if use_symbols else "Disabled"}</td>
</tr>

<tr>
<td><b>Avoid Similar Characters</b></td>
<td>{"Yes" if avoid_similar else "No"}</td>
</tr>

<tr>
<td><b>Excluded Characters</b></td>
<td>{exclude_chars if exclude_chars else "None"}</td>
</tr>

<tr>
<td><b>Password Template</b></td>
<td>{template_type}</td>
</tr>

<tr>
<td><b>Memorable Password</b></td>
<td>{"Enabled" if memorable else "Disabled"}</td>
</tr>

</table>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("")

    st.markdown(
        """
<h3>
<i class="bi bi-bar-chart-line-fill"></i>
Quick Overview
</h3>
""",
        unsafe_allow_html=True,
    )

    overview1, overview2 = st.columns(2)

    with overview1:

        st.metric(
            label="Generated",
            value=len(st.session_state.get("passwords", [])),
        )

    with overview2:

        st.metric(
            label="Template",
            value=template_type,
        )

    st.divider()

    st.markdown(
        """
<h3>
<i class="bi bi-graph-up-arrow"></i>
Live Statistics
</h3>
""",
        unsafe_allow_html=True,
    )

    stat1, stat2 = st.columns(2)

    try:
        vault_total = vault_count()
    except Exception:
        vault_total = 0

    try:
        favorite_total = favorite_count()
    except Exception:
        favorite_total = 0

    with stat1:

        st.metric(
            label="Vault",
            value=vault_total,
        )

    with stat2:

        st.metric(
            label="Favorites",
            value=favorite_total,
        )

    st.divider()

    st.markdown(
        """
<div class="card">

<h3>
<i class="bi bi-lightbulb-fill"></i>
Password Guidelines
</h3>

<ul>

<li>Use at least 16 characters whenever possible.</li>

<li>Combine uppercase, lowercase, numbers and symbols.</li>

<li>Avoid names, birthdays and common words.</li>

<li>Use a different password for every account.</li>

<li>Store passwords securely in Password Vault.</li>

<li>Regularly update important account passwords.</li>

</ul>

</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================
# GENERATED PASSWORDS
# Version 5.0 Professional
# Part 3A-1
# =====================================================

if st.session_state.get("generated", False):

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

    passwords = st.session_state.get("passwords", [])

    if not passwords:

        st.info("No passwords available.")

    else:

        columns = st.columns(3)

        for index, password in enumerate(passwords):

            with columns[index % 3]:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
<h4>
<i class="bi bi-key-fill"></i>
Password {index + 1}
</h4>
""",
                    unsafe_allow_html=True,
                )

                st.code(
                    password,
                    language="text",
                )

                strength = check_strength(password)

                progress = (strength["score"] + 1) / 5

                st.progress(progress)

                if strength["score"] <= 1:

                    st.error(strength["label"])

                elif strength["score"] == 2:

                    st.warning(strength["label"])

                else:

                    st.success(strength["label"])

                entropy = calculate_entropy(password)

                metric_col1, metric_col2 = st.columns(2)

                with metric_col1:

                    st.metric(
                        "Entropy",
                        f"{entropy:.2f} bits",
                    )

                with metric_col2:

                    st.metric(
                        "Crack Time",
                        crack_time(entropy),
                    )

                st.divider()

                st.markdown(
                    """
<h4>
<i class="bi bi-shield-check"></i>
Security Analysis
</h4>
""",
                    unsafe_allow_html=True,
                )

                show_password_stats(password)

                show_health_report(password)

                show_score(
                    password,
                    entropy,
                )

                show_breach_check(password)

                show_recommendations(
                    password,
                    entropy,
                )

                st.divider()
                
                                # ==========================================
                # COPY PASSWORD
                # ==========================================

                st.markdown(
                    """
<h4>
<i class="bi bi-clipboard-check"></i>
Copy Password
</h4>
""",
                    unsafe_allow_html=True,
                )

                render_copy_button(
                    password=password,
                    key=f"generated_password_{index}",
                )

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )

    st.divider()

    total_passwords = len(passwords)

    strong_passwords = sum(
        1
        for password in passwords
        if check_strength(password)["score"] >= 3
    )

    avg_entropy = (
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

    summary1, summary2, summary3 = st.columns(3)

    with summary1:

        st.metric(
            label="Passwords",
            value=total_passwords,
        )

    with summary2:

        st.metric(
            label="Strong",
            value=strong_passwords,
        )

    with summary3:

        st.metric(
            label="Average Entropy",
            value=f"{avg_entropy:.1f}",
        )

    st.divider()

# =====================================================
# SMART PASSWORD SUGGESTIONS
# Version 5.0 Professional
# Part 3B-1
# =====================================================

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
    "Generate additional password ideas based on your current security configuration."
)

suggestion_col1, suggestion_col2 = st.columns(2)

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
            template_type=template_type,
            memorable=memorable,
        )[0]

        st.session_state.setdefault(
            "extra_passwords",
            []
        )

        st.session_state.extra_passwords.append(
            extra_password
        )

with suggestion_col2:

    if st.button(
        "Clear Suggestions",
        key="clear_extra",
        use_container_width=True,
    ):

        st.session_state.extra_passwords = []

st.session_state.setdefault(
    "extra_passwords",
    []
)

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

    for idx, password in enumerate(
        st.session_state.extra_passwords,
        start=1,
    ):

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<b>Suggestion {idx}</b>
""",
            unsafe_allow_html=True,
        )

        st.code(
            password,
            language="text",
        )

        strength = check_strength(password)

        entropy = calculate_entropy(password)

        stat1, stat2 = st.columns(2)

        with stat1:

            st.metric(
                "Strength",
                strength["label"],
            )

        with stat2:

            st.metric(
                "Entropy",
                f"{entropy:.2f}",
            )

        render_copy_button(
            password=password,
            key=f"suggestion_copy_{idx}",
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

st.divider()

# =====================================================
# ABOUT PROJECT
# Version 5.0 Professional
# Part 3B-2
# =====================================================

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

The <b>Smart Password Generator</b> is a professional password
management application built using Python and Streamlit.

It enables users to create strong passwords, analyze password
security, securely store credentials, monitor password health,
and visualize security insights.

</p>

<h4>Key Features</h4>

<ul>

<li>Secure Password Generation</li>

<li>Password Strength Analysis</li>

<li>Entropy Calculation</li>

<li>Estimated Crack Time</li>

<li>Password Vault</li>

<li>Password History</li>

<li>Security Dashboard</li>

<li>Password Health Report</li>

<li>Breach Detection</li>

<li>Export & Backup</li>

</ul>

</div>
""",
    unsafe_allow_html=True,
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

quick1, quick2, quick3 = st.columns(3)

with quick1:

    if st.button(
        "Open Dashboard",
        key="quick_dashboard",
        use_container_width=True,
    ):
        st.session_state.page = "dashboard"
        st.rerun()

with quick2:

    if st.button(
        "Open Vault",
        key="quick_vault",
        use_container_width=True,
    ):
        st.session_state.page = "vault"
        st.rerun()

with quick3:

    if st.button(
        "Open History",
        key="quick_history",
        use_container_width=True,
    ):
        st.session_state.page = "history"
        st.rerun()

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

generated_total = len(st.session_state.get("passwords", []))

summary1, summary2, summary3 = st.columns(3)

with summary1:
    st.metric(
        "Generated",
        generated_total,
    )

with summary2:
    st.metric(
        "Vault",
        vault_total,
    )

with summary3:
    st.metric(
        "Favorites",
        favorite_total,
    )

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.divider()

show_footer()

# =====================================================
# END OF FILE
# Smart Password Generator
# Version 5.0 Professional
# =====================================================