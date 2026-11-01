# Requirements — Add `square(n)` to `app_int.main`, with a test

## Goal

Give the `app_int.main` module a public `square(n)` function that returns `n` multiplied by itself, and add an automated test that checks it.

## Context

- **Actors:** the Developer role (adds the function) and the QA role (adds the test). Downstream, anyone who imports `app_int.main`.
- **Trigger:** a text task asking for "a square(n) function in app_int/main.py, with a test".
- **Expected outcome:** `from app_int.main import square` works, `square(n)` returns `n * n`, a test checks this, and the quality gate (`uv run pytest -q`, `uv run ruff check .`) passes.

## Functional requirements

- **R-1** The module `app_int.main` (file `src/app_int/main.py`) defines a public function named `square`.
- **R-2** `square` takes exactly one positional argument, `n`.
- **R-3** For an integer input `n`, `square(n)` returns the integer `n * n`.
- **R-4** `square` returns the correct, non-negative result for negative integers (for example, `square(-3) == 9`).
- **R-5** `square(0)` returns `0`.
- **R-6** `square` has a docstring that describes what it returns. This matches the existing functions in the module.
- **R-7** `square` has type annotations for its parameter and return value. This matches the existing functions in the module.
- **R-8** The test suite under `tests/` has at least one test that imports `square` from `app_int.main` and checks its result for at least one positive integer, one negative integer, and zero.

## Non-functional requirements

- **R-9** The existing public functions `health_check` and `add` keep their behaviour, and their existing tests still pass.
- **R-10** `uv run pytest -q` exits with status 0.
- **R-11** `uv run ruff check .` exits with status 0.
- **R-12** No new runtime dependencies are added to `pyproject.toml`.

## Assumptions (inferred, not stated in the task)

- **A-1** The task's path "app_int/main.py" means `src/app_int/main.py`. That is the repository's only `app_int/main.py`.
- **A-2** The function's contract covers integers (`int -> int`), matching the style of `add(a: int, b: int) -> int`. Behaviour for floats, bools or other numeric types is not part of the contract and is not tested.
- **A-3** Input validation (for example, raising `TypeError` on non-numeric input) is not required.
- **A-4** "With a test" means one or more pytest tests. Adding them to the existing `tests/test_main.py` is acceptable.

## Out of scope

- Other math helpers (cube, power, square root, and so on).
- A CLI, API endpoint or any other interface that exposes `square`.
- Changes to the README, CI workflows or Dark Factory configuration.
- Refactoring the existing functions.

## Open questions

None of these block the work; each one is covered by an assumption above.

## Possible follow-ups (not requirements)

- Decide whether `square` should accept floats or other numeric types (see A-2).
