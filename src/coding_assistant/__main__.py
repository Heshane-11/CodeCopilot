import argparse

import uvicorn

from coding_assistant.app import create_app


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="coding-assistant",
        description="Local coding assistant — API server and terminal chat client.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="Start the FastAPI server")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--reload", action="store_true")

    chat = sub.add_parser("chat", help="Interactive terminal chat (requires serve)")
    chat.add_argument(
        "--api-url",
        default=None,
        help="API base URL (default: CHAT_API_BASE_URL or http://127.0.0.1:8000)",
    )
    chat.add_argument(
        "--workspace",
        default=None,
        help="Repository root for tool execution (default: WORKSPACE_ROOT)",
    )
    chat.add_argument("--token", default=None, help="Bearer token if AUTH_REQUIRED=true")
    chat.add_argument("--timeout", type=int, default=None, help="Max seconds per run")
    chat.add_argument("--no-color", action="store_true", help="Disable ANSI colors")

    args = parser.parse_args()
    if args.command == "serve":
        uvicorn.run(
            "coding_assistant.app:create_app",
            factory=True,
            host=args.host,
            port=args.port,
            reload=args.reload,
        )
        return

    if args.command == "chat":
        from coding_assistant.cli.chat import chat_from_settings
        from coding_assistant.config import get_settings

        settings = get_settings()
        raise SystemExit(
            chat_from_settings(
                settings,
                api_url=args.api_url,
                workspace=args.workspace,
                token=args.token,
                run_timeout=float(args.timeout) if args.timeout is not None else None,
                use_color=not args.no_color,
            )
        )


if __name__ == "__main__":
    main()
