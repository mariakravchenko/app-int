# Requirements: `subtract(a, b)` function with a test

## Goal

Add a `subtract(a, b)` function to the application module, returning `a - b`, and add an
automated test for it.

## Context

- Actor: a caller of the `app_int` library code (and the test suite).
- Trigger: calling `subtract(a, b)`.
- Expected outcome: the function returns the difference `a - b`.
- The task names `app_int/main.py`; in this repository that module lives at
  `src/app_int/main.py`, importable as `app_int.main`.
- The module already has an `add(a: int, b: int) -> int` function. `subtract` should
  follow the same conventions.

## Functional requirements

- **R1.** The module `app_int.main` (file `src/app_int/main.py`) exposes a public function
  named `subtract`.
- **R2.** `subtract` takes exactly two positional parameters, named `a` and `b`, in that order.
- **R3.** `subtract(a, b)` returns `a - b` (the second argument subtracted from the first).
- **R4.** `subtract` returns the right result for zero, negative operands, and results
  below zero (for example `subtract(2, 5) == -3`).
- **R5.** `subtract` has type annotations matching the existing `add` function: integer
  parameters and an integer return type. *(Assumption: inferred from `add`'s signature.)*
- **R6.** `subtract` has a docstring that says what it returns, like `add` does.
  *(Assumption: inferred from the module's existing conventions.)*
- **R7.** The existing functions `health_check` and `add` keep working exactly as before.

## Test requirements

- **R8.** The test suite under `tests/` includes at least one test that imports `subtract`
  from `app_int.main` and checks its return value.
- **R9.** The new test(s) check at least one case with a positive result and one case with a
  negative result, so that swapped operands (`b - a`) would be caught.

## Non-functional requirements

- **R10.** The quality gate passes: `uv run pytest -q` exits 0 with all tests passing.
- **R11.** The quality gate passes: `uv run ruff check .` exits 0 with no findings.
- **R12.** No new runtime or dev dependencies are added.

## Assumptions

- A1. "app_int/main.py" in the task means `src/app_int/main.py`, the only such module in the repo.
- A2. Integer annotations (R5) follow `add`. The task doesn't say how non-integer inputs
  should behave, and this spec doesn't require any validation or rejection of them.
- A3. Overflow is not a concern; Python integers have arbitrary precision.

## Out of scope

- Other arithmetic functions (multiply, divide, etc.).
- Input validation, error handling for non-numeric inputs, or a CLI/HTTP interface.
- Changes to existing tests, CI configuration, or packaging metadata.

## Open questions

- None blocking.

## Possible follow-ups (not requirements)

- Decide on a consistent policy for numeric types (int vs float) across arithmetic helpers.
