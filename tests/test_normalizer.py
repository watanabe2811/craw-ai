from pathlib import Path

from app.exporters.json_exporter import JsonExporter
from app.parsers.html_parser import HtmlParser
from app.services.crawl_service import CrawlService


class DummyClient:
    def render_page(self, url: str) -> str:
        return "<html></html>"


def test_normalize_creates_expected_schema(tmp_path: Path) -> None:
    service = CrawlService(
        client=DummyClient(),
        parser=HtmlParser(),
        exporter=JsonExporter(str(tmp_path)),
    )

    parsed = {
        "title": "Sample Title",
        "main_text": "Sample body text",
        "links": [
            {"title": "Home", "url": "https://example.com"},
            {"title": None, "url": "https://example.com/about"},
        ],
    }

    result = service.normalize("https://example.com/article", parsed)
    payload = result.model_dump(mode="json")

    assert payload["source"] == "cloudflare_render"
    assert payload["url"] == "https://example.com/article"
    assert payload["title"] == "Sample Title"
    assert payload["main_text"] == "Sample body text"
    assert payload["links"] == [
        {"title": "Home", "url": "https://example.com"},
        {"title": None, "url": "https://example.com/about"},
    ]
    assert payload["collected_at"].endswith("Z")


def test_extract_text_from_html_file(tmp_path: Path) -> None:
    html_file = tmp_path / "sample.html"
    html_file.write_text(
        """
        <html>
          <body>
            <main>
              <h1>Demo</h1>
              <p>Hello world from html file.</p>
            </main>
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    service = CrawlService(
        client=DummyClient(),
        parser=HtmlParser(),
        exporter=JsonExporter(str(tmp_path)),
    )

    text = service.extract_text_from_html_file(str(html_file), "https://example.com")

    assert text == "Demo Hello world from html file."


def test_extract_full_text_from_html_file(tmp_path: Path) -> None:
    html_file = tmp_path / "sample_full.html"
    html_file.write_text(
        """
        <html>
          <body>
            <div class="header-banner">Banner</div>
            <main>
              <h1>Demo</h1>
              <p>Hello world from html file.</p>
            </main>
            <div>Footer note</div>
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    service = CrawlService(
        client=DummyClient(),
        parser=HtmlParser(),
        exporter=JsonExporter(str(tmp_path)),
    )

    text = service.extract_text_from_html_file(
        str(html_file),
        "https://example.com",
        mode="full",
    )

    assert text == "Demo Hello world from html file. Footer note"
