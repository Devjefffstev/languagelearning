from __future__ import annotations

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .config import get_settings
from .guards import block_keyword_guardrail, block_weather_city_guardrail
from .tools import get_weather, prepare_farewell, prepare_greeting, set_temperature_unit

settings = get_settings()

cloud_model = LiteLlm(
    model=settings.cloud_model,
    api_base=settings.cloud_api_base,
    api_key=settings.cloud_api_key,
)

local_greeting_model = LiteLlm(
    model=settings.local_greeting_model,
    api_base=settings.local_greeting_api_base,
)

greeting_agent = Agent(
    name="greeting_agent",
    model=local_greeting_model,
    description="Handles simple greetings and short introductions.",
    instruction=(
        "You are the greeting specialist. Use the 'prepare_greeting' tool every time "
        "before you answer so you can personalize the hello from session memory. "
        "If the user gives you a name, pass it to the tool. Write the final greeting "
        "yourself instead of copying the tool output verbatim."
    ),
    tools=[prepare_greeting],
)

farewell_agent = Agent(
    name="farewell_agent",
    model=cloud_model,
    description="Handles simple farewells and conversation wrap-ups.",
    instruction=(
        "You are the farewell specialist. Use the 'prepare_farewell' tool to gather "
        "session context, then write a short natural goodbye. If session memory is "
        "useful, you may mention it briefly."
    ),
    tools=[prepare_farewell],
)

root_agent = Agent(
    name="weather_agent_team",
    model=cloud_model,
    description=(
        "Main weather agent team coordinator that handles weather questions, "
        "temperature preferences, and delegates greetings and farewells."
    ),
    instruction=(
        "You are the main coordinator for a weather-focused agent team. "
        "Delegate pure greetings to 'greeting_agent'. "
        "Delegate pure farewells to 'farewell_agent'. "
        "If the user wants to set or change a temperature unit preference, use "
        "'set_temperature_unit'. "
        "If the user asks for weather, use 'get_weather'. "
        "Never invent weather facts. Base weather answers only on the tool output. "
        "If a tool reports an error, explain it clearly and do not pretend the request succeeded. "
        "Write the final response in natural language instead of repeating raw JSON."
    ),
    tools=[get_weather, set_temperature_unit],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_agent_reply",
    before_model_callback=block_keyword_guardrail,
    before_tool_callback=block_weather_city_guardrail,
)

