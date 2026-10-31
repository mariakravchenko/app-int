# Requirements — Add `subtract(a, b)` with a test

## Goal

Extend the application module with a `subtract(a, b)` function that returns the
difference `a - b`, and cover it with an automated test.

## Context

- **Actor:** a caller (developer or other code) importing from `app_int.main`.
- **Trigger:** the caller invokes `subtract(a, b)`.
- **Expected outcome:** the function returns `a` minus `b`.
- **Baseline:** `src/app_int/main.py` already provides `health_check()` and
  `add(a: int, b: int) -> int`; `tests/test_main.py` tests both.

## Functional requirements

- **REQ-1** — The module `app_int.main` exposes a public function named
  `subtract` that is importable via `from app_int.main import subtract`.
- **REQ-2** — `subtract` accepts exactly two positional parameters, named `a`
  and `b`, in that order.
- **REQ-3** — `subtract(a, b)` returns the result of `a - b` (the first argument
  minus the second), e.g. `subtract(5, 3) == 2`.
- **REQ-4** — `subtract` returns correct results when the result is negative,
  e.g. `subtract(3, 5) == -2`.
- **REQ-5** — `subtract` returns correct results for zero and negative
  operands, e.g. `subtract(0, 0) == 0`, `subtract(-2, -3) == 1`.
- **REQ-6** — `subtract` has a docstring describing what it returns, consistent
  with the existing `add` function. *(Assumption — inferred from module
  conventions.)*
- **REQ-7** — `subtract` is type-annotated as taking two `int` arguments and
  returning an `int`, consistent with the existing `add` signature.
  *(Assumption — inferred from `add(a: int, b: int) -> int`.)*

## Test requirements

- **REQ-8** — The test suite under `tests/` contains at least one test that
  calls `subtract` and asserts its return value.
- **REQ-9** — The test suite covers at least one case whose expected result is
  negative (verifying argument order, i.e. `a - b` not `b - a`).

## Non-functional requirements

- **REQ-10** — The existing behaviour of `health_check()` and `add()` is
  unchanged, and their existing tests still pass.
- **REQ-11** — The quality gate passes: `uv run pytest -q` exits 0 and
  `uv run ruff check .` exits 0.
- **REQ-12** — No new runtime dependencies are added to the project.

## Assumptions

- **A-1** — The task path `app_int/main.py` refers to the existing file
  `src/app_int/main.py` (the package lives under `src/`).
- **A-2** — Integer inputs only, mirroring `add`. Behaviour for non-integer
  inputs (floats, strings, `None`) is not specified and need not be validated or
  tested.
- **A-3** — No input validation or error handling is required; Python's native
  integer subtraction semantics (arbitrary precision, no overflow) apply.
- **A-4** — The test may live in the existing `tests/test_main.py` or a new test
  file under `tests/`; either satisfies REQ-8.

## Out of scope

- Other arithmetic operations (multiply, divide, etc.).
- Input type validation, coercion, or custom error messages.
- CLI, API, or UI exposure of `subtract`.
- Changes to `README.md`, CI workflows, or Dark Factory configuration.

## Open questions

None blocking. All gaps are covered by assumptions A-1 to A-4.

## Follow-ups (not requirements)

- Consider a parametrized test style for arithmetic helpers if more are added.
