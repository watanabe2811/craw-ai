from __future__ import annotations

import json
from pathlib import Path

import typer

from app.clients.cloudflare_client import CloudflareClient
from app.exporters.json_exporter import JsonExporter
from app.parsers.html_parser import HtmlParser
from app.services.crawl_service import CrawlService
from app.utils.config_loader import load_cloudflare_credentials, load_config
from app.utils.logger import setup_logging


cli = typer.Typer(help="Single-page crawler using Cloudflare Browser Rendering API.")


@cli.callback()
def app_callback() -> None:
    """CLI entrypoint."""


@cli.command()
def crawl(
    url: str | None = typer.Option(None, "--url", help="Target URL to crawl."),
    save_raw: bool = typer.Option(
        False,
        "--save-raw",
        help="Save raw rendered HTML into the output directory.",
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging."),
) -> None:
    setup_logging(debug=debug)

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

    result, output_file = service.crawl(target_url, save_raw=save_raw)

    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False))
    typer.echo(f"\nSaved JSON to: {output_file}")


@cli.command("extract-text")
def extract_text(
    html_file: str = typer.Option(..., "--html-file", help="Path to a local HTML file."),
    base_url: str = typer.Option(
        "https://example.com",
        "--base-url",
        help="Base URL used to resolve relative links during parsing.",
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

    text = service.extract_text_from_html_file(html_file, base_url=base_url)

    if output_file:
        Path(output_file).write_text(text, encoding="utf-8")
        typer.echo(f"Saved text to: {output_file}")

    typer.echo(text)


if __name__ == "__main__":
    cli()
