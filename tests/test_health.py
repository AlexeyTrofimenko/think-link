from fastapi.testclient import TestClient


def test_health_ok(client: TestClient) -> None:
    resp = client.get("/health/")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_health_db_ok(client: TestClient) -> None:
    resp = client.get("/health/db")
    assert resp.status_code == 200
    assert resp.json() == {"db": "ok"}
