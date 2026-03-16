from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LinkItem(BaseModel):
    title: str | None = None
    url: str


class CrawlResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source: str = "cloudflare_render"
    url: HttpUrl | str
    collected_at: datetime
    title: str | None = None
    main_text: str = ""
    links: list[LinkItem] = Field(default_factory=list)
