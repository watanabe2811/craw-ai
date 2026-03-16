---
name: openclaw-cafef-report
description: Use when OpenClaw needs to crawl one JavaScript/AJAX page through Cloudflare Browser Rendering API and return a readable CafeF-style market report by default, or JSON on request. This skill assumes the repo is available locally, `.env` contains `CF_ACCOUNT_ID` and `CF_API_TOKEN`, and the preferred entrypoints are the bundled shell wrappers.
---

# OpenClaw CafeF Report

Use this skill when the user wants a single-page crawl from a dynamic site and expects a readable report instead of raw HTML or generic scraped text.

## Workflow

1. Confirm the project repo exists and `.env` is configured with Cloudflare credentials.
2. Prefer the shell wrapper:
   - Default report output: `./bin/openclaw-crawl.sh`
   - Discord-friendly text output: `./bin/openclaw-discord.sh`
   - JSON output: `./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn" json`
3. If the user asks to update the local project before running, use `./bin/openclaw-update.sh`.
4. If the user already has a rendered HTML file and wants structured extraction:
   - JSON sections: `./scripts/extract_cafef_sections.py`
   - Human-readable report from sections JSON: `./scripts/render_cafef_report.py`

## Default command

Run this from the repository root:

```bash
./bin/openclaw-crawl.sh
```

For Discord bots that need plain text on stdout:

```bash
./bin/openclaw-discord.sh
```

Arguments:

- First argument: target URL. Default is `https://cafef.vn/du-lieu.chn`
- Second argument: output format, `report` or `json`. Default is `report`
- Third argument: optional `--save-raw`

Discord wrapper arguments:

- First argument: target URL. Default is `https://cafef.vn/du-lieu.chn`
- Second argument: output format, `report` or `json`. Default is `report`
- Third argument: max characters for stdout. Default is `1900`
- Fourth argument: optional `--save-raw`

Examples:

```bash
./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn"
./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn" json
./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn" report --save-raw
./bin/openclaw-discord.sh "https://cafef.vn/du-lieu.chn"
./bin/openclaw-discord.sh "https://cafef.vn/du-lieu.chn" report 1900
```

## Expected outputs

- Main default output: human-readable report in console and `output/*.report.txt`
- Side output: normalized JSON in `output/*.json`
- Optional raw HTML: `output/*.html`
- Discord wrapper stdout: only the main text content, trimmed if it exceeds the character limit

## When to switch modes

- Use default `report` when the user wants a readable summary or market-style report.
- Use `json` when the user needs machine-readable output, downstream processing, or debugging.
- Use HTML extraction scripts only when the user already has a local HTML file or asks for post-processing without re-crawling.
