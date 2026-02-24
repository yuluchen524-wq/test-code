from __future__ import annotations

import json

from framework.http.client import ApiClient


class DummyHttpResponse:
    def __init__(self, status: int, payload: dict) -> None:
        self.status = status
        self._body = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_request_builds_url_and_uses_default_timeout(monkeypatch) -> None:
    captured: dict = {}

    def fake_urlopen(req, timeout):
        captured["url"] = req.full_url
        captured["method"] = req.method
        captured["timeout"] = timeout
        return DummyHttpResponse(200, {"ok": True})

    monkeypatch.setattr("framework.http.client.urlopen", fake_urlopen)

    client = ApiClient(base_url="https://example.com/api", timeout=15)
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert captured == {
        "url": "https://example.com/api/users",
        "method": "GET",
        "timeout": 15,
    }


def test_request_allows_overriding_timeout_and_json_body(monkeypatch) -> None:
    captured: dict = {}

    def fake_urlopen(req, timeout):
        captured["url"] = req.full_url
        captured["method"] = req.method
        captured["timeout"] = timeout
        captured["headers"] = dict(req.header_items())
        captured["data"] = req.data.decode("utf-8")
        return DummyHttpResponse(201, {"created": True})

    monkeypatch.setattr("framework.http.client.urlopen", fake_urlopen)

    client = ApiClient(base_url="https://example.com", timeout=15)
    response = client.post("orders", timeout=3, json={"id": 1})

    assert response.status_code == 201
    assert captured["url"] == "https://example.com/orders"
    assert captured["method"] == "POST"
    assert captured["timeout"] == 3
    assert captured["headers"]["Content-type"] == "application/json"
    assert captured["data"] == '{"id": 1}'
