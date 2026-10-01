"""Command-line interface for Context Kit."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .model import PackOptions, build_pack


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="context-kit",
        description="Build a safe, deterministic context bundle from a repository.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    pack = subparsers.add_parser(
        "pack",
        help="discover files and render a Markdown or JSON context bundle",
    )
    pack.add_argument("root", nargs="?", default=".", help="repository directory")
    pack.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="output format (default: markdown)",
    )
    pack.add_argument("--output", type=Path, help="write the bundle to a file")
    pack.add_argument("--max-files", type=int, default=200)
    pack.add_argument("--max-file-bytes", type=int, default=120_000)
    pack.add_argument("--max-total-bytes", type=int, default=1_000_000)
    pack.add_argument(
        "--no-gitignore",
        action="store_true",
        help="do not use the repository's .gitignore rules",
    )
    pack.add_argument(
        "--no-redact",
        action="store_true",
        help="disable value redaction; sensitive filenames remain excluded",
    )

    inspect = subparsers.add_parser(
        "inspect",
        help="print a concise inclusion and exclusion report",
    )
    inspect.add_argument("root", nargs="?", default=".", help="repository directory")
    inspect.add_argument("--max-files", type=int, default=200)
    inspect.add_argument("--max-file-bytes", type=int, default=120_000)
    inspect.add_argument("--max-total-bytes", type=int, default=1_000_000)
    inspect.add_argument("--no-gitignore", action="store_true")

    return parser


def _options(args: argparse.Namespace) -> PackOptions:
    return PackOptions(
        root=Path(args.root),
        max_files=args.max_files,
        max_file_bytes=args.max_file_bytes,
        max_total_bytes=args.max_total_bytes,
        respect_gitignore=not getattr(args, "no_gitignore", False),
        redact_secrets=not getattr(args, "no_redact", False),
    )


def _inspect_text(result) -> str:
    lines = [
        f"Root: {result.root_name}",
        f"Included: {len(result.files)} files / {result.source_bytes} source bytes",
        f"Skipped: {len(result.skipped)} files",
        f"Redactions: {result.redaction_count}",
        "",
        "Included files:",
    ]
    lines.extend(f"  + {record.path}" for record in result.files)
    if result.skipped:
        lines.extend(["", "Skipped files:"])
        lines.extend(f"  - {item['path']}: {item['reason']}" for item in result.skipped)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = build_pack(_options(args))
    except (OSError, TypeError, ValueError) as exc:
        parser.error(str(exc))

    if args.command == "inspect":
        print(_inspect_text(result))
        return 0

    rendered = result.to_json() if args.format == "json" else result.to_markdown()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(
            f"Wrote {args.output} ({len(result.files)} files, "
            f"{result.redaction_count} redactions)"
        )
    else:
        sys.stdout.write(rendered)
    return 0
