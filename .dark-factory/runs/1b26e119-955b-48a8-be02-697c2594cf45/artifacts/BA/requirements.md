# Requirements: Add `cube(n)` to the app, with a test

## Goal
Add a `cube(n)` function to the application's `main` module that returns `n`
raised to the third power, and cover it with an automated test.

## Context
- **Actor:** code that uses the `app_int.main` module, including the test suite.
- **Trigger:** a call to `cube(n)`.
- **Expected outcome:** the call returns `n * n * n`.

## Functional requirements
- **R1.** The module `app_int.main` (file `src/app_int/main.py`) defines a public function named `cube`.
- **R2.** `cube` takes exactly one positional argument, `n`.
- **R3.** For an integer input `n`, `cube(n)` returns the integer `n ** 3` (for example, `cube(3) == 27`).
- **R4.** `cube` returns correct results for zero and negative integers (`cube(0) == 0`, `cube(-2) == -8`).
- **R5.** `cube` can be imported with `from app_int.main import cube`.
- **R6.** `cube` has a docstring that says what it returns, like the existing functions in the module.
- **R7.** The test suite under `tests/` has at least one test that calls `cube` and checks its result.

## Non-functional requirements
- **R8.** `cube` has type annotations in the module's existing style (integer in, integer out).
- **R9.** Existing behaviour does not change: `health_check()`, `add()` and their tests keep passing.
- **R10.** The quality gate passes: `uv run pytest -q` and `uv run ruff check .` both exit with status 0.
- **R11.** No new runtime or dev dependencies are added.

## Assumptions
- **A1.** The task names `app_int/main.py`. The repository uses a src layout, so the actual file is `src/app_int/main.py`, and that file is the target.
- **A2.** "cube" means the arithmetic third power (`n ** 3`). It does not mean a geometric shape or a data cube.
- **A3.** The required inputs are integers, in line with the existing `add(a: int, b: int) -> int`. The task does not say what should happen for non-integer inputs (floats, strings, `None`), so no input validation or custom error is required.
- **A4.** The test can go in the existing `tests/test_main.py` or in a new file under `tests/`. Either is acceptable.

## Out of scope
- Input validation, custom exceptions, or support for non-numeric types.
- CLI, API, or documentation changes (README and so on), apart from the function's docstring.
- Refactoring the existing functions.

## Open questions
- None that block this work.

## Possible follow-ups (not requirements)
- Decide how float and non-numeric inputs should behave, if that is ever needed.
