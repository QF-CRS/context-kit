# Context Kit

[![CI](https://github.com/QF-CRS/context-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/QF-CRS/context-kit/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/QF-CRS/context-kit)](https://github.com/QF-CRS/context-kit/releases)
[![License](https://img.shields.io/github/license/QF-CRS/context-kit)](LICENSE)

Context Kit turns a source repository into a small, deterministic context bundle for code review, onboarding, documentation, and AI coding tools.

It follows the repository's `.gitignore` rules, skips common generated folders, excludes sensitive filenames, detects binary files, applies conservative secret redaction, and produces either Markdown or JSON. The output is plain text, so it works with any editor, review system, or coding assistant without a vendor-specific integration.

## Why it exists

Sharing a whole repository is noisy and can expose credentials. Selecting files by hand is slow and difficult to reproduce. Context Kit gives a team one repeatable command that answers:

- Which files went into the context?
- Which files were left out, and why?
- How large is the resulting bundle?
- Were any likely secret values redacted?
- Can another person or tool regenerate the same result?

The project is intentionally small and dependency-free at runtime. It is designed to be composed with existing Git, editor, CI, and AI workflows rather than replacing them.

## Quick start

Requires Python 3.10 or newer.

```console
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

Inspect a repository before creating a bundle:

```console
context-kit inspect .
```

Create a Markdown bundle for a review or onboarding note:

```console
context-kit pack . --format markdown --output context.md
```

Create a machine-readable bundle for another tool:

```console
context-kit pack . --format json --output context.json
```

The default limits are 200 files, 120 KiB per file, and 1 MiB total source bytes. They can be changed for a particular run:

```console
context-kit pack . --max-files 500 --max-file-bytes 200000 --max-total-bytes 5000000
```

Use `--no-gitignore` only when you have a specific reason to include files ignored by the repository. Use `--no-redact` only in a controlled local workflow; sensitive filenames are still excluded.

## Safety model

Context Kit is a context bundler, not a complete secrets scanner. Its default behavior is deliberately conservative:

1. It skips `.git`, virtual environments, dependency caches, build outputs, IDE metadata, and other common generated directories.
2. It applies Git ignore rules when the root is a Git working tree.
3. It excludes names such as `.env`, `credentials.json`, private-key files, and common certificate or database suffixes.
4. It skips binary and non-UTF-8 files.
5. It redacts several common patterns, including private key blocks, bearer tokens, cloud access keys, and assignment-style values such as `api_key = ...`.
6. It records the SHA-256 of the original file bytes while storing redacted content in the bundle. This makes the source identity auditable without putting the original secret value in the output.

Review the generated bundle before sharing it. Repositories can contain application-specific secret formats that this small, dependency-free scanner does not recognize.

## Output shape

Markdown contains a summary, an ordered file tree, one fenced section per file, and a skipped-file report. JSON contains the same information under schema version `1`, including `path`, `size_bytes`, `sha256`, `redactions`, and redacted `content` for each included file.

The file order and JSON formatting are stable for the same repository state and options. This makes bundles suitable for pull-request attachments, issue discussions, reproducible onboarding notes, and cache keys.

## Development

```console
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

The package uses only the Python standard library at runtime. Pull requests should include focused tests for behavior changes and update the documentation when a safety rule or output field changes.

## Roadmap

- Optional `context-kit.toml` configuration for repository-specific include and exclude rules.
- More output adapters while keeping Markdown and JSON as stable core formats.
- A library API for editor, CI, and pre-commit integrations.
- Feedback-driven rules for additional languages and secret formats.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow. Please report suspected exposure of a real credential privately using [SECURITY.md](SECURITY.md).

## License

Context Kit is released under the [MIT License](LICENSE).
