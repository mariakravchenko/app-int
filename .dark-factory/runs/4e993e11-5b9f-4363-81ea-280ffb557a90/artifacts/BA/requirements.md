# Requirements — `round_currency` helper (issue mariakravchenko/app-int#15)

## Goal

Add a public `round_currency` function to the application module
(`src/app_int/main.py`, importable as `app_int.main`) that rounds a monetary
amount to exactly 2 decimal places using **round-half-up** (ties round away
from zero), as the finance team's reporting spec requires.

## Context

- **Actor:** Python code in this repository (and later, finance reporting code)
  calling the helper.
- **Trigger:** a caller passes a monetary amount to `round_currency`.
- **Expected outcome:** the amount, rounded to 2 decimal places by the
  round-half-up rule.
- **Decision record:** the rounding mode was confirmed by the requester
  (human answer: "Use round-half-up — that's what our finance reporting spec
  requires."). This is a compliance requirement, not a style choice.

## Functional requirements

- **R1.** A function named `round_currency` exists in `app_int.main` and is
  importable as `from app_int.main import round_currency`.
- **R2.** `round_currency` takes a single positional argument: the monetary
  amount to round.
- **R3.** The result has exactly 2 decimal places.
- **R4.** When the digit after the second decimal place is a tie (exactly
  half a cent), the amount rounds **away from zero** (round-half-up).
  Examples: `2.345 → 2.35`, `2.335 → 2.34`, `0.005 → 0.01`, `1.125 → 1.13`.
- **R5.** Round-half-up applies symmetrically to negative amounts (ties round
  away from zero): `-2.345 → -2.35`, `-0.005 → -0.01`.
- **R6.** Amounts that are not ties round to the nearest cent:
  `2.344 → 2.34`, `2.346 → 2.35`, `-2.344 → -2.34`.
- **R7.** Amounts that already have 2 or fewer decimal places are returned
  unchanged in value: `10 → 10.00`, `2.5 → 2.50`, `2.34 → 2.34`, `0 → 0.00`.
- **R8.** Rounding is decided on the amount's **decimal value as written**,
  not on its binary floating-point approximation. In particular, a float
  input of `2.345` (whose binary value is slightly below 2.345) must still
  round to `2.35`, and `1.005` must round to `1.01`.
- **R9.** `round_currency` accepts `decimal.Decimal`, `int` and `float`
  amounts.
- **R10.** *(Assumption A2)* The return value is a `decimal.Decimal`, so the
  exact 2-decimal-place result (e.g. `Decimal("2.35")`) is preserved without
  binary floating-point error.
- **R11.** Existing behaviour of `health_check` and `add` is unchanged.

## Non-functional requirements

- **N1.** The function has a docstring that states the rounding mode
  (round-half-up / ties away from zero) explicitly, so the compliance-relevant
  choice is visible to readers.
- **N2.** The function has type annotations, consistent with the rest of the
  module.
- **N3.** No new third-party runtime dependency is introduced.
- **N4.** The quality gate passes: `uv run pytest -q` and `uv run ruff check .`
  both succeed.
- **N5.** Automated tests cover the tie cases (positive and negative), the
  non-tie cases, the already-rounded case, and the float-representation case.

## Assumptions

- **A1.** The issue says "`app_int/main.py`"; the actual file is
  `src/app_int/main.py` (package `app_int`). The function goes there.
- **A2.** Return type is `decimal.Decimal`. The issue doesn't specify one;
  a `float` can't reliably represent 2-decimal results, and for a compliance
  use case an exact decimal is the safer reading. If the requester wants
  `float`, R10 and the `Decimal` comparisons in the acceptance criteria change,
  but the rounding rule (R4–R8) does not.
- **A3.** "Monetary amount" means a plain number. No currency code, no
  currency-specific minor-unit handling (e.g. JPY with 0 decimals); always
  2 decimal places.
- **A4.** Float inputs are interpreted by their shortest decimal string
  representation (what `str()`/`repr()` shows, e.g. `2.345`) to satisfy R8.
- **A5.** Behaviour for invalid inputs (`None`, strings, `bool`, NaN,
  infinity) is not specified by the task and is not required here.

## Out of scope

- Choosing or supporting any rounding mode other than round-half-up
  (no configurable mode parameter).
- Currency formatting (symbols, thousands separators, locale).
- Currency conversion or multi-currency support.
- Wiring the helper into any reporting, CLI or API surface.
- Validation or error handling for non-numeric / non-finite inputs (see A5).

## Follow-ups (not requirements)

- Decide explicit behaviour for invalid inputs (`None`, strings, NaN,
  infinity, `bool`) if the helper will receive untrusted data.
- Confirm with finance whether any currencies with a non-2-decimal minor unit
  need support.
