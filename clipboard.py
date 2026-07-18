# =====================================================
# CLIPBOARD UTILITIES
# Version 5.1 Professional
# Browser Clipboard (Streamlit Cloud Compatible)
# =====================================================

import html
import streamlit.components.v1 as components


# =====================================================
# COPY BUTTON
# =====================================================

def render_copy_button(password, key):
    """
    Render a browser-based Copy button.

    Works on:
    ✔ Streamlit Cloud
    ✔ Windows
    ✔ Linux
    ✔ macOS
    ✔ Chrome
    ✔ Edge
    ✔ Firefox
    """

    password = html.escape(str(password))

    components.html(
        f"""
<!DOCTYPE html>
<html>

<head>

<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<style>

*{{
box-sizing:border-box;
margin:0;
padding:0;
font-family:Arial,sans-serif;
}}

body{{
background:transparent;
}}

.container{{
display:flex;
align-items:center;
gap:12px;
padding:4px;
}}

input{{
flex:1;
height:42px;
padding:0 14px;
border-radius:8px;
border:1px solid #4b5563;
background:#1f2937;
color:#ffffff;
font-size:15px;
outline:none;
}}

input:focus{{
border-color:#00ACC1;
}}

button{{
height:42px;
padding:0 18px;
border:none;
border-radius:8px;
background:#00ACC1;
color:white;
font-size:14px;
font-weight:600;
cursor:pointer;
display:flex;
align-items:center;
gap:8px;
transition:all .2s ease;
}}

button:hover{{
background:#0097A7;
}}

button:active{{
transform:scale(.97);
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

<button
id="btn_{key}"
onclick="copyPassword()">

<i class="bi bi-copy"></i>

<span id="text_{key}">
Copy
</span>

</button>

</div>

<script>

async function copyPassword(){{

const input=document.getElementById("pwd_{key}");
const text=document.getElementById("text_{key}");
const icon=document.querySelector("#btn_{key} i");

try{{

await navigator.clipboard.writeText(input.value);

icon.className="bi bi-check2";

text.innerHTML="Copied";

setTimeout(()=>{{

icon.className="bi bi-copy";

text.innerHTML="Copy";

}},2000);

}}

catch(err){{

input.focus();
input.select();

try{{

document.execCommand("copy");

icon.className="bi bi-check2";

text.innerHTML="Copied";

setTimeout(()=>{{

icon.className="bi bi-copy";

text.innerHTML="Copy";

}},2000);

}}

catch(e){{

text.innerHTML="Failed";

setTimeout(()=>{{

text.innerHTML="Copy";

}},2000);

}}

}}

}}

</script>

</body>

</html>
""",
        height=58,
    )


# =====================================================
# COPY TEXT
# =====================================================

def render_copy_text(text, key):
    render_copy_button(text, key)