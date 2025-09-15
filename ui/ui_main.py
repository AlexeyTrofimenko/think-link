import requests
import streamlit as st
from models import NoteReadSchema, TagReadSchema
from notes import (
    create_note,
    delete_note,
    fetch_note_by_id,
    fetch_notes,
    render_note,
    update_note,
)
from tags import (
    create_tag,
    fetch_tag_by_id,
    fetch_tags,
    render_tag,
)
from tags import (
    delete_tag as delete_tag_api,
)

st.title("Notes")

st.header("Search")
with st.form("search"):
    c1, c2 = st.columns([1, 2])
    with c1:
        search_type = st.radio("Type", ["notes", "tags"], horizontal=True)
    with c2:
        search_id = st.text_input("ID", value="")
    do_search = st.form_submit_button("Search")

if do_search:
    if search_id.strip():
        try:
            if search_type == "notes":
                data = fetch_note_by_id(search_id.strip())
                render_note(NoteReadSchema(**data))
            else:
                data = fetch_tag_by_id(search_id.strip())
                render_tag(TagReadSchema(**data))
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
        except Exception as e:
            st.error(f"Parsing error: {e}")
    else:
        st.warning("Enter an ID.")

st.header("Manage tags")
with st.form("create_tag"):
    name = st.text_input("Name")
    submit = st.form_submit_button("Create tag")
if submit:
    if name.strip():
        try:
            created = create_tag(name.strip())
            st.success(f"Tag created: {created.get('name')} (id={created.get('id')})")
            st.cache_data.clear()
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
    else:
        st.warning("Enter a name.")

with st.form("delete_tag"):
    tag_id_del = st.text_input("Tag ID")
    submit_del = st.form_submit_button("Delete tag")
if submit_del:
    if tag_id_del.strip():
        try:
            delete_tag_api(tag_id_del.strip())
            st.success("Tag deleted")
            st.cache_data.clear()
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
    else:
        st.warning("Enter a tag ID.")

st.header("Manage notes")
with st.form("create_note"):
    title = st.text_input("Title")
    content = st.text_area("Content", value="", height=120)
    submit_note = st.form_submit_button("Create note")
if submit_note:
    if title.strip():
        try:
            created = create_note(title.strip(), content.strip())
            st.success(f"Note created: {created.get('title')} (id={created.get('id')})")
            st.cache_data.clear()
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
    else:
        st.warning("Enter a title.")

with st.form("update_note"):
    note_id_upd = st.text_input("Note ID")
    new_title = st.text_input("New title (optional)")
    new_content = st.text_area("New content (optional)", value="", height=120)
    submit_upd = st.form_submit_button("Update note")
if submit_upd:
    if note_id_upd.strip():
        payload_title = new_title.strip() if new_title.strip() else None
        payload_content = new_content.strip() if new_content.strip() else None
        if payload_title or payload_content:
            try:
                updated = update_note(note_id_upd.strip(), payload_title, payload_content)
                st.success(f"Note updated: {updated.get('title')} (id={updated.get('id')})")
                st.cache_data.clear()
            except requests.exceptions.RequestException as e:
                st.error(f"Request error: {e}")
        else:
            st.warning("Provide at least one field to update.")
    else:
        st.warning("Enter a note ID.")

with st.form("delete_note"):
    note_id_del = st.text_input("Note ID to delete")
    submit_note_del = st.form_submit_button("Delete note")
if submit_note_del:
    if note_id_del.strip():
        try:
            delete_note(note_id_del.strip())
            st.success("Note deleted")
            st.cache_data.clear()
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
    else:
        st.warning("Enter a note ID.")

st.header("All notes")
show_notes = st.toggle("Show all notes", value=False)
if show_notes:
    try:
        notes = [NoteReadSchema(**n) for n in fetch_notes()]
        for note in notes:
            render_note(note)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching notes: {e}")
    except Exception as e:
        st.error(f"Parsing error: {e}")

st.header("All tags")
show_tags = st.toggle("Show all tags", value=False)
if show_tags:
    try:
        tags = [TagReadSchema(**t) for t in fetch_tags()]
        for tag in tags:
            render_tag(tag)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tags: {e}")
    except Exception as e:
        st.error(f"Parsing error: {e}")
