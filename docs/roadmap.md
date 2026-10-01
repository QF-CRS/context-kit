# Roadmap

This roadmap is a set of testable directions, not a promise of dates. Real usage and issue discussions should decide the order.

## Near term

- Add an optional `context-kit.toml` file for project-specific include, exclude, and redaction rules.
- Add a dry-run mode that prints the planned bundle without reading file contents into the output.
- Improve diagnostics for repositories with nested Git worktrees.

## Later

- Provide a small pre-commit and CI integration.
- Add adapters for additional review and documentation formats while preserving the core schema.
- Expand language-aware secret patterns based on reviewed reports and regression tests.

Every safety or schema change should be accompanied by a focused test and a documented migration note when needed.
