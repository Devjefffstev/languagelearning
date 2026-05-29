from __future__ import annotations

from types import SimpleNamespace
import unittest

from google.genai import types

from agentTeamADK.guards import block_keyword_guardrail, block_weather_city_guardrail


class CallbackGuardrailTest(unittest.TestCase):
    def test_block_keyword_guardrail_returns_llm_response(self) -> None:
        context = SimpleNamespace(agent_name="root", state={})
        request = SimpleNamespace(
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part(text="Please BLOCK this request")],
                )
            ]
        )

        response = block_keyword_guardrail(context, request)

        self.assertIsNotNone(response)
        self.assertTrue(context.state["guardrail_block_keyword_triggered"])
        self.assertIn("blocked keyword", response.content.parts[0].text)

    def test_weather_city_guardrail_blocks_paris(self) -> None:
        tool = SimpleNamespace(name="get_weather")
        context = SimpleNamespace(agent_name="root", state={})

        result = block_weather_city_guardrail(tool, {"city": "Paris"}, context)

        self.assertEqual(result["status"], "error")
        self.assertTrue(context.state["guardrail_tool_block_triggered"])


if __name__ == "__main__":
    unittest.main()
