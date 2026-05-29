from __future__ import annotations

from typing import Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from .config import get_settings


def _last_user_message_text(llm_request: LlmRequest) -> str:
    for content in reversed(llm_request.contents or []):
        if content.role != "user" or not content.parts:
            continue
        for part in content.parts:
            if getattr(part, "text", None):
                return part.text
    return ""


def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """Blocks root-model calls when the configured keyword appears in the latest user message."""
    keyword = get_settings().block_keyword.strip()
    last_user_message = _last_user_message_text(llm_request)
    if keyword and keyword.lower() in last_user_message.lower():
        callback_context.state["guardrail_block_keyword_triggered"] = True
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text=(
                            f"I can't help with that request because it contains the "
                            f"blocked keyword '{keyword}'."
                        )
                    )
                ],
            )
        )
    return None


def block_weather_city_guardrail(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> dict[str, Any] | None:
    """Blocks weather tool calls for the configured city before the tool executes."""
    settings = get_settings()
    if tool.name != "get_weather":
        return None

    requested_city = str(args.get("city", "")).strip()
    if requested_city.lower() != settings.blocked_weather_city.strip().lower():
        return None

    tool_context.state["guardrail_tool_block_triggered"] = True
    return {
        "status": "error",
        "error_message": (
            f"Weather lookups for '{settings.blocked_weather_city}' are blocked "
            "by the tool guardrail."
        ),
    }

