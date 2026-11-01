# Requirements — `round_currency` helper (issue mariakravchenko/app-int#11)

## Goal

Add a `round_currency` function to the application module that rounds a
monetary amount to 2 decimal places using round-half-up, as the finance
reporting spec requires.

## Context

- **Actors:** the Developer adds the function and QA tests it. Callers in the
  codebase use it to round amounts for reporting.
- **Trigger:** a caller passes a monetary amount to `round_currency`.
- **Expected outcome:** the caller gets back the amount rounded to exactly 2
  decimal places, with exact halves rounded away from zero.
- **Rounding mode decision:** the requester confirmed (human answer to the
  clarification question) that the finance reporting spec requires
  **round-half-up**, meaning exact halves round away from zero. Banker's
  rounding (round-half-to-even) is explicitly **not** acceptable.

## Functional requirements

- **R1.** The module `src/app_int/main.py` exposes a public function named
  `round_currency`. (The issue says `app_int/main.py`; in this repo that module
  lives at `src/app_int/main.py`.)
- **R2.** `round_currency` accepts one monetary amount as input and returns that
  amount rounded to 2 decimal places.
- **R3.** Exact halves at the third decimal place round **away from zero**
  (round-half-up), e.g. `2.345 → 2.35`, `2.355 → 2.36`, `0.005 → 0.01`,
  `1.005 → 1.01`.
- **R4.** Negative amounts use the same rule mirrored around zero, e.g.
  `-2.345 → -2.35`, `-0.005 → -0.01`.
- **R5.** Values that are not exact halves round to the nearest hundredth, e.g.
  `2.344 → 2.34`, `2.346 → 2.35`, `-2.344 → -2.34`.
- **R6.** Amounts that already have 2 or fewer decimal places come back
  unchanged in value, e.g. `2.34 → 2.34`, `5 → 5.00`, `0 → 0.00`.
- **R7.** The result reflects the decimal value of the amount as the caller
  wrote it. Binary floating-point representation must not change the outcome:
  an amount written as `2.345` or `1.005` is treated as an exact half and
  rounds up (see R3), even though a binary float stores it slightly below that
  value.
- **R8.** The function returns a numeric value, not a formatted string.
  *(Assumption A1.)*

## Non-functional requirements

- **R9.** The existing public functions `health_check` and `add` keep their
  current behaviour. Their existing tests still pass unchanged.
- **R10.** The function has a docstring that states it uses round-half-up
  (halves away from zero) to 2 decimal places, so the compliance-relevant
  choice is visible to future maintainers.
- **R11.** The repository quality gate passes: `uv run pytest -q` and
  `uv run ruff check .` both exit successfully.
- **R12.** The test suite includes tests for `round_currency` that cover at
  least the exact-half cases (positive and negative), the non-half cases, and
  the already-2-decimals case.

## Assumptions

- **A1.** The return value is numeric, not a string, and has no currency
  symbol or thousands separators. The issue says "rounds a monetary amount" and
  does not mention formatting.
- **A2.** Negative amounts (refunds, credits) are valid input and follow the
  mirrored rule in R4. Round-half-up is taken as "away from zero" for
  negatives, matching the definition the requester confirmed.
- **A3.** The caller-facing semantics are decimal: R7 applies whatever numeric
  input type the implementation accepts. The input and return type
  (e.g. `float`, `Decimal`, or both) is left to the Architect, provided R3–R7
  hold.
- **A4.** Handling invalid input (non-numeric values, NaN, infinity) is not
  specified. No particular behaviour is required beyond not returning a wrong
  rounded number silently.

## Out of scope

- Formatting amounts for display (strings, currency symbols, locales).
- Multiple currencies or currencies with other than 2 minor-unit digits.
- Configurable rounding modes or a configurable number of decimal places.
- Changing any existing function in the module.

## Follow-ups (not requirements)

- Decide how invalid input (NaN, infinity, non-numeric) should behave once the
  finance spec has been checked.
- If callers will add up many rounded amounts, consider a wider policy on
  using `Decimal` for monetary values across the codebase.
