from pathlib import Path

import streamlit as st
from notes import delete_note, fetch_note_by_id, update_note

_CSS = Path("ui/styles/chat.css")


def _clear_caches() -> None:
    try:
        st.cache_data.clear()
    except Exception:
        pass
    try:
        st.cache_resource.clear()
    except Exception:
        pass


def _close_panel_and_rerun() -> None:
    st.session_state["selected_note_id"] = None
    for k in ["note", "act", "note_title", "content", "zen_msg"]:
        st.query_params.pop(k, None)
    _clear_caches()
    st.rerun()


def note_panel() -> None:
    note_id = st.session_state.get("selected_note_id")
    if note_id is None:
        return

    st.html(f"<style>{_CSS.read_text(encoding='utf-8')}</style>")

    qp = st.query_params
    act = qp.get("act")

    if act == "delete" and qp.get("note") == str(note_id):
        delete_note(str(note_id))
        _close_panel_and_rerun()

    if act == "update" and qp.get("note") == str(note_id):
        title_new = qp.get("note_title")
        content_new = qp.get("content")
        update_note(str(note_id), title=title_new or None, content=content_new or None)
        _close_panel_and_rerun()

    note = fetch_note_by_id(str(note_id))
    title_initial = note.get("title") or ""
    content_initial = note.get("content") or ""
    created_at = note.get("created_at") or ""
    updated_at = note.get("updated_at") or ""
    is_archived = bool(note.get("is_archived"))
    tags = [t.get("name") for t in (note.get("tags") or []) if isinstance(t, dict)]

    note_answers = st.session_state.get("note_answers", {})
    answer = note_answers.get(str(note_id))

    st.html(f"""
    <div class="chat-panel">
      <a class="chat-close" href="?" title="Close">✕</a>

      <div class="chat-title">Note #{note.get("id")}</div>
      <div class="chat-meta">
        <span class="chat-chip" title="Created">{created_at}</span>
        <span class="chat-chip" title="Updated">{updated_at}</span>
        {('<span class="chat-chip" title="Archived">ARCHIVED</span>' if is_archived else "")}
      </div>

      <div class="chat-tags">
        {
        "".join(f'<span class="chat-tag">{t}</span>' for t in tags)
        or '<span style="opacity:.6">(no tags)</span>'
    }
      </div>

      <form method="get">
        <input type="hidden" name="note" value="{note_id}">
        <textarea class="chat-input" name="note_title" placeholder="Title">{
        title_initial
    }</textarea>
        <hr class="chat-sep">
        <textarea class="chat-textarea" name="content" placeholder="Content">{
        content_initial
    }</textarea>
        <div class="chat-footer">
          <button class="chat-btn" type="submit" name="act" value="update" title="Update note">Update</button>
          <a class="chat-btn" href="?note={note_id}&act=delete" title="Delete note">Delete</a>
        </div>
      </form>
        <div class="chat-answers">
          <hr class="chat-sep">
          <div class="chat-answer-content">{answer or ""}</div>
        </div>
    </div>
    """)  # noqa: E501
