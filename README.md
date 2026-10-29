# app-int

A small integration target repository: a minimal Python app used to exercise
[Dark Factory](https://github.com/mariakravchenko/dark-factory) end to end
against a real GitHub repository.

- `src/app_int/` — the application code the Developer role edits.
- `tests/` — the test suite QA edits and the quality gate runs.
- `.dark-factory.yaml` / `.dark-factory/` — Dark Factory's pipeline
  configuration for this repo.

See [`DARK_FACTORY_SETUP.md`](./DARK_FACTORY_SETUP.md) for the full setup
walkthrough (keys, install steps, first run).

## Running the app's own tests

```bash
uv sync --all-extras --dev
uv run pytest -q
uv run ruff check .
```
