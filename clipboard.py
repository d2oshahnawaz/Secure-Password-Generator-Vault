# =====================================================
# CLIPBOARD UTILITIES
# Version 4.0 Professional
# =====================================================

try:
    import pyperclip
except ImportError:
    pyperclip = None

import streamlit as st


# =====================================================
# COPY PASSWORD
# =====================================================

def copy_password(password):
    """
    Copy password to system clipboard.

    Returns
    -------
    bool
        True if copied successfully,
        otherwise False.
    """

    if pyperclip is None:
        return False

    try:

        pyperclip.copy(str(password))

        return True

    except Exception:

        return False


# =====================================================
# COPY BUTTON
# =====================================================

def render_copy_button(password, key):

    if st.button(
        "Copy Password",
        key=f"copy_{key}",
        use_container_width=True
    ):

        if copy_password(password):

            st.success(
                "Password copied successfully."
            )

        else:

            st.code(
                password,
                language="text"
            )

            st.info(
                "Clipboard is unavailable. Copy the password manually."
            )


# =====================================================
# COPY TEXT
# =====================================================

def render_copy_text(text, key):

    if st.button(
        "Copy",
        key=f"text_{key}",
        use_container_width=True
    ):

        if copy_password(text):

            st.success("Copied successfully.")

        else:

            st.code(text)

            st.info(
                "Clipboard unavailable."
            )