# Architecture: `cube(n)`

## Goal

Add a typed, documented `cube` function to `src/app_int/main.py` and cover its
behavior with a test under `tests/`, while preserving the existing application
functions and tests.

## Existing structure

- `src/app_int/main.py` contains the small application API, including
  `health_check()` and `add(a, b)`.
- `tests/test_main.py` imports those functions and verifies their behavior.
- The project quality gate is `uv run pytest -q` followed by
  `uv run ruff check .`.

## Technical approach

Add a module-level function in `src/app_int/main.py` with the public interface
`cube(n: int) -> int`. It takes one positional argument, returns `n * n * n`,
and has a non-empty docstring. This direct arithmetic implementation naturally
preserves zero, one, positive, and negative integer behavior; no input
validation or new dependencies are needed.

Extend `tests/test_main.py` to import `cube` from `app_int.main` and assert its
results for the specified positive, zero, unit, and negative inputs. Keep the
existing health-check and addition test functions intact and passing. No other
application interfaces or test infrastructure need to change.

## Data flow and interfaces

The caller supplies an integer to `cube`; the function cubes that value and
returns the integer result. There is no state, I/O, persistence, or change to
the package's public API beyond adding this function.

## Change sequence

1. Add the annotated, documented `cube(n)` function to `src/app_int/main.py`.
2. Import it in `tests/test_main.py` and add assertions covering the required
   inputs.
3. Run `uv run pytest -q` and `uv run ruff check .`.

## Acceptance-criteria coverage

| Criterion | Design coverage |
|---|---|
| AC-1 | Expose `cube` at module scope in `src/app_int/main.py` with exactly one positional parameter. |
| AC-2 | Assert `cube(3) == 27` and `cube(2) == 8`. |
| AC-3 | Assert `cube(0) == 0` and `cube(1) == 1`. |
| AC-4 | Assert `cube(-2) == -8` and `cube(-3) == -27`. |
| AC-5 | Add a test under `tests/` importing `cube` from `app_int.main` and asserting returned values. |
| AC-6 | Preserve `health_check()`, `add(2, 3)`, and both existing tests in `tests/test_main.py`. |
| AC-7 | Run `uv run pytest -q` and require exit status 0 with no failures or errors. |
| AC-8 | Run `uv run ruff check .` and require exit status 0. |
| AC-9 | Annotate the parameter and return value and provide a non-empty function docstring. |

## Tradeoff

Use the direct integer multiplication expression instead of a generic numeric
helper or validation layer. This keeps the implementation minimal and ensures
the specified negative and boundary cases follow ordinary integer arithmetic.

## Clarification

None. The required callable shape and tested input/output values are explicit.
