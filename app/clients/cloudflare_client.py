from __future__ import annotations

import time
from typing import Any

import httpx

from app.utils.logger import get_logger


logger = get_logger(__name__)


class CloudflareClient:
    def __init__(
        self,
        account_id: str,
        api_token: str,
        base_url: str,
        timeout: int,
        retry: int,
    ) -> None:
        self.account_id = account_id
        self.api_token = api_token
        self.timeout = timeout
        self.retry = retry
        self.endpoint = (
            f"{base_url.rstrip('/')}/accounts/{self.account_id}/browser-rendering/content"
        )

    def build_payload(self, url: str) -> dict[str, Any]:
        return {
            "url": url,
            "gotoOptions": {
                "waitUntil": "networkidle2",
                "timeout": self.timeout,
            },
            "rejectResourceTypes": ["image", "media", "font"],
        }

    def render_page(self, url: str) -> str:
        payload = self.build_payload(url)
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        last_error: Exception | None = None

        for attempt in range(1, self.retry + 1):
            try:
                logger.info("Calling Cloudflare Browser Rendering API for URL: %s", url)
                with httpx.Client(timeout=self.timeout / 1000) as client:
                    response = client.post(
                        self.endpoint,
                        headers=headers,
                        json=payload,
                    )

                logger.info("Cloudflare API response status: %s", response.status_code)
                response.raise_for_status()

                data = response.json()
                if data.get("success") is False:
                    raise ValueError(f"Cloudflare API error: {data.get('errors', [])}")

                result = data.get("result")
                if isinstance(result, dict):
                    content = result.get("content")
                elif isinstance(result, str):
                    content = result
                else:
                    content = None

                if not content:
                    raise ValueError("Cloudflare API returned an empty rendered content field.")

                return content
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                logger.error(
                    "Cloudflare render attempt %s/%s failed: %s",
                    attempt,
                    self.retry,
                    exc,
                )
                if attempt == self.retry:
                    break

                backoff_seconds = 2 ** (attempt - 1)
                logger.info("Retrying after %s second(s)...", backoff_seconds)
                time.sleep(backoff_seconds)

        raise RuntimeError("Failed to render page via Cloudflare API.") from last_error
