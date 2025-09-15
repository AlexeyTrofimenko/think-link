import requests
import streamlit as st
from models import TagReadSchema

API_BASE = "http://api:8000"


@st.cache_data(ttl=120)
def fetch_tags() -> list[TagReadSchema]:
    r = requests.get(f"{API_BASE}/tags/")
    r.raise_for_status()
    return [t for t in r.json()]


@st.cache_data(ttl=120)
def fetch_tag_by_id(i: str) -> TagReadSchema:
    r = requests.get(f"{API_BASE}/tags/{i}")
    r.raise_for_status()
    return r.json()


def create_tag(name: str) -> TagReadSchema:
    r = requests.post(f"{API_BASE}/tags/", json={"name": name})
    r.raise_for_status()
    return r.json()


def delete_tag(tag_id: str) -> bool:
    r = requests.delete(f"{API_BASE}/tags/{tag_id}")
    if r.status_code not in (200, 204):
        r.raise_for_status()
    return True


def render_tag(tag: TagReadSchema) -> None:
    st.subheader(f"{tag.name} (id={tag.id})")
    created = getattr(tag, "created_at", "—")
    updated = getattr(tag, "updated_at", "—")
    st.write(f"Created: {created}, Updated: {updated}")
    st.divider()
