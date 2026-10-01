# Contributing to Context Kit

Thanks for helping make repository context safer and easier to share.

## Local setup

Use Python 3.10 or newer, create a virtual environment, and install the project in editable mode:

```console
python -m pip install -e .
```

Run the same checks used by CI:

```console
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

## Pull requests

Keep changes focused. Explain the user problem, the behavior change, and the verification you ran. Changes to discovery, ignore handling, redaction, limits, or output schemas should include a regression test.

Avoid adding a runtime dependency for a feature that can reasonably use the standard library. If a dependency is necessary, explain the maintenance and security tradeoff in the pull request.

## Reporting security issues

Do not paste real credentials into a public issue or pull request. Follow [SECURITY.md](SECURITY.md) for private reporting guidance.
