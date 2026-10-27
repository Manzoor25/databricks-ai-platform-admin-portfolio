"""Public FDIC BankFind Suite client.

Docs checked 2026-10-27: https://api.fdic.gov/banks/docs/
Verified live:
  GET /banks/failures
  GET /banks/institutions
No API key. Public data only. Do not point this at any non-public FDIC system.
"""

from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://api.fdic.gov/banks"
DEFAULT_TIMEOUT_SECONDS = 60


class FdicClient:
    def __init__(self, session: requests.Session | None = None, base_url: str = BASE_URL) -> None:
        self._session = session or requests.Session()
        self._base_url = base_url.rstrip("/")

    def get_page(
        self,
        dataset: str,
        fields: list[str],
        *,
        limit: int = 500,
        offset: int = 0,
        filters: str | None = None,
        sort_by: str | None = None,
        sort_order: str = "DESC",
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "fields": ",".join(fields),
            "limit": limit,
            "offset": offset,
        }
        if filters:
            params["filters"] = filters
        if sort_by:
            params["sort_by"] = sort_by
            params["sort_order"] = sort_order
        response = self._session.get(
            f"{self._base_url}/{dataset}",
            params=params,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

    def iter_records(
        self,
        dataset: str,
        fields: list[str],
        *,
        filters: str | None = None,
        sort_by: str | None = None,
        page_size: int = 500,
        max_records: int | None = None,
    ) -> list[dict[str, Any]]:
        """Pull pages until the API is exhausted or max_records is hit.

        The BankFind response shape is {"data": [{"data": {...}}], "meta": {"total": N}}.
        """
        records: list[dict[str, Any]] = []
        offset = 0
        total: int | None = None
        while True:
            page = self.get_page(
                dataset,
                fields,
                limit=page_size,
                offset=offset,
                filters=filters,
                sort_by=sort_by,
            )
            if total is None:
                total = int(page.get("meta", {}).get("total", 0))
            rows = page.get("data", [])
            if not rows:
                break
            for row in rows:
                payload = row.get("data", row)
                records.append(payload)
                if max_records is not None and len(records) >= max_records:
                    return records
            offset += len(rows)
            if offset >= total:
                break
        return records
