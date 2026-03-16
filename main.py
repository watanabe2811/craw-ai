from __future__ import annotations

import json
import logging
from pathlib import Path

import typer

from app.clients.cloudflare_client import CloudflareClient
from app.exporters.json_exporter import JsonExporter
from app.exporters.report_renderer import render_cafef_report
from app.parsers.cafef_sections_parser import CafeFSectionsParser
from app.parsers.html_parser import HtmlParser
from app.services.crawl_service import CrawlService
from app.utils.config_loader import load_cloudflare_credentials, load_config
from app.utils.logger import setup_logging


cli = typer.Typer(help="Single-page crawler using Cloudflare Browser Rendering API.")
logger = logging.getLogger(__name__)


def _prepare_stdout_text(text: str, max_chars: int | None = None) -> str:
    cleaned_text = text.strip()
    if max_chars is None or max_chars <= 0 or len(cleaned_text) <= max_chars:
        return cleaned_text

    suffix = "\n\n[truncated]"
    if max_chars <= len(suffix):
        return suffix[:max_chars]

    truncated = cleaned_text[: max_chars - len(suffix)].rstrip()
    return f"{truncated}{suffix}"


@cli.callback()
def app_callback() -> None:
    """CLI entrypoint."""


@cli.command()
def crawl(
    url: str | None = typer.Option(None, "--url", help="Target URL to crawl."),
    output_format: str = typer.Option(
        "report",
        "--output-format",
        help="Output format: 'report' for human-readable report or 'json' for normalized JSON.",
    ),
    save_raw: bool = typer.Option(
        False,
        "--save-raw",
        help="Save raw rendered HTML into the output directory.",
    ),
    stdout_only: bool = typer.Option(
        False,
        "--stdout-only",
        help="Print only the main output content to stdout for bots/webhooks.",
    ),
    max_chars: int | None = typer.Option(
        None,
        "--max-chars",
        help="Optionally truncate stdout content to a maximum number of characters.",
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging."),
) -> None:
    setup_logging(debug=debug, enable_console=not stdout_only)
    try:
        config = load_config()
        credentials = load_cloudflare_credentials()
        target_url = url or config.default_target_url

        client = CloudflareClient(
            account_id=credentials.account_id,
            api_token=credentials.api_token,
            base_url=config.base_url,
            timeout=config.timeout,
            retry=config.retry,
        )
        parser = HtmlParser()
        exporter = JsonExporter(config.output_dir)
        service = CrawlService(client=client, parser=parser, exporter=exporter)

        crawl_data = service.crawl_and_collect(target_url, save_raw=save_raw)
        result = crawl_data["result"]
        output_file = crawl_data["json_file"]
        html = crawl_data["html"]
        slug = crawl_data["slug"]
        timestamp = crawl_data["timestamp"]

        if output_format == "json":
            json_text = _prepare_stdout_text(
                json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False),
                max_chars=max_chars,
            )
            typer.echo(json_text)
            if not stdout_only:
                typer.echo(f"\nSaved JSON to: {output_file}")
            return

        report_parser = CafeFSectionsParser()
        report_data = report_parser.parse(html, target_url)
        report_text = render_cafef_report(report_data)
        report_file = Path(config.output_dir) / f"{slug}_{timestamp}.report.txt"
        report_file.write_text(report_text, encoding="utf-8")

        typer.echo(_prepare_stdout_text(report_text, max_chars=max_chars))
        if not stdout_only:
            typer.echo(f"Saved report to: {report_file}")
            typer.echo(f"Saved JSON to: {output_file}")
    except Exception as exc:
        logger.error("Crawl command failed: %s", exc)
        error_text = f"Crawl failed: {exc}"
        if stdout_only:
            typer.echo(_prepare_stdout_text(error_text, max_chars=max_chars))
        else:
            typer.echo(error_text, err=True)
        raise typer.Exit(code=1)


@cli.command("extract-text")
def extract_text(
    html_file: str = typer.Option(..., "--html-file", help="Path to a local HTML file."),
    base_url: str = typer.Option(
        "https://example.com",
        "--base-url",
        help="Base URL used to resolve relative links during parsing.",
    ),
    mode: str = typer.Option(
        "main",
        "--mode",
        help="Extraction mode: 'main' for main content or 'full' for nearly all visible body text.",
    ),
    output_file: str | None = typer.Option(
        None,
        "--output-file",
        help="Optional path to save extracted text as UTF-8 plain text.",
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging."),
) -> None:
    setup_logging(debug=debug)

    parser = HtmlParser()
    exporter = JsonExporter("output")
    service = CrawlService(client=None, parser=parser, exporter=exporter)

    text = service.extract_text_from_html_file(html_file, base_url=base_url, mode=mode)

    if output_file:
        Path(output_file).write_text(text, encoding="utf-8")
        typer.echo(f"Saved text to: {output_file}")

    typer.echo(text)


if __name__ == "__main__":
    cli()
