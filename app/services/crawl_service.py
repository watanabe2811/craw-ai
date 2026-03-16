from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from app.clients.cloudflare_client import CloudflareClient
from app.exporters.json_exporter import JsonExporter
from app.models.response_models import CrawlResult, LinkItem
from app.parsers.html_parser import HtmlParser
from app.utils.logger import get_logger


logger = get_logger(__name__)


class CrawlService:
    def __init__(
        self,
        client: CloudflareClient,
        parser: HtmlParser,
        exporter: JsonExporter,
    ) -> None:
        self.client = client
        self.parser = parser
        self.exporter = exporter

    def crawl(self, url: str, save_raw: bool = False) -> tuple[CrawlResult, Path]:
        html = self.client.render_page(url)
        parsed = self.parser.parse(html, url)
        normalized = self.normalize(url, parsed)

        timestamp = normalized.collected_at.strftime("%Y%m%dT%H%M%SZ")
        slug = self._build_filename_slug(url)
        output_file = self.exporter.export(normalized, f"{slug}_{timestamp}.json")

        if save_raw:
            self.exporter.export_raw_html(html, f"{slug}_{timestamp}.html")

        return normalized, output_file

    def extract_text_from_html(self, html: str, base_url: str = "https://example.com") -> str:
        parsed = self.parser.parse(html, base_url)
        main_text = parsed.get("main_text")
        return main_text if isinstance(main_text, str) else ""

    def extract_text_from_html_file(
        self,
        html_file: str,
        base_url: str = "https://example.com",
    ) -> str:
        html = Path(html_file).read_text(encoding="utf-8")
        return self.extract_text_from_html(html, base_url=base_url)

    def normalize(self, url: str, parsed_html: dict[str, object]) -> CrawlResult:
        links = [
            LinkItem(**link)
            for link in parsed_html.get("links", [])
            if isinstance(link, dict) and link.get("url")
        ]

        return CrawlResult(
            url=url,
            collected_at=datetime.now(timezone.utc),
            title=parsed_html.get("title") if isinstance(parsed_html.get("title"), str) else None,
            main_text=(
                parsed_html.get("main_text")
                if isinstance(parsed_html.get("main_text"), str)
                else ""
            ),
            links=links,
        )

    @staticmethod
    def _build_filename_slug(url: str) -> str:
        parsed = urlparse(url)
        slug = f"{parsed.netloc}{parsed.path}".strip("/").replace("/", "_")
        return slug or "rendered_page"
