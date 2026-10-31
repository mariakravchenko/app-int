# Requirements: `round_currency` helper

Source: mariakravchenko/app-int#8, "Add a round_currency helper (retest)"

## Goal

Add a helper to the application module that rounds a monetary amount to 2
decimal places, using round-half-up as the finance reporting spec requires. The
human requester confirmed this rounding mode.

## Actors and trigger

- **Actor:** application code, or a developer calling the helper directly.
- **Trigger:** a caller passes a monetary amount to `round_currency`.
- **Outcome:** the caller gets the amount rounded to 2 decimal places using
  round-half-up.

## Functional requirements

- **R1.** A public function named `round_currency` exists in the module
  `app_int.main` (file `src/app_int/main.py`).
- **R2.** `round_currency` takes one monetary amount as its argument and
  returns that amount rounded to exactly 2 decimal places.
- **R3.** It uses **round-half-up**: when the digits after the second decimal
  place are exactly halfway (…5), the result rounds **away from zero**. For
  example, `2.345` becomes `2.35` and `2.335` becomes `2.34`.
- **R4.** Negative amounts round symmetrically, also away from zero. For
  example, `-2.345` becomes `-2.35`.
- **R5.** Amounts that are not halfway round to the nearest hundredth. For
  example, `2.344` becomes `2.34`, `2.346` becomes `2.35` and `-2.344` becomes
  `-2.34`.
- **R6.** Halfway is decided by the amount's decimal value as written, not by
  its binary floating-point approximation. A float input such as `2.345`,
  `1.005` or `0.125` counts as exactly halfway and rounds up (`2.35`, `1.01`,
  `0.13`). This holds even though the float's stored binary value is slightly
  below the decimal.
- **R7.** Amounts that already have 2 or fewer decimal places come back
  numerically unchanged. For example, `2.3` becomes `2.30`, `5` becomes `5.00`
  and `0` becomes `0.00`.
- **R8.** `round_currency` accepts at least `int`, `float` and
  `decimal.Decimal` inputs.

## Non-functional requirements

- **R9.** The existing functions `health_check` and `add` keep their current
  behaviour.
- **R10.** The repository quality gate passes: `uv run pytest -q` and
  `uv run ruff check .`.
- **R11.** The function has a docstring that names the rounding mode
  (round-half-up).
- **R12.** No new third-party runtime dependency is added.

## Assumptions (inferred, not stated by the requester)

- **A1.** The issue says `app_int/main.py`. The module actually lives at
  `src/app_int/main.py`, and that is the intended target.
- **A2.** "Monetary amount" means a plain number. It carries no currency code
  and has no minor-unit rules other than 2 decimal places.
- **A3.** R6 means that for float inputs, "as written" is the float's shortest
  decimal representation, which is what Python's `repr`/`str` shows.
- **A4.** The return type is the implementer's choice, as long as it represents
  the rounded value exactly to 2 decimal places. Criteria compare results by
  their decimal value, using `Decimal(str(result))`.
- **A5.** Behaviour for non-numeric, NaN or infinite inputs is not specified.
  The tests do not cover it.

## Out of scope

- Currency symbols, formatting, localisation and string output.
- Currency conversion, or minor-unit precision other than 2 decimal places.
- Changes to `health_check` or `add`.
- Making the rounding mode configurable.

## Follow-ups (not requirements)

- Agree on how invalid inputs (None, strings, NaN, infinity) should be handled.
- Consider whether callers should pass `Decimal` amounts end to end, to avoid
  float imprecision before rounding.
