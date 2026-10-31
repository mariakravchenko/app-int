# Design — Add `multiply(a, b)` to `app_int.main`, with a test

## Summary
Add one pure function, `multiply`, to the existing module `src/app_int/main.py`
(import path `app_int.main`). It should match the existing `add` function exactly in
shape. Add a pytest test to the existing `tests/test_main.py`. No other file
changes. This is the smallest change that satisfies AC-1..AC-11.

## Current state (verified in repo)
- `src/app_int/main.py` — module docstring, `from __future__ import annotations`,
  then `health_check() -> dict[str, str]` and `add(a: int, b: int) -> int`, each
  with a one-line docstring.
- `tests/test_main.py` — `from app_int.main import add, health_check` plus
  `test_health_check_reports_ok` and `test_add_returns_the_sum`.
- `pyproject.toml` — `dependencies = []`; ruff rules `E, F, I, UP, B`,
  line length 100; package built from `src/app_int`.
- The task text says `app_int/main.py`. Per BA assumption A1 this is
  `src/app_int/main.py`. No new top-level `app_int/` directory is created.

## Affected components
| File | Change | Owner (write scope) |
|---|---|---|
| `src/app_int/main.py` | Append new function `multiply` after `add` | DEVELOPMENT (`src/**`) |
| `tests/test_main.py` | Extend import; add test function(s) for `multiply` | QA (`tests/**`) |

**Important sequencing note:** the DEVELOPMENT role's write scope is `src/**` only,
so the Developer must **not** touch `tests/`. QA writes the test required by AC-7
(write scope `tests/**`), and QA runs after DEVELOPMENT. The
Developer may check behaviour locally (e.g. with an ad-hoc `python -c` check)
but must leave no files outside `src/`.

## Interface (new)
`multiply` in module `app_int.main`:
- **Name:** `multiply`. Public and module-level, defined with `def` (not a lambda
  or an alias), so `inspect.signature` reports its parameters cleanly. (AC-1)
- **Parameters:** exactly two, named `a` then `b`, both positional-or-keyword
  (the same kind as in `add`). No defaults, no `*args`/`**kwargs`. (AC-2)
- **Annotations:** `a: int`, `b: int`, return `int`, the same as `add`. (AC-6)
- **Docstring:** one line, in the same style as `add`, e.g. "Return the product of two
  integers." (AC-6)
- **Behaviour:** returns the product `a * b` using Python's built-in
  multiplication operator. No validation, no type coercion, no error handling
  (BA A2/A3). This covers AC-3, AC-4 and AC-5 with no special cases.

**Placement:** directly after `add`, with two blank lines between them (PEP 8 / ruff
E30x). Do not reorder or change `health_check` or `add`. (AC-8)

### Note on annotations and `from __future__ import annotations`
The module keeps `from __future__ import annotations`. Because of that, at runtime
`inspect.signature(multiply).parameters["a"].annotation` is the *string*
`"int"`, not the class `int`. This is already true for `add`. Tests that check AC-6
should use `typing.get_type_hints(multiply)` (which resolves to `int`) or accept
either `int` or `"int"`. The Developer must not remove the future import to
"fix" this: no requirement asks for that change.

## Test design (QA)
In `tests/test_main.py`:
- Extend the existing import to `from app_int.main import add, health_check, multiply`.
  Keep the names sorted so ruff `I` passes.
- Add at least one test, e.g. `test_multiply_returns_the_product`, that asserts
  `multiply(2, 3) == 6`. Also recommended: assertions or tests for zero and
  negatives (`multiply(0, 5) == 0`, `multiply(-2, 3) == -6`,
  `multiply(-2, -3) == 6`), and optionally a signature, annotation and docstring
  check that follows the note above.
- Leave the two existing tests unchanged. (AC-7, AC-8)

## Data flow
Caller → `multiply(a, b)` → `a * b` → returned int. A pure function with no state,
I/O or side effects.

## Sequencing
1. **DEVELOPMENT:** add `multiply` to `src/app_int/main.py`, then run
   `uv run ruff check .` and `uv run pytest -q`. The existing tests must still pass.
2. **QA:** add the `multiply` test(s) to `tests/test_main.py` and run the quality gate.
3. **Quality gate:** `uv run pytest -q` and `uv run ruff check .` both exit 0.
   (AC-9, AC-10)

## AC traceability
| AC | Satisfied by |
|---|---|
| AC-1 | Public `def multiply` in `app_int.main` |
| AC-2 | Parameters are exactly `a`, `b`, with no defaults or varargs |
| AC-3, AC-4, AC-5 | Body returns `a * b` |
| AC-6 | One-line docstring; `int` annotations on `a`, `b`, return |
| AC-7 | QA test in `tests/test_main.py` importing from `app_int.main` |
| AC-8 | `health_check`, `add` and the existing tests are untouched |
| AC-9, AC-10 | Code passes ruff (import sort, blank lines, line length) and tests pass |
| AC-11 | No edits to `pyproject.toml` |

## Tradeoffs / decisions
- **Match `add` rather than generalise** (e.g. `numbers.Number`, `*args`).
  The requirements fix the domain to `int` and two operands. Generalising would add
  surface that no requirement asks for.
- **Put the test in the existing `tests/test_main.py`** rather than a new file.
  This keeps the tests for `app_int.main` together, and BA A4 suggests this file.
- **No input validation.** `add` has none, and `int * int` cannot overflow in
  Python. Behaviour for non-int inputs is unspecified and untested.

## Open questions
None blocking.
