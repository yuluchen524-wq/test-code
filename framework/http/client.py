from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass
class ApiResponse:
    status_code: int
    text: str

    def json(self) -> Any:
        return json.loads(self.text)


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout

    def request(self, method: str, path: str, **kwargs: Any) -> ApiResponse:
        url = urljoin(self.base_url, path.lstrip("/"))
        timeout = int(kwargs.pop("timeout", self.timeout))
        headers = kwargs.pop("headers", {})
        json_body = kwargs.pop("json", None)

        data: bytes | None = None
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers = {"Content-Type": "application/json", **headers}

        req = Request(url=url, method=method.upper(), data=data, headers=headers)
        with urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return ApiResponse(status_code=response.status, text=body)

    def get(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("POST", path, **kwargs)

    def close(self) -> None:
        return None
