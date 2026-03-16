from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    base_url: str
    default_target_url: str
    timeout: int = Field(default=60000)
    retry: int = Field(default=3)
    output_dir: str = Field(default="output")


class CloudflareCredentials(BaseModel):
    account_id: str
    api_token: str


def load_config(config_path: str = "config/config.yaml") -> AppConfig:
    load_dotenv()
    path = Path(config_path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return AppConfig(**data)


def load_cloudflare_credentials() -> CloudflareCredentials:
    load_dotenv()
    account_id = os.getenv("CF_ACCOUNT_ID", "").strip()
    api_token = os.getenv("CF_API_TOKEN", "").strip()

    if not account_id or not api_token:
        raise ValueError(
            "Missing Cloudflare credentials. Please set CF_ACCOUNT_ID and CF_API_TOKEN."
        )

    return CloudflareCredentials(account_id=account_id, api_token=api_token)

