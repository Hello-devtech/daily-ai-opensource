from __future__ import annotations

import base64
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed


@dataclass(slots=True)
class ImageGenConfig:
    provider: str = "none"  # none | openai | custom
    model: str = "gpt-image-1"
    output_dir: str = "reports/images"
    size: str = "1024x1024"
    api_base: str = "https://api.openai.com"
    api_key_env: str = "OPENAI_API_KEY"
    endpoint: str = "/v1/images/generations"
    prompt_prefix: str = "为以下 AI 日报条目生成一张专业科技感配图："


class ImageGenerator:
    def __init__(self, config: ImageGenConfig, timeout: float = 60.0) -> None:
        self.config = config
        self.client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self.client.close()

    def generate(self, prompt: str, filename_stem: str) -> str | None:
        provider = self.config.provider.lower()
        if provider == "none":
            return None
        if provider == "openai":
            return self._generate_openai(prompt, filename_stem)
        if provider == "custom":
            return self._generate_custom(prompt, filename_stem)
        raise ValueError(f"Unsupported image provider: {self.config.provider}")

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    def _generate_openai(self, prompt: str, filename_stem: str) -> str | None:
        api_key = os.getenv(self.config.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Missing API key env var: {self.config.api_key_env}. "
                "Set it before enabling image generation."
            )
        url = f"{self.config.api_base.rstrip('/')}{self.config.endpoint}"
        payload = {
            "model": self.config.model,
            "prompt": f"{self.config.prompt_prefix}{prompt}",
            "size": self.config.size,
        }
        response = self.client.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        return self._save_from_response(response.json(), filename_stem)

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    def _generate_custom(self, prompt: str, filename_stem: str) -> str | None:
        api_key = os.getenv(self.config.api_key_env, "")
        url = f"{self.config.api_base.rstrip('/')}{self.config.endpoint}"
        payload = {
            "model": self.config.model,
            "prompt": f"{self.config.prompt_prefix}{prompt}",
            "size": self.config.size,
        }
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = self.client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return self._save_from_response(response.json(), filename_stem)

    def _save_from_response(self, data: dict[str, Any], filename_stem: str) -> str | None:
        items = data.get("data") or []
        if not items:
            return None

        first = items[0]
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_stem = _safe_filename(filename_stem)

        if "b64_json" in first and first["b64_json"]:
            output_file = output_dir / f"{safe_stem}.png"
            output_file.write_bytes(base64.b64decode(first["b64_json"]))
            return output_file.as_posix()

        if "url" in first and first["url"]:
            img_resp = self.client.get(first["url"])
            img_resp.raise_for_status()
            suffix = _guess_suffix_from_content_type(img_resp.headers.get("content-type", ""))
            output_file = output_dir / f"{safe_stem}{suffix}"
            output_file.write_bytes(img_resp.content)
            return output_file.as_posix()

        return None


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", name).strip("-")
    return cleaned[:80] or "image"


def _guess_suffix_from_content_type(content_type: str) -> str:
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    if "jpeg" in content_type or "jpg" in content_type:
        return ".jpg"
    return ".png"
