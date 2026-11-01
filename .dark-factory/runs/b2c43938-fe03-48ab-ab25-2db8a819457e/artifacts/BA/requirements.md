# Requirements — Add a `cube(n)` function with a test

## Goal

Provide a public `cube(n)` function in the application's `main` module that
returns `n` raised to the third power, together with automated tests that
verify it.

## Context

- Actor: a developer or caller who imports `app_int.main`.
- Trigger: calling `cube(n)`.
- Expected outcome: the function returns `n * n * n`.
- The task names `app_int/main.py`. In this repository the module lives at
  `src/app_int/main.py` and is imported as `app_int.main`. That is the file
  meant (assumption A1).

## Functional requirements

- **R1.** The module `app_int.main` exposes a public function named `cube`.
- **R2.** `cube` accepts exactly one positional argument named `n`.
- **R3.** For any integer `n`, `cube(n)` returns an `int` equal to `n * n * n`.
- **R4.** `cube` returns correct results for positive integers (for example
  `cube(3) == 27`).
- **R5.** `cube` returns correct results for zero (`cube(0) == 0`).
- **R6.** `cube` returns correct results for negative integers, keeping the
  sign (for example `cube(-2) == -8`).
- **R7.** `cube` does not change the behaviour of the module's existing public
  functions (`health_check`, `add`).

## Non-functional requirements

- **R8.** `cube` has a type annotation for its parameter and its return value,
  matching the style of the existing functions in the module (assumption A2).
- **R9.** `cube` has a docstring, matching the style of the existing functions
  in the module (assumption A2).
- **R10.** The test suite includes at least one automated test that calls
  `app_int.main.cube` and checks its result.
- **R11.** The quality gate passes: `uv run pytest -q` exits 0 and
  `uv run ruff check .` exits 0.

## Assumptions

- **A1.** "`app_int/main.py`" in the task means `src/app_int/main.py` (import
  path `app_int.main`). No other file of that name exists.
- **A2.** `n` is an integer (`int`), the same as the sibling `add(a: int, b: int)`
  function. Annotations and a docstring are expected because every existing
  function in the module has them.
- **A3.** The task does not ask for input validation. Behaviour for non-integer
  inputs such as floats, strings or `None` is not specified, and no specific
  error handling is required.
- **A4.** New tests go in the existing test suite under `tests/`, either in
  `tests/test_main.py` or in a new test module. Either location is acceptable.

## Out of scope

- Input validation or custom exceptions for non-integer arguments.
- Generalised power functions, such as `power(n, k)`, and other math helpers.
- Changes to `health_check`, `add`, packaging, CI or documentation.

## Open questions

None block the work. The assumptions above cover the gaps.

## Possible follow-ups (not requirements)

- Decide whether `cube` should accept `float` as well, or reject non-numeric
  input explicitly.
