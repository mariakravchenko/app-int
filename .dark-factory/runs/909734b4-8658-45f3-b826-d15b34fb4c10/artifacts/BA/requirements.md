# Requirements — Add `subtract(a, b)` with a test

## Goal

Extend the application module with a `subtract(a, b)` function that returns the
difference of two integers, and cover it with an automated test.

## Context

- Actor: a caller of the `app_int.main` module (library-style API; no UI, no I/O).
- Trigger: the caller invokes `subtract(a, b)`.
- Expected outcome: the function returns `a - b`.
- The task refers to `app_int/main.py`; in this repository the module lives at
  `src/app_int/main.py` (importable as `app_int.main`). That is the file meant.
- The existing `add(a: int, b: int) -> int` function in the same module is the
  reference for style and contract.

## Functional requirements

- **R1.** The module `app_int.main` exposes a public function named `subtract`.
- **R2.** `subtract` accepts exactly two positional parameters, named `a` and `b`, in that order.
- **R3.** `subtract(a, b)` returns the result of `a` minus `b` (i.e. the first argument minus the second, not the reverse).
- **R4.** `subtract` returns correct results for negative inputs, zero inputs, and results that are negative (e.g. when `b > a`).
- **R5.** `subtract` carries type annotations declaring integer parameters and an integer return value, consistent with the existing `add` function. *(Assumption — inferred from the existing `add` signature; not stated in the task.)*
- **R6.** `subtract` has a docstring describing what it returns, consistent with the other functions in the module. *(Assumption — inferred from module convention.)*
- **R7.** The test suite under `tests/` includes at least one test that calls `subtract` and asserts its result.

## Non-functional requirements

- **R8.** Existing behaviour is unchanged: `health_check()` and `add()` keep their current behaviour, and all pre-existing tests continue to pass.
- **R9.** The quality gate passes: `uv run pytest -q` exits successfully and `uv run ruff check .` reports no violations.
- **R10.** No new runtime dependencies are introduced.

## Assumptions

- A1. "Integer" semantics only; behaviour for non-integer inputs (floats, strings, `None`) is unspecified and not required to be validated or rejected.
- A2. No overflow handling is needed (Python integers are arbitrary precision).
- A3. R5 and R6 follow from existing module conventions rather than explicit instruction.

## Out of scope

- Input validation / custom error handling for non-integer arguments.
- Other arithmetic operations (multiply, divide, etc.).
- Any CLI, HTTP, or UI exposure of `subtract`.
- Changes to `__init__.py` re-exports, README, or packaging metadata.

## Open questions

None blocking.

## Follow-ups (not requirements)

- Consider whether the package should re-export arithmetic helpers from `app_int/__init__.py`.
