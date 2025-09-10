from fastapi.testclient import TestClient

from app.schemas.note import NoteCreateSchema, NoteUpdateSchema
from app.schemas.tag import TagCreateSchema
from tests._types import NoteOut, TagOut
from tests._utils import unique


def _create_tag(client: TestClient, name: str | None = None) -> TagOut:
    name = name or unique("tag")
    resp = client.post("/tags/", json=TagCreateSchema(name=name).model_dump(mode="json"))
    assert resp.status_code == 201, resp.text
    body: TagOut = resp.json()
    return body


def _create_note(
    client: TestClient,
    title: str | None = None,
    content: str | None = None,
    tags_ids: list[int] | None = None,
) -> NoteOut:
    model = NoteCreateSchema(
        title=title or unique("title"),
        content=content,
        tags_ids=tags_ids or [],
    )
    resp = client.post("/notes/", json=model.model_dump(mode="json"))
    assert resp.status_code == 201, resp.text
    body: NoteOut = resp.json()
    return body


def test_create_note_without_and_with_tags(client: TestClient) -> None:
    n1 = _create_note(client, content=unique("content"))
    assert n1["title"]
    assert "is_archived" in n1 and n1["is_archived"] in (False, True)
    assert n1["tags"] == []

    t1 = _create_tag(client)
    t2 = _create_tag(client)
    n2 = _create_note(client, tags_ids=[t1["id"], t2["id"]])
    tag_names = {t["name"] for t in n2["tags"]}
    assert tag_names == {t1["name"], t2["name"]}


def test_get_note_ok_and_404(client: TestClient) -> None:
    note = _create_note(client)
    ok = client.get(f"/notes/{note['id']}")
    assert ok.status_code == 200
    assert ok.json()["id"] == note["id"]

    not_found = client.get("/notes/99999999")
    assert not_found.status_code == 404
    assert not_found.json()["detail"] == "Note not found"


def test_list_notes_desc_order(client: TestClient) -> None:
    n1 = _create_note(client, title="first-" + unique(), content="c1")
    n2 = _create_note(client, title="second-" + unique(), content="c2")
    resp = client.get("/notes/")
    assert resp.status_code == 200
    rows = resp.json()
    ids = [r["id"] for r in rows]
    assert ids.index(n2["id"]) < ids.index(n1["id"])


def test_update_note_fields_and_tags(client: TestClient) -> None:
    t1 = _create_tag(client)
    t2 = _create_tag(client)
    note = _create_note(client, tags_ids=[t1["id"]])

    patch = NoteUpdateSchema(
        title="updated-" + unique(),
        content="updated-" + unique(),
        is_archived=True,
        tags_ids=[t2["id"]],
    )
    resp = client.patch(
        f"/notes/{note['id']}", json=patch.model_dump(mode="json", exclude_none=False)
    )
    assert resp.status_code == 200, resp.text
    updated = resp.json()

    assert updated["title"] == patch.title
    assert updated["content"] == patch.content
    assert updated["is_archived"] is True
    names = [t["name"] for t in updated["tags"]]
    assert names == [t2["name"]]


def test_delete_note_ok_and_404(client: TestClient) -> None:
    note = _create_note(client)
    assert client.delete(f"/notes/{note['id']}").status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404
    again = client.delete(f"/notes/{note['id']}")
    assert again.status_code == 404
    assert again.json()["detail"] == "Note not found"
