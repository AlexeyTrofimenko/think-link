from fastapi.testclient import TestClient

from app.schemas.tag import TagCreateSchema
from tests._types import TagOut
from tests._utils import unique


def _create_tag(client: TestClient, name: str | None = None) -> TagOut:
    name = name or unique("tag")
    payload = TagCreateSchema(name=name).model_dump(mode="json")
    resp = client.post("/tags/", json=payload)
    assert resp.status_code == 201, resp.text
    body: TagOut = resp.json()
    assert body["name"] == name
    assert "id" in body
    return body


def test_create_tag_ok(client: TestClient) -> None:
    tag = _create_tag(client)
    assert isinstance(tag["id"], int)


def test_create_tag_conflict(client: TestClient) -> None:
    name = unique("tag")
    tag = _create_tag(client, name)
    resp = client.post("/tags/", json=TagCreateSchema(name=name).model_dump(mode="json"))
    assert resp.status_code == 201
    assert resp.json()["id"] == tag["id"]


def test_list_tags_sorted_by_name(client: TestClient) -> None:
    names = [f"zzz-{unique()}", f"mmm-{unique()}", f"aaa-{unique()}"]
    for n in names:
        _create_tag(client, n)

    resp = client.get("/tags/")
    assert resp.status_code == 200
    tags = resp.json()

    ours = [t for t in tags if t["name"] in names]
    assert [t["name"] for t in ours] == sorted([t["name"] for t in ours])


def test_get_tag_ok_and_404(client: TestClient) -> None:
    tag = _create_tag(client)
    ok = client.get(f"/tags/{tag['id']}")
    assert ok.status_code == 200
    assert ok.json()["id"] == tag["id"]

    not_found = client.get("/tags/99999999")
    assert not_found.status_code == 404
    assert not_found.json()["detail"] == "Tag not found"


def test_delete_tag_ok_and_404(client: TestClient) -> None:
    tag = _create_tag(client)
    resp_del = client.delete(f"/tags/{tag['id']}")
    assert resp_del.status_code == 204

    assert client.get(f"/tags/{tag['id']}").status_code == 404
    again = client.delete(f"/tags/{tag['id']}")
    assert again.status_code == 404
    assert again.json()["detail"] == "Tag not found"
