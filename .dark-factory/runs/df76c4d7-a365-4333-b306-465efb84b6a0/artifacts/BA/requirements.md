# Requirements — Add `divide(a, b)` to `app_int.main`, with a test

## Goal

Extend the application's public surface with a `divide(a, b)` function in the
`app_int.main` module, alongside the existing `add` and `health_check`, and cover
it with automated tests so the quality gate verifies its behaviour.

## Context

- Actor: a caller of the `app_int` Python package (library consumer / test suite).
- Trigger: the caller invokes `divide(a, b)` with two numbers.
- Expected outcome: the caller receives the quotient of `a` divided by `b`.
- The task names `app_int/main.py`; in this repository that module lives at
  `src/app_int/main.py` and is imported as `app_int.main`. The task is
  interpreted as referring to that existing module.

## Functional requirements

- **R1.** The module `app_int.main` exposes a public function named `divide`.
- **R2.** `divide` accepts exactly two positional arguments, the dividend `a`
  and the divisor `b`, in that order.
- **R3.** For a non-zero divisor, `divide(a, b)` returns the mathematical
  quotient `a / b` (true division, not floor/integer division) — e.g.
  `divide(6, 3) == 2`, `divide(7, 2) == 3.5`. *(Assumption A1.)*
- **R4.** `divide` handles negative operands with ordinary sign rules — e.g.
  `divide(-6, 3) == -2`, `divide(6, -4) == -1.5`.
- **R5.** A zero dividend with a non-zero divisor returns zero — e.g.
  `divide(0, 5) == 0`.
- **R6.** Calling `divide(a, 0)` raises `ZeroDivisionError`; it does not return
  a value (no `None`, `inf`, `nan`, or sentinel). *(Assumption A2.)*
- **R7.** `divide` has a docstring describing what it returns, consistent with
  the existing functions in the module.
- **R8.** The existing public functions `add` and `health_check` keep their
  current behaviour.

## Test requirements

- **R9.** The test suite under `tests/` contains at least one test that
  exercises `divide` with a non-zero divisor and asserts the returned quotient.
- **R10.** The test suite contains a test asserting that a non-integer
  quotient is returned exactly (e.g. `divide(7, 2) == 3.5`), demonstrating true
  division.
- **R11.** The test suite contains a test asserting that `divide(x, 0)` raises
  `ZeroDivisionError`.

## Non-functional requirements

- **R12.** `uv run pytest -q` passes with all tests (existing and new) green.
- **R13.** `uv run ruff check .` reports no violations.
- **R14.** `divide`'s signature carries type annotations for both parameters
  and the return value, matching the annotated style of the existing module.
- **R15.** No new runtime dependencies are added to the project.

## Assumptions

- **A1.** "Divide" means true division (Python `/` semantics), so the result
  may be a non-integer value even when both inputs are integers. Integer/floor
  division was not requested.
- **A2.** Division by zero should surface as an error to the caller, using the
  language's standard `ZeroDivisionError`, rather than a custom exception or a
  silent sentinel value.
- **A3.** `app_int/main.py` in the task refers to the existing
  `src/app_int/main.py` (import path `app_int.main`); no new module is created.
- **A4.** Inputs are numbers (ints and/or floats). Behaviour for non-numeric
  inputs is not specified and is not required to be tested.

## Out of scope

- Input validation / custom error messages for non-numeric arguments.
- Other arithmetic operations (subtract, multiply, modulo, etc.).
- Rounding, precision control, or `Decimal`/`Fraction` support.
- Any CLI, HTTP, or UI exposure of `divide`.
- Changes to CI, packaging, or Dark Factory configuration.

## Open questions (non-blocking)

- None blocking. If stakeholders prefer integer division, or a value other than
  an exception for a zero divisor, A1/A2 (and R3, R6, R10, R11) would change.

## Possible follow-ups

- Align `add`'s type hints with `divide` (e.g. accept floats) if a consistent
  numeric API is desired.
