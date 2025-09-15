import requests
import streamlit as st
from models import NoteReadSchema

API_BASE = "http://api:8000"


@st.cache_data(ttl=120)
def fetch_notes() -> list[NoteReadSchema]:
    r = requests.get(f"{API_BASE}/notes/")
    r.raise_for_status()
    return [n for n in r.json()]


@st.cache_data(ttl=120)
def fetch_note_by_id(i: str) -> NoteReadSchema:
    r = requests.get(f"{API_BASE}/notes/{i}")
    r.raise_for_status()
    return r.json()


def create_note(title: str, content: str | None = None) -> NoteReadSchema:
    payload = {"title": title}
    if content:
        payload["content"] = content
    r = requests.post(f"{API_BASE}/notes/", json=payload)
    r.raise_for_status()
    return r.json()


def update_note(
    note_id: str, title: str | None = None, content: str | None = None
) -> NoteReadSchema:
    payload: NoteReadSchema = {}
    if title:
        payload["title"] = title
    if content:
        payload["content"] = content
    r = requests.patch(f"{API_BASE}/notes/{note_id}", json=payload)
    r.raise_for_status()
    return r.json()


def delete_note(note_id: str) -> bool:
    r = requests.delete(f"{API_BASE}/notes/{note_id}")
    if r.status_code not in (200, 204):
        r.raise_for_status()
    return True


def render_note(note: NoteReadSchema) -> None:
    st.subheader(f"{note.title} (id={note.id})")
    st.write(note.content or "—")
    st.write(f"Created: {note.created_at}, Updated: {note.updated_at}")
    st.write("Tags:")
    if note.tags:
        for tag in note.tags:
            st.markdown(f"- **{tag.name}** (id={tag.id})")
    else:
        st.write("—")
    st.divider()
