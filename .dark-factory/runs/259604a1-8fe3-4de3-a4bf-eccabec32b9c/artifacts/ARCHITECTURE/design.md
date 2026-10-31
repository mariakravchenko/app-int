# Design: add `subtract(a, b)` to `app_int.main`

## Summary
Add one pure function, `subtract`, to `src/app_int/main.py`, mirroring the
existing `add` function, plus tests in the existing `tests/test_main.py`.
No other files change.

Note on the task wording: the task says `app_int/main.py`. In this repo the
package lives at `src/app_int/` (src layout, see `pyproject.toml`
`[tool.hatch.build.targets.wheel] packages = ["src/app_int"]`). The function
goes in `src/app_int/main.py`. Do **not** create a top-level `app_int/`
directory (AC-11).

## Affected components
| File | Change | Owner |
|---|---|---|
| `src/app_int/main.py` | Add `subtract` after `add` | Developer |
| `tests/test_main.py` | Extend import; add test function(s) for `subtract` | Developer and/or QA (whichever role the pipeline assigns tests to) |

Not touched: `pyproject.toml`, `uv.lock`, `.dark-factory*`, README, CI files.

## Interface
```
subtract(a: int, b: int) -> int
```
- Module-level function in `app_int.main`, so `from app_int.main import subtract` works (AC-1).
- Exactly two positional-or-keyword parameters, named `a` then `b`, in that
  order. No defaults, no `*args`/`**kwargs`, no keyword-only or
  positional-only markers (AC-2).
- Returns `a - b`: the first argument minus the second, not the reverse
  (AC-3, AC-4: `subtract(3, 5) == -2`, `subtract(0, 7) == -7`).
- Annotations: `int` on `a`, `int` on `b`, return `int` (AC-5). The module
  already has `from __future__ import annotations`. Keep it. Annotations will
  then be the strings `"int"` at runtime, which matches how `add` is written.
  AC-5 checks the annotations in the source.
- One-line docstring in the same style as `add`, e.g. "Return the difference
  of two integers (a minus b)." Must be non-empty (AC-5).
- No input validation and no type coercion. Behaves like `add` (smallest
  change; nothing in the criteria asks for validation).

## Tests (AC-6, AC-7)
In `tests/test_main.py`:
- Change the import to `from app_int.main import add, health_check, subtract`.
  Ruff's isort rule (`I`) needs the names in alphabetical order.
- Add at least one test function whose name starts with `test_` and that
  asserts on `subtract`'s return value. Recommended coverage, which matches the
  acceptance criteria one-for-one:
  - `test_subtract_returns_the_difference`: `subtract(5, 3) == 2`, `subtract(10, 4) == 6`
  - `test_subtract_handles_negative_and_zero`: `subtract(3, 5) == -2`,
    `subtract(7, 0) == 7`, `subtract(0, 7) == -7`, `subtract(0, 0) == 0`
- Add a `-> None` return annotation to each test, like the existing tests.
- Leave `test_health_check_reports_ok` and `test_add_returns_the_sum`
  unchanged (AC-7).

## Sequencing
1. Add `subtract` to `src/app_int/main.py` after `add`, separated by two blank
   lines (PEP 8 / ruff E30x).
2. Update the import and add the tests in `tests/test_main.py`.
3. Run `uv run pytest -q` (AC-8) and `uv run ruff check .` (AC-9). Both must exit 0.
4. Check that `git diff main -- pyproject.toml` is empty (AC-10).

## Acceptance-criteria traceability
| AC | Satisfied by |
|---|---|
| AC-1 | Module-level `subtract` in `app_int.main` |
| AC-2 | Signature `(a, b)` with no extras |
| AC-3, AC-4 | `return a - b` |
| AC-5 | `int` annotations + non-empty docstring |
| AC-6 | New tests in `tests/test_main.py` |
| AC-7 | Existing functions/tests untouched |
| AC-8, AC-9 | Quality gate run before finishing |
| AC-10 | No `pyproject.toml` / lockfile edits |
| AC-11 | Edit only `src/app_int/main.py`; no top-level `app_int/` |

## Tradeoffs
- **Tests go in the existing `tests/test_main.py` rather than a new file.**
  This keeps all tests for `main.py` in one place. A new file would also
  satisfy AC-6.
- **No validation or `float` support.** The criteria specify `int`
  annotations and only integer cases. Adding more would be scope creep.

## Open questions
None. The only ambiguity is the `app_int/` vs `src/app_int/` path, and AC-11
settles it.
