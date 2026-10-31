# Design — Add `divide(a, b)` to `app_int.main`, with tests

## Summary

Add one new public function, `divide`, to the existing module
`src/app_int/main.py` (import path `app_int.main`), and add tests for it in the
existing `tests/test_main.py`. No other file changes are needed. This is the
smallest change that satisfies AC-1 … AC-16.

## Current state

- `src/app_int/main.py` has `from __future__ import annotations` and two
  annotated, docstringed functions: `health_check() -> dict[str, str]` and
  `add(a: int, b: int) -> int`.
- `tests/test_main.py` imports `add, health_check` from `app_int.main` and has
  one test per function, named `test_<function>_<behaviour>` with `-> None`
  return annotations.
- Ruff selects `E, F, I, UP, B` with line length 100. `I` (isort) enforces
  sorted import names, which matters once `divide` joins the import line.
- `pyproject.toml` `dependencies = []`; pytest is a dev dependency only.

## Affected components

| File | Change | Owner role |
|---|---|---|
| `src/app_int/main.py` | Add `divide` function | Developer (`src/**`) |
| `tests/test_main.py` | Import `divide`, add three tests | QA (`tests/**`) |

The Developer role's write scope is `src/**` only, so the Developer must
**not** edit `tests/`. The tests below are specified so QA can write them. If
the Developer leaves tests out, that is expected and does not mean the work is
incomplete.

## Interface

New function in `app_int.main`, placed after `add`:

- **Name:** `divide`
- **Parameters:** two positional parameters named `a` (dividend) and `b`
  (divisor), in that order (AC-2). No defaults, no keyword-only or extra
  parameters.
- **Annotations:** `a: float`, `b: float`, return `float` (AC-15). Under PEP 484
  numeric promotion, `int` arguments are accepted where `float` is annotated,
  so `divide(6, 3)` type-checks. `from __future__ import annotations` is
  already present; annotations are stored as strings, which still counts as
  non-empty for `inspect.signature`.
- **Behaviour:** returns `a / b` using Python's true-division operator `/`
  (AC-3, AC-4, AC-5, AC-6). Do not use `//`, `divmod`, `round`, or `int(...)`.
- **Zero divisor:** no special handling. Python's `/` already raises
  `ZeroDivisionError` for an `int` or `float` zero divisor (AC-7). Do not catch
  it, wrap it, return `None`/`inf`/`nan`, or raise a custom exception.
- **Docstring:** a one-line docstring in the same style as `add`, describing
  the return value and saying that a zero divisor raises `ZeroDivisionError`
  (AC-8).

### Why `float` rather than `int` annotations

`divide(7, 2)` returns `3.5`, and `/` always returns `float` for int/float
operands, so `-> int` would be wrong. `float` for the parameters matches the
inputs allowed by assumption A4 (ints and/or floats). We are not using a
`Union`/`numbers.Real`/`TypeVar` design: it would add complexity and imports
for no gain in this scope.

## Data flow

Caller → `divide(a, b)` → evaluates `a / b` → either returns the float
quotient, or `ZeroDivisionError` reaches the caller unchanged. No state, no
I/O, no dependencies.

## Test design (for QA)

In `tests/test_main.py`:

1. Extend the existing import to `from app_int.main import add, divide,
   health_check`. Keep names alphabetically sorted to satisfy ruff `I001`.
   Add `import pytest` as its own third-party import block above the
   first-party `app_int` import (ruff/isort ordering: stdlib, third-party,
   first-party, separated by blank lines).
2. Add test functions, following the existing naming and `-> None` style:
   - Exact quotient with a non-zero divisor, e.g. `divide(6, 3) == 2` and/or
     `divide(10, 2) == 5` → AC-10 (also covers AC-2 and AC-3).
   - Non-integer quotient, `divide(7, 2) == 3.5` → AC-11 (AC-4).
   - Zero divisor, `with pytest.raises(ZeroDivisionError): divide(1, 0)` →
     AC-12 (AC-7).
   - Optional but recommended: argument order (`divide(2, 10) == 0.2`),
     negatives (`divide(-6, 3) == -2`, `divide(6, -4) == -1.5`), and zero
     dividend (`divide(0, 5) == 0`) for AC-2, AC-5, AC-6.
     `pytest.mark.parametrize` is fine for these.
3. Leave the existing `add`/`health_check` tests unchanged (AC-9).

Exact equality is safe for every listed value: 0.2, 3.5, -1.5, 2.0, 5.0 and
0.0 are what IEEE-754 true division produces for these operands, so
`pytest.approx` is not needed. QA may still use it for `0.2`.

## Sequencing

1. **Developer:** add `divide` to `src/app_int/main.py` per the interface
   above. Run `uv run ruff check .` and `uv run pytest -q`; the existing tests
   must still pass.
2. **QA:** add the tests above to `tests/test_main.py`, then run both
   quality-gate commands (AC-13, AC-14).

## Acceptance-criteria traceability

| AC | Satisfied by |
|---|---|
| AC-1 | `divide` defined at module level in `app_int.main` |
| AC-2 | Parameters `(a, b)`, body `a / b` |
| AC-3, AC-4, AC-5, AC-6 | True division `/` |
| AC-7 | Native `ZeroDivisionError` from `/`, not caught |
| AC-8 | One-line docstring |
| AC-9 | `add` and `health_check` not modified |
| AC-10, AC-11, AC-12 | QA tests 2a–2c |
| AC-13 | All tests green |
| AC-14 | Sorted imports, line length ≤ 100, no unused imports |
| AC-15 | `a: float, b: float -> float` |
| AC-16 | No `pyproject.toml` edits |

## Tradeoffs and notes

- **Rely on native `ZeroDivisionError` instead of an explicit guard.** This is
  simpler, and the error message is the standard one. An explicit
  `if b == 0: raise ZeroDivisionError(...)` would also be acceptable, but it
  adds code without adding behaviour.
- **Tests go in the existing `tests/test_main.py`** rather than a new file,
  following the one-file-per-module pattern.
- **No clarification needed.** The BA's assumptions A1–A4 settle the only
  ambiguities (division semantics, zero-divisor behaviour, module path).
