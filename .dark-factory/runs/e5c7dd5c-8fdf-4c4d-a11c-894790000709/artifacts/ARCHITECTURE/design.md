# Design: `square(n)` in `app_int.main`

Run: e5c7dd5c-8fdf-4c4d-a11c-894790000709

## Summary

Add one pure function, `square`, to `src/app_int/main.py`, and one test covering it
in `tests/test_main.py`. No other files change. This is the smallest change that
meets AC-1 through AC-12.

## Current state

- `src/app_int/main.py` has a module docstring, `from __future__ import annotations`,
  and two functions: `health_check() -> dict[str, str]` and `add(a: int, b: int) -> int`.
  Each has a type-annotated signature and a one-line docstring.
- `tests/test_main.py` imports `add, health_check` from `app_int.main` and has
  `test_health_check_reports_ok` and `test_add_returns_the_sum`.
- `pyproject.toml`: `dependencies = []`. Ruff runs rules `E, F, I, UP, B` with
  line-length 100.

## Who changes what

The pipeline's write scopes split the work:

| Role        | Write scope | Change                                   |
|-------------|-------------|------------------------------------------|
| DEVELOPMENT | `src/**`    | Add `square` to `src/app_int/main.py`    |
| QA          | `tests/**`  | Add the `square` test to `tests/test_main.py` |

The Developer must **not** touch `tests/`. Any edit there breaks its write scope and
the attempt is reverted. The test that the task asks for ("with a test") and that
AC-8 requires is QA's to write.

## Change 1: `src/app_int/main.py` (Developer)

Append a new top-level function **after** `add`, matching the style of the existing
functions:

- **Name:** `square`
- **Parameters:** exactly one positional parameter named `n`, annotated `int`. No
  defaults, `*args`, `**kwargs` or keyword-only parameters (AC-2).
- **Return annotation:** `int` (AC-7).
- **Docstring:** a non-empty one-line docstring in the same style as `add`, e.g.
  "Return the square of an integer." (AC-6).
- **Behaviour:** return `n` multiplied by itself (`n * n`, or `n ** 2`). For any
  `int` input the result is a non-negative `int`, so:
  - positive values: 3 → 9, 1 → 1, 12 → 144 (AC-3)
  - negative values: -3 → 9, -1 → 1 (AC-4)
  - zero: 0 → 0 (AC-5)
- No input validation, no new imports, no I/O, no change to the module docstring or
  to `health_check` and `add` (AC-9).

Keep `from __future__ import annotations`. With it, `square.__annotations__` holds
string values (`{'n': 'int', 'return': 'int'}`). AC-7 checks only that the `'n'` and
`'return'` keys are present, so this still passes.

### Why `int` and not a wider numeric type

Every existing function annotates concrete `int` types, and every acceptance
criterion uses integer inputs and expects an `int` result (AC-3). A float or
`numbers.Number` annotation would add scope that no criterion asks for. The function
still works at runtime if someone passes a float. The annotation just doesn't
promise it.

## Change 2: `tests/test_main.py` (QA)

- Extend the existing import to `from app_int.main import add, health_check, square`.
  Keep the names in alphabetical order so ruff's isort rule (`I`) passes.
- Add at least one test function, for example `test_square_returns_the_square`, that
  asserts:
  - a positive integer: `square(3) == 9`
  - a negative integer: `square(-3) == 9`
  - zero: `square(0) == 0`

  This satisfies AC-8. QA may also assert the other AC-3/AC-4 values, the `int`
  return type, the signature, the docstring and the annotations (AC-2, AC-6, AC-7),
  either in the same test or in separate tests.
- Annotate the new test `-> None` to match the existing tests.
- Do not remove or rename `test_health_check_reports_ok` or
  `test_add_returns_the_sum` (AC-9).

## Sequencing

1. DEVELOPMENT adds `square` to `src/app_int/main.py` and runs `uv run ruff check .`
   and `uv run pytest -q` locally. The existing tests must still pass.
2. QA adds the test(s) in `tests/test_main.py` and runs the same two commands.
3. The quality gate runs `uv run pytest -q` and `uv run ruff check .`. Both must
   exit 0 (AC-10, AC-11).

## Out of scope

- No changes to `pyproject.toml`. `dependencies` stays empty (AC-12) and no
  dev-dependency changes are needed.
- No changes to `src/app_int/__init__.py`. AC-1 only needs the import
  `from app_int.main import square`, so there is no package-level re-export.
- No README or other documentation changes.

## Traceability

| AC    | Satisfied by |
|-------|--------------|
| AC-1  | `square` defined at top level in `src/app_int/main.py` |
| AC-2  | single parameter named `n` |
| AC-3  | `n * n` on `int` input returns `int` |
| AC-4  | the square of a negative integer is positive |
| AC-5  | `0 * 0 == 0` |
| AC-6  | non-empty docstring |
| AC-7  | `n: int` and `-> int` annotations |
| AC-8  | QA's test in `tests/test_main.py` (positive, negative, zero) |
| AC-9  | existing functions and tests left untouched |
| AC-10 | the gate runs pytest |
| AC-11 | import sorting and line-length rules followed, gate runs ruff |
| AC-12 | `pyproject.toml` not edited |

## Open questions

None. The requirements are clear enough to build without human input.
