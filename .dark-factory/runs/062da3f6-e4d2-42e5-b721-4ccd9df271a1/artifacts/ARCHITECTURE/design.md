# Design: add `subtract(a, b)` to `app_int.main`, with tests

## Summary

Add one pure function, `subtract`, to `src/app_int/main.py`, modelled on the
existing `add` function, and add unit tests for it under `tests/`. No other
files change. There are no new modules, dependencies, configuration, or I/O.

## Current state

- `src/app_int/main.py` starts with a module docstring and
  `from __future__ import annotations`, then defines `health_check()` and
  `add(a: int, b: int) -> int`. Each function has a one-line docstring.
- `tests/test_main.py` imports `add` and `health_check` and has one test for each.
- Ruff (`line-length = 100`; rules `E, F, I, UP, B`) and pytest make up the
  quality gate.

## Who changes what (pipeline write scopes)

The pipeline gives each role a fixed set of paths it may write:

| Role        | Write scope | Responsibility in this change                  |
|-------------|-------------|------------------------------------------------|
| DEVELOPMENT | `src/**`    | Add `subtract` to `src/app_int/main.py`        |
| QA          | `tests/**`  | Add the `subtract` tests to `tests/test_main.py` |

The task says "with a test", but the Developer **must not** write under
`tests/`. If it does, the change is reverted and the attempt fails. The tests
in AC-8/AC-9 belong to QA. Section 2 below spells them out so QA has an
exact target. The Developer may still run the quality gate locally to check
its work.

## 1. Production change — `src/app_int/main.py` (DEVELOPMENT)

Add a new top-level function right after `add`:

- **Name:** `subtract` (AC-1)
- **Parameters:** exactly two, `a` then `b`. Both are plain
  positional-or-keyword parameters with no defaults: no `*`, no `/`, no
  `*args`/`**kwargs` (AC-2).
- **Annotations:** `a: int`, `b: int`, return `-> int`. Keep the existing
  `from __future__ import annotations`. Under it, the annotations are stored
  as the string `'int'`, which AC-5 explicitly accepts (AC-5).
- **Docstring:** a one-line docstring in the same style as `add`, for
  example "Return the difference of two integers (a minus b)." (AC-6)
- **Behaviour:** return `a - b`, with no validation, coercion, or side
  effects. The operand order must be exactly `a - b`, not `b - a` (AC-3, AC-4).

  Check against the required values: 5-3=2, 10-4=6, 2-5=-3, 0-0=0, 7-0=7,
  (-4)-(-6)=2, (-3)-2=-5.

Do not modify `health_check` or `add`, and do not reorder or remove the
existing imports (AC-7). You may update the module docstring, but it is not
required.

Do not add input type checks such as `isinstance` or raising `TypeError`. The
criteria don't require them, and `add` has none, so leaving them out keeps the
two functions consistent.

## 2. Test change — `tests/test_main.py` (QA)

- Extend the existing import to
  `from app_int.main import add, health_check, subtract`. Keep the names
  sorted alphabetically to satisfy Ruff's `I` (isort) rule.
- Keep both existing tests unchanged (AC-7).
- Add test functions that import `subtract` and assert on its return value (AC-8). At minimum, cover:
  - a positive result, such as `subtract(5, 3) == 2` and `subtract(10, 4) == 6`
  - a negative result, such as `subtract(2, 5) == -3`. Together with the
    positive case, this makes a `b - a` implementation fail (AC-9).
  - the AC-4 edge cases: `subtract(0, 0) == 0`, `subtract(7, 0) == 7`,
    `subtract(-4, -6) == 2`, `subtract(-3, 2) == -5`
- Optional: add `inspect`-based tests for AC-2 (signature), AC-5
  (annotations; accept `int` or `'int'`), and AC-6 (non-empty `__doc__`).
- Every test function gets a `-> None` return annotation, matching the
  existing style. Keep lines at or under 100 characters.
- Put the tests in the existing `tests/test_main.py` rather than a new file.
  That keeps the change small and matches the one-file-per-module layout.

## 3. Things that must stay unchanged

- `pyproject.toml`: no changes at all. In particular, `[project].dependencies`
  and `[dependency-groups]` stay exactly the same (AC-12). The tests need only
  the standard library and pytest.
- No new files under `src/`. `src/app_int/__init__.py` stays unchanged, and
  `subtract` is not re-exported from the package. AC-1 only requires
  `from app_int.main import subtract`.
- `uv.lock` is gitignored and must not be committed.

## Sequencing

1. DEVELOPMENT adds `subtract` to `src/app_int/main.py`, then runs
   `uv run ruff check .` and `uv run pytest -q`. The existing tests must still
   pass.
2. QA adds the tests from section 2, then runs both gate commands.
3. The quality gate runs `uv run pytest -q` and `uv run ruff check .`. Both
   must exit 0 (AC-10, AC-11).

## Traceability

| AC    | Satisfied by |
|-------|--------------|
| AC-1  | §1 name and location |
| AC-2  | §1 parameters |
| AC-3  | §1 behaviour `a - b` |
| AC-4  | §1 behaviour; verified values |
| AC-5  | §1 annotations under the existing `__future__` import |
| AC-6  | §1 docstring |
| AC-7  | §1 "do not modify"; §2 keep existing tests |
| AC-8  | §2 tests import and assert on `subtract` |
| AC-9  | §2 positive and negative expected results |
| AC-10 | §1 and §2 together; sequencing step 3 |
| AC-11 | §2 sorted import and line length; style matches existing code |
| AC-12 | §3 no `pyproject.toml` changes |

## Tradeoffs and notes

- **Tests split from the code.** The task bundles the function and its test
  into one request. The pipeline's write scopes split them between
  DEVELOPMENT and QA. I followed the write scopes rather than the wording of
  the task, because breaking a scope fails the attempt. Nothing is lost: QA
  runs before the gate and owns `tests/**`.
- **`int`-only annotations.** At runtime, `a - b` works for floats too, but
  AC-5 requires `int` annotations. That matches `add`, so I kept it.
- No open questions need a human decision.
