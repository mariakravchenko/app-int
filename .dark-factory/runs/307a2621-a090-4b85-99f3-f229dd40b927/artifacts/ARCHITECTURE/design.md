# Design — Add `subtract(a, b)` to `app_int.main`, with a test

Run: `307a2621-a090-4b85-99f3-f229dd40b927`
Inputs: `artifacts/BA/acceptance_criteria.json` (AC-1 … AC-13), `artifacts/BA/requirements.md`

## 1. Summary

Add one pure function, `subtract`, to the existing module
`src/app_int/main.py`, next to `add` and in the same style. Cover it with
pytest tests under `tests/`. Nothing else changes: no new modules, no new
dependencies, no config changes.

This is the smallest change that meets every acceptance criterion. A larger
refactor (e.g. a separate `arithmetic` module, or a generic `operate()`
helper) was considered and rejected — the task doesn't ask for it, and it
would risk AC-10 (existing behaviour unchanged).

## 2. Current state (baseline on `main`)

- `src/app_int/main.py` — module docstring, `from __future__ import annotations`,
  `health_check() -> dict[str, str]`, `add(a: int, b: int) -> int` with a
  one-line docstring.
- `src/app_int/__init__.py` — package marker. It does **not** re-export
  `add`, and it must not be changed to re-export `subtract` either (see C-5).
- `tests/test_main.py` — imports `add, health_check` from `app_int.main` and has
  `test_health_check_reports_ok` and `test_add_returns_the_sum`.
- `pyproject.toml` — `dependencies = []`; ruff runs with `line-length = 100` and
  rule sets `E, F, I, UP, B`. The package is built from `src/app_int`
  (hatchling), so it imports as `app_int`.

Path note (BA assumption A-1): the task says `app_int/main.py`. That means the
existing `src/app_int/main.py`. Do not create a top-level `app_int/` directory.

## 3. Who does what

The pipeline only lets each role write to certain paths, so the work is split:

| Role        | Write scope | Responsibility in this run |
|-------------|-------------|----------------------------|
| Developer   | `src/**`    | Add `subtract` to `src/app_int/main.py` (§4). Must **not** touch `tests/`. |
| QA          | `tests/**`  | Add the `subtract` tests (§5). Keep the existing tests unchanged. |

The task says "with a test". The test is still a required deliverable of the
run (AC-8, AC-9), but QA writes it, not the Developer. A Developer edit under
`tests/` breaks its write scope and gets reverted.

## 4. Production change — `src/app_int/main.py` (Developer)

### Interface

A new module-level public function:

- **Name:** `subtract`
- **Parameters:** exactly two, `a` then `b`, both plain positional-or-keyword
  parameters (the same kind as `add`'s). No defaults, no `*args`/`**kwargs`,
  no keyword-only or positional-only markers. (AC-2)
- **Annotations:** `a: int`, `b: int`, return `int`. The module already has
  `from __future__ import annotations`, so `subtract.__annotations__` will
  hold the string `'int'` for each. AC-7 explicitly accepts this. (AC-7)
- **Docstring:** a non-empty one-line docstring in the same voice as `add`'s
  (`"Return the sum of two integers."`), saying the function returns `a`
  minus `b`. Naming the order makes the argument order clear. (AC-6)
- **Behaviour:** return `a - b` using Python's native integer subtraction. (AC-3, AC-4, AC-5)
  - No input validation, type checks, coercion, or error handling (BA A-2, A-3).
  - No side effects, logging, or I/O.

### Placement

Put it directly after `add`, separated by two blank lines (PEP 8 / ruff `E`).
Do not edit `health_check`, `add`, the module docstring, or the `__future__`
import. (AC-10)

### Expected results this must produce (for self-checking)

| Call                 | Result |
|----------------------|--------|
| `subtract(5, 3)`     | `2`    |
| `subtract(3, 5)`     | `-2`   |
| `subtract(0, 0)`     | `0`    |
| `subtract(-2, -3)`   | `1`    |
| `subtract(7, 0)`     | `7`    |

## 5. Test change — `tests/` (QA)

- Preferred location: the existing `tests/test_main.py`. Add `subtract` to the
  existing `from app_int.main import ...` line, keeping the names in the
  alphabetical order ruff's `I` (isort) rule expects: `add, health_check, subtract`.
  A new file such as `tests/test_subtract.py` is also acceptable (BA A-4), but
  either way the existing two tests must stay as they are, with the same names
  (AC-10).
- At least one test function must call `subtract` and assert on the returned
  value (AC-8).
- At least one assertion must have a **negative** expected result, e.g.
  `subtract(3, 5) == -2`. This checks the argument order is `a - b`, not `b - a` (AC-9).
- Recommended coverage: all five cases in the §4 table. These can be
  separate test functions or one `pytest.mark.parametrize` test. Either way it
  stays within the existing `pytest` dev dependency.
- Test functions should use the existing style: `test_<behaviour>` names and
  a `-> None` return annotation.
- Signature, docstring, and annotation checks (AC-2, AC-6, AC-7) can be done
  with `inspect.signature` / `__doc__` / `__annotations__` in tests if QA wants
  them automated. That is optional for the design. If added, the annotation
  assertion must accept both `'int'` and `int` (see §4).

## 6. Data flow

There is no new data flow. A caller imports `subtract` from `app_int.main`
and passes two ints, and the function returns one int. No state, I/O, or
cross-module interaction.

## 7. Sequencing

1. **Developer:** add `subtract` to `src/app_int/main.py` as described in §4.
   Optionally run `uv run ruff check .` and `uv run pytest -q` locally. The
   existing tests must still pass. The new tests don't exist yet at this stage,
   which is expected.
2. **QA:** add the `subtract` tests under `tests/` as described in §5. Run
   `uv run pytest -q` and `uv run ruff check .`.
3. **Quality gate:** `uv run pytest -q` and `uv run ruff check .` both exit 0
   (AC-11, AC-12).

## 8. Acceptance-criteria traceability

| AC    | Satisfied by |
|-------|--------------|
| AC-1  | §4 — public module-level `subtract` in `app_int.main` |
| AC-2  | §4 Interface — exactly `(a, b)`, in that order, no extras |
| AC-3  | §4 Behaviour — `a - b` → `subtract(5, 3) == 2` |
| AC-4  | §4 Behaviour — `subtract(3, 5) == -2` |
| AC-5  | §4 Behaviour — native int subtraction handles zero/negative operands |
| AC-6  | §4 Interface — non-empty docstring |
| AC-7  | §4 Interface — `int` annotations (string form via `__future__`, accepted) |
| AC-8  | §5 — QA test calling `subtract` and asserting the result |
| AC-9  | §5 — QA test with a negative expected result |
| AC-10 | §4 Placement + §5 — existing functions and tests untouched |
| AC-11 | §7 step 3 — pytest passes |
| AC-12 | §4 Placement / §5 import order — ruff clean |
| AC-13 | C-3 — no `pyproject.toml` changes |

## 9. Tradeoffs and decisions

- **Same module, not a new one.** The task names `main.py`, and putting
  `subtract` beside `add` keeps the module's style consistent. A separate
  module would be unnecessary structure for one function.
- **`int` annotations even though the function would work on floats.**
  This matches `add` and AC-7. There is no runtime enforcement, so
  `subtract(1.5, 0.5)` still works, but it is unsupported and untested (BA A-2).
- **No re-export from `app_int/__init__.py`.** `add` isn't re-exported
  either, and AC-1 only needs `from app_int.main import subtract`.
- **Tests owned by QA.** This follows from the pipeline's write scopes rather
  than being a design preference. See §3.

## 10. Open questions

None. The BA's assumptions A-1 to A-4 settle every ambiguity, and this design
adopts them as written.
