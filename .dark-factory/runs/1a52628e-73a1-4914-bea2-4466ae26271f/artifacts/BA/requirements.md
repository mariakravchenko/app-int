# Requirements — `round_currency` helper (issue #14)

## Goal

Add a `round_currency` function to the application module that rounds a
monetary amount to 2 decimal places using **round-half-up** (0.5 rounds away
from zero), as the finance team's reporting spec requires for compliance.

## Context

- **Actor:** code inside the app that needs a money amount ready for finance
  reporting.
- **Trigger:** a call to `round_currency(amount)`.
- **Expected outcome:** the amount, rounded to exactly 2 decimal places using
  round-half-up.
- **Decision record:** the requester confirmed the rounding mode:
  "Use round-half-up — that's what our finance reporting spec requires."
  Round-half-to-even (banker's rounding) is explicitly **not** acceptable.

## Functional requirements

- **R1.** A public function named `round_currency` is added to
  `src/app_int/main.py` and can be imported as
  `from app_int.main import round_currency`.
- **R2.** `round_currency` takes one monetary amount and returns that amount
  rounded to 2 decimal places.
- **R3.** Amounts whose value lies exactly halfway between two 2-decimal
  values are rounded **away from zero** (round-half-up), e.g. `2.345 → 2.35`,
  `2.335 → 2.34`, `0.005 → 0.01`, `1.005 → 1.01`.
- **R4.** Negative amounts are rounded symmetrically to positive amounts
  (half away from zero), e.g. `-2.345 → -2.35`, `-0.005 → -0.01`.
- **R5.** Amounts not exactly on a half are rounded to the nearest 2-decimal
  value, e.g. `2.344 → 2.34`, `2.346 → 2.35`, `-2.344 → -2.34`.
- **R6.** Amounts that already have 2 or fewer decimal places are returned
  numerically unchanged, e.g. `10 → 10.00`, `2.5 → 2.50`, `0 → 0.00`.
- **R7.** The function's docstring states that it rounds to 2 decimal places
  using round-half-up (half away from zero).

## Non-functional requirements

- **R8.** The existing functions `health_check` and `add` keep their current
  behaviour; existing tests continue to pass.
- **R9.** The quality gate passes: `uv run pytest -q` and
  `uv run ruff check .` both succeed.
- **R10.** No new third-party runtime dependencies are added.

## Assumptions (inferred, not stated)

- **A1.** "Exactly halfway" is judged on the amount as the caller writes it in
  decimal (e.g. the literal `2.345`), not on the nearest binary floating-point
  approximation (which for `2.345` is slightly below the half). Without this,
  the requester's own example could not round to `2.35` reliably.
- **A2.** Results are compared by numeric value; the return type (e.g. `float`
  vs `Decimal`) is an Architect decision as long as R2–R6 hold for the
  examples given.
- **A3.** Handling of invalid input (non-numeric values, NaN, infinity) is not
  specified by the requester and is left to the Architect; it is not covered
  by acceptance criteria.

## Out of scope

- Currency symbols, thousands separators, string formatting or localisation.
- Currency conversion, or currencies with other than 2 minor-unit digits.
- Configurable rounding modes (only round-half-up is required).
- Changing any other existing function.

## Follow-ups (not requirements)

- Consider whether callers should pass amounts as `Decimal`/strings to avoid
  float representation issues across the codebase.
