import base64
from pathlib import Path

import streamlit as st
from components.chat import note_panel
from components.glasswall import glasswall
from components.zenbar import zenbar
from notes import fetch_notes


def set_page_background(img_path: str) -> None:
    b64 = base64.b64encode(Path(img_path).read_bytes()).decode()
    st.markdown(
        f"""
    <style>
      html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], footer {{ background: transparent !important; }}
      body::before {{
        content:"";
        position: fixed; inset: 0;
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover; background-position: center; background-repeat: no-repeat;
        z-index: -1; pointer-events: none;
      }}
    </style>
    """,  # noqa: E501
        unsafe_allow_html=True,
    )


set_page_background("ui/static/bg.jpg")


st.set_page_config(page_title="Think-Link • Zen", layout="wide")


if "selected_note_id" not in st.session_state:
    st.session_state["selected_note_id"] = None
if "note_answers" not in st.session_state:
    st.session_state["note_answers"] = {}


@st.dialog("Answer")
def show_answer_dialog(text: str) -> None:
    st.markdown(text)


if "open_dialog" not in st.session_state:
    st.session_state["open_dialog"] = False
if "pending_answer" not in st.session_state:
    st.session_state["pending_answer"] = ""

if st.session_state.get("open_dialog"):
    show_answer_dialog(st.session_state.get("pending_answer", ""))


qid = st.query_params.get("note")
if qid is not None:
    try:
        st.session_state["selected_note_id"] = int(qid)
    except ValueError:
        pass

notes_items = fetch_notes()

glasswall(notes=notes_items)

note_panel()

st.markdown(
    """
    <style>
    div[data-testid="stChatInput"] {
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        width: min(60rem, 92vw);
        z-index: 10;
        background: rgba(32, 56, 88, 0.28) !important;
        backdrop-filter: blur(10px) saturate(130%) brightness(1.05);
        border-radius: 9999px !important;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.35), 0 10px 32px rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    div[data-testid="stChatInput"] input {
        background: transparent !important;
        color: #fff !important;
        font-size: clamp(0.95rem, 0.9rem + 0.25vw, 1.1rem) !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

zenbar("Ask or command")


st.markdown(
    """
    <style>
    .block-container {
        height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
