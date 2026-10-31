# Requirements — Add `multiply(a, b)` with a test

## Goal
Extend the app's public surface with a `multiply(a, b)` function that returns the
product of two integers, covered by an automated test, without breaking anything
that exists today.

## Context
- Actor: a caller of the `app_int.main` module (library consumer / test suite).
- Trigger: calling `multiply(a, b)`.
- Expected outcome: the product of `a` and `b` is returned.
- The task refers to `app_int/main.py`; in this repository that module lives at
  `src/app_int/main.py` and is imported as `app_int.main` (see Assumption A1).

## Functional requirements
- **R1.** The module `app_int.main` exposes a public callable named `multiply`.
- **R2.** `multiply` accepts exactly two positional arguments, `a` and `b`.
- **R3.** `multiply(a, b)` returns the arithmetic product of `a` and `b` for integer
  inputs (e.g. `multiply(2, 3) == 6`).
- **R4.** `multiply` returns correct results for zero and negative integer inputs
  (e.g. `multiply(0, 5) == 0`, `multiply(-2, 3) == -6`, `multiply(-2, -3) == 6`).
- **R5.** `multiply` is documented in the same style as its sibling functions (a
  docstring stating what it returns) and carries type annotations consistent with
  `add(a: int, b: int) -> int` (see Assumption A2).
- **R6.** The test suite under `tests/` contains at least one test that imports
  `multiply` from `app_int.main` and asserts its result.

## Non-functional requirements
- **R7.** Existing behaviour is preserved: `health_check()` and `add()` keep their
  current signatures and results, and all pre-existing tests still pass.
- **R8.** The project quality gate passes: `uv run pytest -q` exits 0 and
  `uv run ruff check .` exits 0.
- **R9.** No new runtime dependencies are introduced (`[project].dependencies`
  stays empty).

## Assumptions
- **A1.** "app_int/main.py" in the task means the existing module
  `src/app_int/main.py` (import path `app_int.main`); no new file at a repo-root
  `app_int/` path is to be created.
- **A2.** Inputs are integers, mirroring `add(a: int, b: int) -> int`. Behaviour for
  floats, strings, or other types is not specified and is not tested.
- **A3.** No input validation or custom error handling is required; overflow is not
  a concern (Python integers are arbitrary precision).
- **A4.** "with a test" means a pytest test placed in the existing `tests/` suite
  (e.g. `tests/test_main.py`).

## Out of scope
- CLI, HTTP, or any other interface to `multiply`.
- Support for non-integer types, vectors/matrices, or more than two operands.
- Refactoring `add`, `health_check`, or the project layout.
- Documentation changes beyond the function's docstring (README, changelog).

## Open questions
- None blocking. The type-domain question is resolved by Assumption A2.

## Follow-ups (not requirements)
- Consider whether other arithmetic helpers (subtract, divide) are wanted.
