from __future__ import annotations

import argparse
import asyncio
import json

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .agent import root_agent
from .config import get_settings


async def call_agent_async(
    query: str, *, runner: Runner, user_id: str, session_id: str
) -> str:
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response = "The agent did not return a final response."

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if not event.is_final_response():
            continue

        if event.content and event.content.parts:
            parts = [
                part.text
                for part in event.content.parts
                if getattr(part, "text", None)
            ]
            if parts:
                final_response = "\n".join(parts)
        elif event.error_message:
            final_response = event.error_message

    return final_response


async def build_runner(user_id: str, session_id: str) -> tuple[Runner, InMemorySessionService]:
    settings = get_settings()
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=settings.app_name,
        user_id=user_id,
        session_id=session_id,
        state=settings.initial_session_state(),
    )
    runner = Runner(
        agent=root_agent,
        app_name=settings.app_name,
        session_service=session_service,
    )
    return runner, session_service


async def print_state(
    *, session_service: InMemorySessionService, user_id: str, session_id: str
) -> None:
    settings = get_settings()
    session = await session_service.get_session(
        app_name=settings.app_name,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        print("No session found.")
        return
    print(json.dumps(session.state, indent=2, sort_keys=True))


async def run(args: argparse.Namespace) -> None:
    settings = get_settings()
    user_id = args.user_id or settings.default_user_id
    session_id = args.session_id or settings.default_session_id
    runner, session_service = await build_runner(user_id, session_id)

    if args.query:
        response = await call_agent_async(
            args.query,
            runner=runner,
            user_id=user_id,
            session_id=session_id,
        )
        print(response)
        if args.show_state:
            await print_state(
                session_service=session_service,
                user_id=user_id,
                session_id=session_id,
            )
        return

    print("agentTeamADK interactive session")
    print("Type /state to inspect memory or /quit to exit.")

    while True:
        try:
            query = input("> ").strip()
        except EOFError:
            print()
            break

        if not query:
            continue
        if query in {"/quit", "/exit"}:
            break
        if query == "/state":
            await print_state(
                session_service=session_service,
                user_id=user_id,
                session_id=session_id,
            )
            continue

        response = await call_agent_async(
            query,
            runner=runner,
            user_id=user_id,
            session_id=session_id,
        )
        print(response)
        if args.show_state:
            await print_state(
                session_service=session_service,
                user_id=user_id,
                session_id=session_id,
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the agentTeamADK demo.")
    parser.add_argument("--query", help="Run a single query and exit.")
    parser.add_argument("--user-id", help="Override the default user id.")
    parser.add_argument("--session-id", help="Override the default session id.")
    parser.add_argument(
        "--show-state",
        action="store_true",
        help="Print session state after each response.",
    )
    return parser.parse_args()


def main() -> None:
    asyncio.run(run(parse_args()))

