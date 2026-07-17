# =====================================================
# CLIPBOARD UTILITIES
# Version 5.0 Professional
# Browser Clipboard (Streamlit Cloud Compatible)
# =====================================================

import html
import streamlit.components.v1 as components


# =====================================================
# COPY BUTTON
# =====================================================

def render_copy_button(password, key):

    password = html.escape(str(password))

    components.html(
        f"""
        <!DOCTYPE html>
        <html>

        <head>

            <!-- Bootstrap Icons -->
            <link
                rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

            <style>

                body {{
                    margin:0;
                    padding:0;
                    background:transparent;
                    font-family:Arial, sans-serif;
                }}

                .container {{
                    display:flex;
                    gap:12px;
                    align-items:center;
                }}

                input {{
                    flex:1;
                    padding:12px;
                    border-radius:8px;
                    border:1px solid #444;
                    background:#1e1e1e;
                    color:white;
                    font-size:15px;
                    outline:none;
                }}

                button {{
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    gap:8px;
                    padding:12px 18px;
                    border:none;
                    border-radius:8px;
                    cursor:pointer;
                    background:#00ACC1;
                    color:white;
                    font-weight:600;
                    transition:.2s;
                }}

                button:hover {{
                    background:#0097A7;
                }}

                #msg {{
                    margin-left:10px;
                    color:#4CAF50;
                    font-size:14px;
                    display:none;
                    font-weight:600;
                }}

            </style>

        </head>

        <body>

            <div class="container">

                <input
                    id="pwd_{key}"
                    type="text"
                    value="{password}"
                    readonly>

                <button onclick="copyPassword()">

                    <i class="bi bi-copy"></i>

                    Copy

                </button>

                <span id="msg">

                    Copied

                </span>

            </div>

            <script>

                async function copyPassword() {{

                    const txt =
                        document.getElementById("pwd_{key}");

                    try {{

                        await navigator.clipboard.writeText(txt.value);

                        const msg =
                            document.getElementById("msg");

                        msg.style.display = "inline";

                        setTimeout(() => {{

                            msg.style.display = "none";

                        }},2000);

                    }}

                    catch(err) {{

                        txt.select();

                        document.execCommand("copy");

                    }}

                }}

            </script>

        </body>

        </html>
        """,
        height=70,
    )


# =====================================================
# COPY TEXT
# =====================================================

def render_copy_text(text, key):

    render_copy_button(text, key)