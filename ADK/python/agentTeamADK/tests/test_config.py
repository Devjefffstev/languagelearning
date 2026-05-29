from __future__ import annotations

import os
import unittest

from agentTeamADK.config import (
    Settings,
    get_settings,
    normalize_ollama_chat_model,
    normalize_temperature_unit,
)


class SettingsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.keys = [
            "ollama_api_key",
            "OLLAMA_API_KEY",
            "Ollama_cloud_model",
            "OLLAMA_CLOUD_MODEL",
            "OLLAMA_CLOUD_API_BASE",
            "OLLAMA_BASE_URL",
            "OLLAMA_MODEL",
            "TEMPERATURE_UNIT_DEFAULT",
            "BLOCK_KEYWORD",
            "BLOCKED_WEATHER_CITY",
            "APP_NAME",
            "USER_ID",
            "SESSION_ID",
        ]
        self.original = {key: os.environ.get(key) for key in self.keys}
        for key in self.keys:
            os.environ.pop(key, None)
        get_settings.cache_clear()

    def tearDown(self) -> None:
        for key in self.keys:
            os.environ.pop(key, None)
            if self.original[key] is not None:
                os.environ[key] = self.original[key]
        get_settings.cache_clear()

    def test_settings_normalize_cloud_and_local_models(self) -> None:
        os.environ["ollama_api_key"] = "test-key"
        os.environ["Ollama_cloud_model"] = "gpt-oss:120b"
        os.environ["OLLAMA_MODEL"] = "gemma4:e2b"

        settings = Settings.from_env()

        self.assertEqual(settings.cloud_model, "ollama_chat/gpt-oss:120b")
        self.assertEqual(settings.local_greeting_model, "ollama_chat/gemma4:e2b")

    def test_temperature_unit_normalization(self) -> None:
        self.assertEqual(normalize_temperature_unit("c"), "Celsius")
        self.assertEqual(normalize_temperature_unit("Fahrenheit"), "Fahrenheit")

    def test_model_normalization_preserves_prefixed_name(self) -> None:
        self.assertEqual(
            normalize_ollama_chat_model("ollama_chat/gemma4:e2b"),
            "ollama_chat/gemma4:e2b",
        )


if __name__ == "__main__":
    unittest.main()

