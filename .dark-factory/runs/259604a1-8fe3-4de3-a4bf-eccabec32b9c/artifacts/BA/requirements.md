# Requirements — Add `subtract(a, b)` with a test

## Goal

Give the application module a `subtract(a, b)` function that returns `a` minus
`b`, plus an automated test for it, so the module's arithmetic matches the
existing `add(a, b)`.

## Context

- Actors: the Developer role (adds the function), the QA role (adds the test),
  and the quality gate (runs `uv run pytest -q` and `uv run ruff check .`).
- Trigger: a text task asking to "Add a subtract(a, b) function to
  app_int/main.py, with a test".
- Expected outcome: `subtract` can be imported from `app_int.main`, returns the
  correct difference, has a test, and the quality gate passes.

## Functional requirements

- **R1.** The module `app_int.main` exposes a public function named `subtract`.
- **R2.** `subtract` takes exactly two positional parameters, named `a` and `b`
  in that order.
- **R3.** `subtract(a, b)` returns the result of `a` minus `b` (the order
  matters: `subtract(5, 3)` returns `2`, not `-2`).
- **R4.** `subtract` returns correct results when the result is negative (e.g.
  `subtract(3, 5)` returns `-2`) and when an operand is zero.
- **R5.** `subtract` has type annotations and a docstring, in the same style as
  the existing `add` function (integer parameters, integer return value).
- **R6.** The test suite under `tests/` contains at least one test that calls
  `subtract` and asserts on its return value.
- **R7.** The existing functions `health_check` and `add` keep working exactly
  as before, and their existing tests still pass.

## Non-functional requirements

- **R8.** `uv run pytest -q` passes with no failures or errors.
- **R9.** `uv run ruff check .` reports no lint violations.
- **R10.** No new runtime or development dependencies are added.

## Assumptions

- **A1.** The task's path "app_int/main.py" means the existing module at
  `src/app_int/main.py` (import path `app_int.main`). No top-level
  `app_int/` directory exists, and none should be created.
- **A2.** `subtract` works on integers, like `add` (`a: int, b: int -> int`).
  Behavior for floats or other types is not specified and is not checked
  beyond what Python's `-` operator does naturally.
- **A3.** No input validation or special error handling is expected. This
  matches `add`.
- **A4.** The test may go in the existing `tests/test_main.py` or in a new file
  under `tests/`. Either way meets R6.

## Out of scope

- Other arithmetic operations (multiply, divide, etc.).
- Changing `add` or `health_check`, or their signatures.
- Exposing `subtract` through a CLI, HTTP endpoint, or `__init__.py`
  re-export.
- Editing the README or other documentation.

## Open questions

None of these block the work. A1–A4 cover the only ambiguities.

## Possible follow-ups (not requirements)

- Re-export `add`/`subtract` from `app_int/__init__.py` if a package-level API
  is wanted.
