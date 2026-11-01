# Requirements — Add a `cube(n)` function with a test

## Goal
Expose a `cube(n)` function from the application's `main` module that returns
`n` raised to the third power, and cover it with an automated test.

## Context
- Actor: developers/consumers importing `app_int.main`.
- Trigger: calling `cube(n)`.
- Expected outcome: the cube of `n` is returned.
- The task names `app_int/main.py`; in this repository that module lives at
  `src/app_int/main.py` (importable as `app_int.main`). Existing tests live in
  `tests/test_main.py`.

## Functional requirements
1. **R1** — The module `app_int.main` (file `src/app_int/main.py`) shall define
   a public function named `cube` that accepts a single argument `n`.
2. **R2** — `cube(n)` shall return `n` raised to the third power (`n * n * n`)
   for any integer `n`, including positive integers, zero, and negative
   integers (e.g. `cube(3) == 27`, `cube(0) == 0`, `cube(-2) == -8`).
3. **R3** — `cube` shall be importable via `from app_int.main import cube`.
4. **R4** — The test suite under `tests/` shall contain at least one test that
   calls `cube` and asserts on its result.

## Non-functional requirements
5. **R5** — Existing behaviour of `health_check` and `add` shall remain
   unchanged, and their existing tests shall continue to pass.
6. **R6** — The repository quality gate shall pass: `uv run pytest -q` and
   `uv run ruff check .` both exit with status 0.
7. **R7** — `cube` shall follow the existing style of the module: a
   type-annotated signature and a docstring, consistent with `add`.

## Assumptions
- **A1** — "`app_int/main.py`" refers to the existing `src/app_int/main.py`.
- **A2** — Integer input (`int -> int`) is the required contract, matching the
  existing `add(a: int, b: int) -> int`. Behaviour for floats or other numeric
  types is not required (nor forbidden).
- **A3** — No input validation or error raising for non-numeric input is
  required.
- **A4** — R7 (annotations + docstring) is inferred from module conventions,
  not stated in the task.

## Out of scope
- Any other math functions, a CLI/HTTP surface, or README/documentation changes.
- Changes to CI, Dark Factory configuration, or dependencies.

## Open questions
- None blocking.

## Follow-ups (not requirements)
- None.
