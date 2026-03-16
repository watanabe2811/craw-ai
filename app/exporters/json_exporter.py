from __future__ import annotations

import json
from pathlib import Path

from app.models.response_models import CrawlResult
from app.utils.logger import get_logger


logger = get_logger(__name__)


class JsonExporter:
    def __init__(self, output_dir: str) -> None:
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def export(self, result: CrawlResult, filename: str) -> Path:
        file_path = self.output_path / filename
        file_path.write_text(
            json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.info("Exported normalized JSON to %s", file_path)
        return file_path

    def export_raw_html(self, html: str, filename: str) -> Path:
        file_path = self.output_path / filename
        file_path.write_text(html, encoding="utf-8")
        logger.info("Saved raw rendered HTML to %s", file_path)
        return file_path

