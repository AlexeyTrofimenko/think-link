from datetime import datetime
from itertools import islice
from pathlib import Path

import streamlit as st
from models import NoteReadSchema

_CSS = Path("ui/styles/glasswall.css")


def glasswall(
    notes: list[NoteReadSchema],
    rows: tuple[int, int, int] = (5, 3, 2),
    base_cols: int | None = None,
) -> None:
    css = Path(_CSS).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    notes_iter = iter(notes)
    max_cols = base_cols or max(rows)
    for r_idx, count in enumerate(rows):
        st.markdown('<div class="row-wrap">', unsafe_allow_html=True)
        cols = st.columns(max_cols, gap="medium")
        row_notes = list(islice(notes_iter, count))
        for i in range(max_cols):
            with cols[i]:
                st.markdown('<div class="cell-pad">', unsafe_allow_html=True)
                if i < len(row_notes):
                    nid = row_notes[i].get("id")
                    selected = st.session_state["selected_note_id"] == nid
                    css_cls = "note-card selected" if selected else "note-card"

                    iso_time = row_notes[i].get("updated_at") or row_notes[i].get("created_at")
                    date_time = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
                    date_str = date_time.strftime("%d %b %I:%M %p").lstrip("0")

                    tags = row_notes[i].get("tags") or []
                    tags_html = ""
                    if tags:
                        for t in tags:
                            tags_html += f"""<span class="tag">{t.get("name")}</span>"""

                    st.markdown(
                        f"""
                        <a class="note-link" href="?note={nid}">
                          <div class="{css_cls}">
                            <div class="note-header">
                              <div class="note-title">{row_notes[i].get("title", "Untitled")}</div>
                              <div class="note-date">{date_str}</div>
                            </div>
                            <div class="note-body">{row_notes[i].get("content", "")}</div>
                            <div class="note-tags">{tags_html}</div>
                          </div>
                        </a>
                        """,
                        unsafe_allow_html=True,
                    )
                elif i < count:
                    st.markdown(
                        f"""
                        <div class="note-slot"
                             role="button" tabindex="0"
                             data-row="{r_idx}" data-col="{i}">
                          <span class="slot-plus">+</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown('<div class="placeholder"></div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
