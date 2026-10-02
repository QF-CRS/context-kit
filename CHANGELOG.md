# Changelog

All notable changes to Context Kit are documented here.

## [0.1.1] - 2026-10-03

Maintenance release.

- Harden sensitive filename filtering for common credential stores.
- Redact quoted assignment values that contain spaces or comment characters.
- Add regression coverage for the expanded filtering rules.
- Validate source and wheel builds in CI and add monthly Dependabot updates.
- Migrate package license metadata to the SPDX format.

## [0.1.0] - 2026-10-01

Initial public release.

- Add deterministic Markdown and JSON repository context bundles.
- Respect `.gitignore` and skip common generated directories.
- Exclude sensitive filenames and binary or non-UTF-8 files.
- Redact several common credential patterns while preserving original-byte hashes.
- Add file-count and byte-size limits with explicit skip reasons.
- Add `pack` and `inspect` CLI commands and a standard-library-only Python API.
