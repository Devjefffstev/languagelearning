from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env", override=False)

DEFAULT_APP_NAME = "agent_team_adk"
DEFAULT_OLLAMA_CLOUD_API_BASE = "https://ollama.com"
DEFAULT_LOCAL_OLLAMA_BASE_URL = "http://192.168.1.172:11434"
DEFAULT_LOCAL_OLLAMA_MODEL = "gemma4:e2b"
DEFAULT_TEMPERATURE_UNIT = "Celsius"
DEFAULT_BLOCK_KEYWORD = "BLOCK"
DEFAULT_BLOCKED_WEATHER_CITY = "Paris"
DEFAULT_USER_ID = "demo-user"
DEFAULT_SESSION_ID = "demo-session"


def _first_non_empty_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value and value.strip():
            return value.strip()
    return None


def normalize_ollama_chat_model(model_name: str) -> str:
    cleaned = model_name.strip()
    if not cleaned:
        raise ValueError("Model name cannot be empty.")
    if "/" in cleaned:
        return cleaned
    return f"ollama_chat/{cleaned}"


def normalize_temperature_unit(unit: str) -> str:
    lowered = unit.strip().lower()
    if lowered in {"c", "celsius"}:
        return "Celsius"
    if lowered in {"f", "fahrenheit"}:
        return "Fahrenheit"
    raise ValueError("Temperature unit must be Celsius or Fahrenheit.")


@dataclass(frozen=True)
class Settings:
    app_name: str
    cloud_api_key: str
    cloud_model: str
    cloud_api_base: str
    local_greeting_api_base: str
    local_greeting_model: str
    default_temperature_unit: str
    block_keyword: str
    blocked_weather_city: str
    default_user_id: str
    default_session_id: str

    @classmethod
    def from_env(cls) -> "Settings":
        cloud_api_key = _first_non_empty_env("ollama_api_key", "OLLAMA_API_KEY")
        if not cloud_api_key:
            raise RuntimeError(
                "Missing Ollama Cloud API key. Set 'ollama_api_key' or 'OLLAMA_API_KEY'."
            )

        cloud_model_raw = _first_non_empty_env(
            "Ollama_cloud_model", "OLLAMA_CLOUD_MODEL"
        )
        if not cloud_model_raw:
            raise RuntimeError(
                "Missing Ollama Cloud model. Set 'Ollama_cloud_model' or 'OLLAMA_CLOUD_MODEL'."
            )

        default_temperature_unit = normalize_temperature_unit(
            _first_non_empty_env("TEMPERATURE_UNIT_DEFAULT")
            or DEFAULT_TEMPERATURE_UNIT
        )

        return cls(
            app_name=_first_non_empty_env("APP_NAME") or DEFAULT_APP_NAME,
            cloud_api_key=cloud_api_key,
            cloud_model=normalize_ollama_chat_model(cloud_model_raw),
            cloud_api_base=(
                _first_non_empty_env("OLLAMA_CLOUD_API_BASE")
                or DEFAULT_OLLAMA_CLOUD_API_BASE
            ).rstrip("/"),
            local_greeting_api_base=(
                _first_non_empty_env("OLLAMA_BASE_URL")
                or DEFAULT_LOCAL_OLLAMA_BASE_URL
            ).rstrip("/"),
            local_greeting_model=normalize_ollama_chat_model(
                _first_non_empty_env("OLLAMA_MODEL") or DEFAULT_LOCAL_OLLAMA_MODEL
            ),
            default_temperature_unit=default_temperature_unit,
            block_keyword=_first_non_empty_env("BLOCK_KEYWORD")
            or DEFAULT_BLOCK_KEYWORD,
            blocked_weather_city=_first_non_empty_env("BLOCKED_WEATHER_CITY")
            or DEFAULT_BLOCKED_WEATHER_CITY,
            default_user_id=_first_non_empty_env("USER_ID") or DEFAULT_USER_ID,
            default_session_id=_first_non_empty_env("SESSION_ID")
            or DEFAULT_SESSION_ID,
        )

    def initial_session_state(self) -> dict[str, str]:
        return {
            "user_preference_temperature_unit": self.default_temperature_unit,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()

