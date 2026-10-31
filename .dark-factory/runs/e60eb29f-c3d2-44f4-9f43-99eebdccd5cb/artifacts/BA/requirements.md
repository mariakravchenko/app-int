# Requirements — Add a rounding helper (mariakravchenko/app-int#5)

## Goal

Add a public helper to the application's `main` module that rounds a number to
a chosen number of decimal places with predictable, "schoolbook" behaviour.

## Context

- **Actor:** a Python caller of the `app_int` package (other code, tests).
- **Trigger:** the caller invokes the helper with a number and, optionally, a
  number of decimal places.
- **Outcome:** the caller receives the rounded value.
- The issue explicitly delegates the exact behaviour to our judgment. The
  behaviour chosen below is recorded as a set of assumptions (A-*) so it can be
  reviewed; none of it blocks specification.

## Assumptions

- **A-1** The issue's path `app_int/main.py` refers to the existing module
  `src/app_int/main.py` (the repo uses a `src/` layout). No new module is created.
- **A-2** The public name is `round_number`, with signature
  `round_number(value, ndigits=0)`. A fixed name is needed so QA can test it.
- **A-3** Ties (a value exactly halfway between two candidates) round **half
  away from zero** (2.5 → 3, -2.5 → -3), not Python's built-in banker's
  rounding (2.5 → 2). Rationale: this is what most users expect of a
  "rounding helper", and it is the main reason to add one instead of calling
  the built-in `round`.
- **A-4** Rounding is performed on the number's shortest decimal
  representation (what `repr()` shows), so values such as `2.675` round to
  `2.68` rather than `2.67` (the built-in gives `2.67` because of binary
  floating-point error).
- **A-5** `ndigits` may be negative, meaning rounding to tens, hundreds, etc.
  (1250 with `ndigits=-2` → 1300).
- **A-6** Return type: an `int` when `ndigits <= 0`; a `float` when
  `ndigits > 0`.
- **A-7** `bool` is not accepted as a number (even though it is an `int`
  subclass), to avoid silent misuse.

## Functional requirements

- **R-1** `src/app_int/main.py` exposes a public function `round_number`
  importable as `from app_int.main import round_number`.
- **R-2** `round_number` accepts a required positional argument `value`
  (an `int` or `float`) and an optional argument `ndigits` (an `int`) that
  defaults to `0`.
- **R-3** With the default `ndigits`, the result is `value` rounded to the
  nearest whole number.
- **R-4** With a positive `ndigits`, the result is `value` rounded to that many
  digits after the decimal point.
- **R-5** With a negative `ndigits`, the result is `value` rounded to the
  nearest multiple of `10 ** abs(ndigits)` (A-5).
- **R-6** Exact ties round half away from zero for both positive and negative
  values (A-3).
- **R-7** Rounding follows the value's shortest decimal representation, so
  `round_number(2.675, 2) == 2.68` and `round_number(1.005, 2) == 1.01` (A-4).
- **R-8** The result is an `int` when `ndigits <= 0` and a `float` when
  `ndigits > 0` (A-6).
- **R-9** Integer input that needs no rounding at the requested precision is
  returned with the same numeric value (e.g. `round_number(7) == 7`).
- **R-10** A `value` that is not an `int` or `float`, or that is a `bool`,
  raises `TypeError` (A-7).
- **R-11** An `ndigits` that is not an `int`, or that is a `bool`, raises
  `TypeError`.
- **R-12** A `value` that is NaN or ±infinity raises `ValueError`.
- **R-13** The function has no side effects (no I/O, no global state).

## Non-functional requirements

- **N-1** The function has type hints and a docstring describing the tie-breaking
  rule and return type.
- **N-2** No new runtime dependencies are added to `pyproject.toml`
  (standard library only).
- **N-3** Existing functions `health_check` and `add` keep their current
  behaviour; existing tests still pass.
- **N-4** The quality gate passes: `uv run pytest -q` and `uv run ruff check .`.
- **N-5** Automated tests covering the new function are added under `tests/`.

## Out of scope

- Other rounding modes (floor, ceiling, half-even, truncation) or a
  mode-selection parameter.
- `decimal.Decimal`, `fractions.Fraction`, or other numeric types as input.
- Formatting numbers as strings, currency handling, significant-figure rounding.
- Changes to the README or other documentation.

## Open questions (non-blocking)

- **Q-1** Should other numeric types (e.g. `Decimal`) be accepted? Assumed no;
  possible follow-up.
- **Q-2** Is half-away-from-zero the preferred tie rule? Assumed yes (A-3); a
  maintainer can change it on review.
