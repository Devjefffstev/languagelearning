from __future__ import annotations

from typing import Any

import httpx
from google.adk.tools.tool_context import ToolContext

from .config import get_settings, normalize_temperature_unit

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODE_LABELS = {
    0: "clear sky",
    1: "mostly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


def _weather_label(code: int | None) -> str:
    if code is None:
        return "unknown conditions"
    return WEATHER_CODE_LABELS.get(code, f"weather code {code}")


def prepare_greeting(name: str | None = None, tool_context: ToolContext | None = None) -> dict[str, Any]:
    """Collects greeting context from session state so the model can personalize the hello."""
    state = tool_context.state
    cleaned_name = name.strip() if name else ""
    if cleaned_name:
        state["user_name"] = cleaned_name

    remembered_name = cleaned_name or state.get("user_name")
    return {
        "status": "success",
        "remembered_name": remembered_name,
        "last_city_checked": state.get("last_city_checked"),
        "preferred_temperature_unit": state.get(
            "user_preference_temperature_unit", get_settings().default_temperature_unit
        ),
    }


def prepare_farewell(tool_context: ToolContext) -> dict[str, Any]:
    """Collects farewell context so the model can say goodbye with session awareness."""
    state = tool_context.state
    return {
        "status": "success",
        "remembered_name": state.get("user_name"),
        "last_city_checked": state.get("last_city_checked"),
        "last_agent_reply": state.get("last_agent_reply"),
    }


def set_temperature_unit(unit: str, tool_context: ToolContext) -> dict[str, Any]:
    """Stores the user's preferred temperature unit in session state."""
    try:
        normalized = normalize_temperature_unit(unit)
    except ValueError as error:
        return {
            "status": "error",
            "error_message": str(error),
            "supported_units": ["Celsius", "Fahrenheit"],
        }

    tool_context.state["user_preference_temperature_unit"] = normalized
    return {
        "status": "success",
        "saved_preference": normalized,
    }


def get_weather(city: str, tool_context: ToolContext) -> dict[str, Any]:
    """Fetches live weather facts for a city and stores the last checked city in session state."""
    settings = get_settings()
    preferred_unit = normalize_temperature_unit(
        str(
            tool_context.state.get(
                "user_preference_temperature_unit",
                settings.default_temperature_unit,
            )
        )
    )
    temperature_unit = "fahrenheit" if preferred_unit == "Fahrenheit" else "celsius"
    temperature_symbol = "°F" if preferred_unit == "Fahrenheit" else "°C"
    previous_city = tool_context.state.get("last_city_checked")

    with httpx.Client(
        timeout=15.0,
        headers={"User-Agent": "agentTeamADK/0.1.0"},
    ) as client:
        try:
            geocode_response = client.get(
                GEOCODING_URL,
                params={
                    "name": city,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
            )
            geocode_response.raise_for_status()
        except httpx.HTTPError as error:
            return {
                "status": "error",
                "error_message": f"Unable to geocode '{city}': {error}",
            }

        geocode_payload = geocode_response.json()
        results = geocode_payload.get("results") or []
        if not results:
            return {
                "status": "error",
                "error_message": f"I couldn't find a city match for '{city}'.",
            }

        match = results[0]
        latitude = match.get("latitude")
        longitude = match.get("longitude")
        if latitude is None or longitude is None:
            return {
                "status": "error",
                "error_message": f"Weather lookup is missing coordinates for '{city}'.",
            }

        try:
            forecast_response = client.get(
                FORECAST_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": (
                        "temperature_2m,apparent_temperature,"
                        "relative_humidity_2m,weather_code,wind_speed_10m"
                    ),
                    "temperature_unit": temperature_unit,
                    "wind_speed_unit": "kmh",
                    "timezone": "auto",
                },
            )
            forecast_response.raise_for_status()
        except httpx.HTTPError as error:
            return {
                "status": "error",
                "error_message": f"Unable to fetch live weather for '{city}': {error}",
            }

    forecast_payload = forecast_response.json()
    current = forecast_payload.get("current")
    if not isinstance(current, dict):
        return {
            "status": "error",
            "error_message": f"Weather data for '{city}' did not include a current conditions block.",
        }

    resolved_city = match.get("name") or city
    region = match.get("admin1")
    country = match.get("country")
    tool_context.state["last_city_checked"] = resolved_city

    return {
        "status": "success",
        "location": {
            "city": resolved_city,
            "region": region,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
        },
        "current_weather": {
            "temperature": current.get("temperature_2m"),
            "temperature_unit": temperature_symbol,
            "feels_like": current.get("apparent_temperature"),
            "relative_humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "condition": _weather_label(current.get("weather_code")),
            "observed_at": current.get("time"),
        },
        "memory": {
            "preferred_temperature_unit": preferred_unit,
            "previous_city_checked": previous_city,
        },
    }

