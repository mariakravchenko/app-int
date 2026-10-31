# Design — Add `subtract(a, b)` to `app_int.main`, with a test

## Summary

Add one pure function, `subtract`, to the existing module
`src/app_int/main.py`, alongside and modelled on the existing `add`. Add test
coverage for it under `tests/`. Nothing else changes.

The task text says `app_int/main.py`; in this repository that module lives at
`src/app_int/main.py` (importable as `app_int.main`, packaged via hatch from
`src/app_int`). That is the only production file touched.

## Affected components

| Component | Change | Owner (write scope) |
|---|---|---|
| `src/app_int/main.py` | Add a new top-level function `subtract` after `add`. | Developer (`src/**`) |
| `tests/test_main.py` | Add test(s) for `subtract`; extend the existing import line. | QA (`tests/**`) |
| `pyproject.toml`, `src/app_int/__init__.py`, `README.md` | **No change.** | — |

Note on role split: the Developer role's write scope is `src/**` only, and the
QA role's is `tests/**` only. So the Developer implements the function and
does **not** write test files; the test required by AC-7 is QA's deliverable.
The Developer should still run the quality gate locally to confirm nothing
breaks (and may verify behaviour ad hoc in a shell, without committing test
files).

## Interface

New public function in `app_int.main`:

- Name: `subtract`
- Parameters: exactly two, in order — `a` annotated `int`, `b` annotated `int`.
  Plain positional-or-keyword parameters (no defaults, no `*args`/`**kwargs`,
  no positional-only `/` or keyword-only `*` markers), matching `add`.
- Return annotation: `int`.
- Semantics: returns `a - b` (first argument minus second).
- Docstring: a single-line, non-empty docstring in the same style as `add`'s
  (e.g. describing that it returns the difference of two integers, `a` minus
  `b`).
- Pure: no I/O, no validation, no side effects, no new imports.

Placement: immediately after `add`, separated by the standard two blank lines,
so the module reads health_check → add → subtract. The module already has
`from __future__ import annotations`; no import changes are required.

## Data flow

Caller → `subtract(a, b)` → returns `a - b`. No state, no dependencies.
Python ints are arbitrary precision, so no overflow handling is needed.

## Test design (for QA)

In `tests/test_main.py` (the existing file — keeps all tests for `app_int.main`
together; a new file would also satisfy AC-7 but is unnecessary):

- Extend the existing import to also import `subtract`. Keep the imported
  names in ruff/isort order (`add, health_check, subtract`) so `ruff check`
  rule `I` passes.
- Add at least one test function (e.g. `test_subtract_returns_the_difference`)
  asserting `subtract(5, 3) == 2`, mirroring the existing `add` test style
  (typed `-> None`, plain `assert`).
- Recommended additional tests covering AC-3/AC-4: `subtract(3, 5) == -2`
  (order matters), `subtract(0, 0) == 0`, `subtract(7, 0) == 7`,
  `subtract(0, 7) == -7`, `subtract(-4, -6) == 2`, `subtract(-4, 6) == -10`.
  `pytest.mark.parametrize` is acceptable; pytest is already a dev dependency.
- Optional structural checks for AC-2/AC-5/AC-6 via `inspect.signature`,
  `typing.get_type_hints` (note: because of `from __future__ import
  annotations`, raw `__annotations__` values are strings like `'int'`;
  `get_type_hints` resolves them to `int`), and `subtract.__doc__`.
- Do not modify or remove `test_health_check_reports_ok` or
  `test_add_returns_the_sum`.

## Sequencing

1. Developer: add `subtract` to `src/app_int/main.py`; run
   `uv run ruff check .` and `uv run pytest -q` — both must exit 0.
2. QA: add tests for `subtract` to `tests/test_main.py`; run the same gate.

## Acceptance-criteria traceability

| AC | Satisfied by |
|---|---|
| AC-1 | Public top-level `subtract` in `app_int.main`. |
| AC-2 | Exactly two plain params `a`, `b` in that order; positional call works. |
| AC-3 | Body returns `a - b` (not `b - a`). |
| AC-4 | Native int subtraction handles zero/negative cases; no special-casing. |
| AC-5 | Annotations `a: int`, `b: int`, `-> int`. |
| AC-6 | Non-empty docstring. |
| AC-7 | QA test(s) in `tests/test_main.py` calling `subtract` and asserting results. |
| AC-8 | `health_check`, `add`, and their tests left untouched. |
| AC-9 | Code mirrors existing style; line length ≤ 100; imports sorted. Gate run by both roles. |
| AC-10 | No dependency or `pyproject.toml` change. |

## Tradeoffs / decisions

- **No input validation** (BA assumption A1): raising on non-ints would add
  behaviour not requested and diverge from `add`. Type hints document intent.
- **No re-export from `__init__.py`**: out of scope per BA; AC-1 imports from
  `app_int.main` directly.
- **Tests in the existing file** rather than a new one: smallest change,
  keeps per-module test locality.

## Open questions

None. The path discrepancy (`app_int/main.py` vs `src/app_int/main.py`) is
resolved by repository layout, as the BA also noted.
