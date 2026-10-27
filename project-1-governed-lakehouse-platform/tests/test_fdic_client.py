from __future__ import annotations

import json
from typing import Any

import requests

from src.fdic_client import FdicClient
from src.synthetic_pii import generate_complaints


class _FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self._payload


class _FakeSession:
    def __init__(self, pages: list[dict[str, Any]]) -> None:
        self._pages = pages
        self.calls: list[dict[str, Any]] = []

    def get(self, url: str, params: dict[str, Any], timeout: int) -> _FakeResponse:
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        return _FakeResponse(self._pages.pop(0))


def test_iter_records_unwraps_bankfind_envelope() -> None:
    session = _FakeSession(
        [
            {
                "meta": {"total": 2},
                "data": [
                    {"data": {"CERT": 1, "NAME": "A"}},
                    {"data": {"CERT": 2, "NAME": "B"}},
                ],
            }
        ]
    )
    client = FdicClient(session=session)  # type: ignore[arg-type]
    rows = client.iter_records("failures", ["CERT", "NAME"], page_size=10)
    assert rows == [{"CERT": 1, "NAME": "A"}, {"CERT": 2, "NAME": "B"}]
    assert session.calls[0]["url"].endswith("/failures")


def test_iter_records_respects_max_records() -> None:
    session = _FakeSession(
        [
            {
                "meta": {"total": 3},
                "data": [{"data": {"CERT": i}} for i in range(3)],
            }
        ]
    )
    client = FdicClient(session=session)  # type: ignore[arg-type]
    rows = client.iter_records("institutions", ["CERT"], max_records=2)
    assert [r["CERT"] for r in rows] == [0, 1]


def test_synthetic_complaints_are_labeled_and_seeded() -> None:
    first = generate_complaints(5, seed=7)
    second = generate_complaints(5, seed=7)
    assert first == second
    assert all(row["data_origin"] == "synthetic-faker" for row in first)
    assert first[0]["complaint_id"].startswith("SYN-7-")
    json.dumps(first)


def test_client_rejects_http_error(monkeypatch: Any) -> None:
    class Boom(requests.Session):
        def get(self, *args: Any, **kwargs: Any) -> Any:
            raise requests.HTTPError("nope")

    client = FdicClient(session=Boom())
    try:
        client.get_page("failures", ["CERT"])
    except requests.HTTPError:
        return
    raise AssertionError("expected HTTPError")
