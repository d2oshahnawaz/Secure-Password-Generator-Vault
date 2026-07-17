# =====================================================
# APP
# Version 4.2 Professional
# Part 1 / 4
# =====================================================

# =====================================================
# IMPORTS
# =====================================================

from pathlib import Path
import secrets

import streamlit as st

try:
    import pyperclip
except ImportError:
    pyperclip = None

# =====================================================
# PAGE CONFIG
# (Must be the first Streamlit command)
# =====================================================

st.set_page_config(

    page_title="Smart Password Generator",

    page_icon="assets/favicon.png",

    layout="wide",

    initial_sidebar_state="expanded"

)

# =====================================================
# LOAD CUSTOM CSS
# =====================================================

def load_css():

    css_file = Path("style.css")

    if css_file.exists():

        st.markdown(

            f"<style>{css_file.read_text(encoding='utf-8')}</style>",

            unsafe_allow_html=True

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
# =====================================================

settings = sidebar()

# =====================================================
# USER SETTINGS
# =====================================================

password_length = settings["password_length"]

password_count = settings["password_count"]

use_upper = settings["use_upper"]

use_lower = settings["use_lower"]

use_numbers = settings["use_numbers"]

use_symbols = settings["use_symbols"]

avoid_similar = settings["avoid_similar"]

exclude_chars = settings["exclude_chars"]

template_type = settings["template_type"]

memorable = settings["memorable"]

# =====================================================
# MAINTENANCE
# =====================================================

if settings["clear_history"]:

    clear_history()

    st.success("Password history cleared successfully.")

    st.rerun()

# =====================================================
# PAGE ROUTING
# =====================================================

page = st.session_state.get(

    "page",

    "generator"

)

# ---------------- Dashboard ----------------

if page == "dashboard":

    show_dashboard()

    st.stop()

# ---------------- Vault ----------------

elif page == "vault":

    show_vault()

    st.stop()

# ---------------- Favorites ----------------

elif page == "favorites":

    st.session_state.show_favorites = True

    st.session_state.show_expired = False

    show_vault()

    st.stop()

# ---------------- Expired ----------------

elif page == "expired":

    st.session_state.show_expired = True

    st.session_state.show_favorites = False

    show_vault()

    st.stop()

# ---------------- History ----------------

elif page == "history":

    show_history()

    st.divider()

    show_export()

    st.stop()

# =====================================================
# GENERATOR PAGE
# Version 4.2 Professional
# Part 2 / 4
# =====================================================

left, right = st.columns([2, 1], gap="large")

# =====================================================
# LEFT PANEL
# =====================================================

with left:

    st.header("Generate Secure Password")

    user_input = st.text_input(

        "Enter your password idea",

        placeholder="Example: Mohd123, BankPassword, OfficeLogin..."

    )

    extra_letters = ""

    extra_numbers = ""

    # -------------------------------------------------
    # Ask for missing letters
    # -------------------------------------------------

    if user_input:

        if not any(char.isalpha() for char in user_input):

            extra_letters = st.text_input(

                "No letters detected. Enter letters"

            )

        if not any(char.isdigit() for char in user_input):

            extra_numbers = st.text_input(

                "No numbers detected. Enter numbers"

            )

    # -------------------------------------------------
    # Generate Button
    # -------------------------------------------------

    generate_clicked = st.button(

        "Generate Secure Password",

        key="generate_password",

        type="primary",

        use_container_width=True

    )

    # -------------------------------------------------
    # Password Generation
    # -------------------------------------------------

    if generate_clicked:

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

        # ---------------------------------------------
        # Save Password History
        # ---------------------------------------------

        for password in passwords:

            strength = check_strength(password)

            entropy = calculate_entropy(password)

            save_password(

                password=password,

                strength=strength["label"],

                entropy=entropy,

                crack_time=crack_time(entropy)

            )

        st.success(

            f"{len(passwords)} password(s) generated successfully."

        )

# =====================================================
# RIGHT PANEL
# =====================================================

with right:

    st.markdown(
        f"""
<div class="card">

<h3>
<i class="bi bi-sliders"></i>
Current Settings
</h3>

<table style="width:100%;line-height:2;">

<tr>
<td><b>Password Length</b></td>
<td>{password_length}</td>
</tr>

<tr>
<td><b>Password Count</b></td>
<td>{password_count}</td>
</tr>

<tr>
<td><b>Uppercase</b></td>
<td>{"Enabled" if use_upper else "Disabled"}</td>
</tr>

<tr>
<td><b>Lowercase</b></td>
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
<td><b>Avoid Similar</b></td>
<td>{"Yes" if avoid_similar else "No"}</td>
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
<td><b>Memorable</b></td>
<td>{"Enabled" if memorable else "Disabled"}</td>
</tr>

</table>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("### Quick Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Generated",

            len(st.session_state.passwords)

            if st.session_state.generated

            else 0

        )

    with col2:

        st.metric(

            "Template",

            template_type

        )

# =====================================================
# GENERATED PASSWORDS
# Version 4.2 Professional
# Part 3 / 4
# =====================================================

if st.session_state.generated:

    st.divider()

    st.header("Generated Passwords")

    passwords = st.session_state.passwords

    columns = st.columns(3)

    for index, password in enumerate(passwords):

        with columns[index % 3]:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.subheader(f"Password {index + 1}")

            st.code(
                password,
                language="text"
            )

            # ==========================================
            # PASSWORD STRENGTH
            # ==========================================

            strength = check_strength(password)

            st.progress(
                (strength["score"] + 1) / 5
            )

            if strength["score"] <= 1:

                st.error(strength["label"])

            elif strength["score"] == 2:

                st.warning(strength["label"])

            else:

                st.success(strength["label"])

            # ==========================================
            # ENTROPY & CRACK TIME
            # ==========================================

            entropy = calculate_entropy(password)

            metric1, metric2 = st.columns(2)

            with metric1:

                st.metric(
                    "Entropy",
                    f"{entropy:.2f} bits"
                )

            with metric2:

                st.metric(
                    "Crack Time",
                    crack_time(entropy)
                )

            st.divider()

            # ==========================================
            # SECURITY ANALYSIS
            # ==========================================

            show_password_stats(password)

            show_health_report(password)

            show_score(
                password,
                entropy
            )

            show_breach_check(password)

            show_recommendations(
                password,
                entropy
            )

            st.divider()

            # ==========================================
            # COPY PASSWORD
            # ==========================================

            if st.button(

                "Copy Password",

                key=f"copy_password_{index}",

                type="primary",

                use_container_width=True

            ):

                try:

                    if pyperclip:

                        pyperclip.copy(password)

                        st.success(
                            "Password copied successfully."
                        )

                    else:

                        st.code(password)

                        st.info(
                            "Clipboard not available. Copy manually."
                        )

                except Exception:

                    st.code(password)

                    st.info(
                        "Clipboard not available. Copy manually."
                    )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    st.divider()

# =====================================================
# SMART PASSWORD SUGGESTIONS
# =====================================================

if user_input:

    st.header("Smart Password Suggestions")

    letters = "".join(

        ch for ch in user_input

        if ch.isalpha()

    )

    numbers = "".join(

        ch for ch in user_input

        if ch.isdigit()

    )

    if not letters:

        letters = "User"

    if not numbers:

        numbers = secrets.choice(

            [

                "123",

                "321",

                "786",

                "007",

                "2026",

                "2027"

            ]

        )

    suggestions = [

        f"{letters.capitalize()}@{numbers}",

        f"{letters.capitalize()}#{numbers}",

        f"{letters.capitalize()}_{numbers}",

        f"{letters.capitalize()}Secure{numbers}",

        f"{letters.capitalize()}@Tech{numbers}",

        f"{letters.capitalize()}@AI{numbers}",

        f"{letters.capitalize()}{numbers}!",

        f"{letters.capitalize()}_{numbers}_Pro",

    ]

    suggestion_cols = st.columns(2)

    for i, suggestion in enumerate(suggestions):

        with suggestion_cols[i % 2]:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.code(
                suggestion,
                language="text"
            )

            if st.button(

                "Copy Suggestion",

                key=f"suggestion_{i}",

                use_container_width=True

            ):

                try:

                    if pyperclip:

                        pyperclip.copy(suggestion)

                        st.success("Copied successfully.")

                    else:

                        st.code(suggestion)

                        st.info(
                            "Clipboard unavailable."
                        )

                except Exception:

                    st.code(suggestion)

                    st.info(
                        "Clipboard unavailable."
                    )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

# =====================================================
# ABOUT
# Version 5.1 Professional
# =====================================================

st.divider()

with st.expander("About Smart Password Generator", expanded=False):

    st.markdown(
        """
<h2>
<i class="bi bi-info-circle-fill"></i>
About Smart Password Generator
</h2>

A professional password generation and password management platform
built using **Python**, **Streamlit**, and **SQLite**.

---

### <i class="bi bi-person-badge-fill"></i> Developer

**Mohd Shahnawaz**

Founder & CEO — Tech Education World

Founding President — ENAC Cybersecurity Club

---

### <i class="bi bi-cpu-fill"></i> Technology Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- Cryptography
- zxcvbn

---

### <i class="bi bi-stars"></i> Features

- Secure Password Generator
- Multiple Password Templates
- Memorable Password Generator
- Password Strength Analysis
- Password Entropy Calculation
- Password Crack Time Estimation
- Password Health Report
- Password Security Score
- Offline Breach Detection
- Password Recommendations
- Password History
- Analytics Dashboard
- Password Vault
- CSV / TXT / JSON Export

---

### <i class="bi bi-lightbulb-fill"></i> Upcoming Features

- Password Expiry Alerts
- Vault Backup & Restore
- QR Code Export
- Password Audit Report
- Cloud Synchronization
- Multi-device Support
- Password Sharing
- Multi-Factor Authentication

""",
        unsafe_allow_html=True,
    )

# =====================================================
# PROJECT DASHBOARD
# =====================================================

st.divider()

st.markdown(
    """
<h2>
<i class="bi bi-speedometer2"></i>
Project Dashboard
</h2>
""",
    unsafe_allow_html=True,
)

page_names = {
    "generator": "Generator",
    "history": "History",
    "dashboard": "Dashboard",
    "vault": "Vault",
    "favorites": "Favorites",
    "expired": "Expired",
}

current_page = page_names.get(
    st.session_state.get("page", "generator"),
    "Generator",
)

generated_count = len(
    st.session_state.get("passwords", [])
)

try:
    vault_total = vault_count()
except Exception:
    vault_total = 0

try:
    favorite_total = favorite_count()
except Exception:
    favorite_total = 0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Generated",
        value=generated_count,
    )

with col2:
    st.metric(
        label="Templates",
        value="11",
    )

with col3:
    st.metric(
        label="Current Page",
        value=current_page,
    )

with col4:
    st.metric(
        label="Vault",
        value=vault_total,
    )

with col5:
    st.metric(
        label="Favorites",
        value=favorite_total,
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

show_footer()