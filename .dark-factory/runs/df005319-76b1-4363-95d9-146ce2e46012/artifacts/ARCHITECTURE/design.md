# Design — `round_currency` helper (issue mariakravchenko/app-int#11)

## Summary

Add one pure function, `round_currency`, to `src/app_int/main.py`. It rounds a
monetary amount to 2 decimal places using **round-half-up (exact halves round
away from zero)**. Internally it uses the standard-library `decimal` module and
**returns a `float`**. No new dependencies, no other modules touched.

### Rounding-mode decision (traceability)

The issue asked the team to check the rounding mode with the requester rather
than guess. The BA's `requirements.md` records that the requester confirmed
**round-half-up (away from zero)** and ruled out banker's rounding. This design
follows that recorded decision and does not reopen it. If that confirmation
turns out to be wrong, the only things to change are the rounding constant, the
docstring, and the expected test values. Nothing else depends on the mode.

## Affected components

| Path | Change |
|---|---|
| `src/app_int/main.py` | Add `round_currency` and a stdlib `decimal` import. `health_check` and `add` stay exactly as they are. |
| `tests/test_round_currency.py` (new) | Tests for `round_currency` (AC-2…AC-8, AC-13). |
| `tests/test_main.py` | **Not modified** (AC-9). |

No changes to `pyproject.toml`, the lockfile, CI, or `.dark-factory/`.

## Interface

```
round_currency(amount: int | float | Decimal) -> float
```

- **Name and location:** `round_currency`, a public, module-level function in
  `app_int.main`, so `from app_int.main import round_currency` works (AC-1).
- **Input:** one amount. Accepted types are `int`, `float` and
  `decimal.Decimal`.
- **Output:** a `float` equal to the amount rounded to 2 decimal places (AC-8:
  a number, not a `str`).
- **Docstring (AC-10):** must say that the function rounds to **2 decimal
  places** using **round-half-up, where exact halves round away from zero**. It
  should also say that a float input is read by its shortest decimal form, so
  `1.005` counts as an exact half, and that invalid input raises an error (see
  below).

## Algorithm / data flow

1. **Validate the type.** Reject `bool` explicitly, because it is a subclass of
   `int`. Also reject anything that is not an `int`, `float` or `Decimal`. Raise
   `TypeError` in both cases.
2. **Convert to `Decimal` using the decimal value the caller wrote** (R7, AC-4):
   - `float` → `Decimal(str(amount))`. Python's `str(float)` gives the shortest
     string that round-trips, so `1.005` becomes `Decimal("1.005")`, not the
     binary value `1.00499999999999989…`. **Do not** use `Decimal(amount)`
     directly on a float. That keeps the binary error and makes `1.005` and
     `2.345` round **down**, which breaks AC-2 and AC-4.
   - `int` → `Decimal(amount)`. This is exact.
   - `Decimal` → use it as is.
3. **Reject non-finite values** (A4). If the `Decimal` is NaN or infinite,
   raise `ValueError` rather than return a number.
4. **Quantize** to `Decimal("0.01")` with `rounding=decimal.ROUND_HALF_UP`. In
   Python's `decimal` module, `ROUND_HALF_UP` rounds ties **away from zero** for
   both signs. That covers R3 and R4 (`-2.345 → -2.35`, `-0.005 → -0.01`).
   - **Do not** use the built-in `round()`. It uses banker's rounding and works
     on the binary value, so `round(2.345, 2)` gives `2.35` only by accident and
     `round(1.005, 2)` gives `1.0`.
   - **Do not** use `ROUND_HALF_EVEN` (the default context rounding mode). Pass
     the rounding mode explicitly in the `quantize` call. Do not rely on, or
     change, the global decimal context.
5. **Convert the result to `float`** and return it.

Worked through by hand (Bash was unavailable to execute it):
`2.345 → "2.345" → 2.35`; `1.005 → "1.005" → 1.01`; `-0.005 → -0.01`;
`2.344 → 2.34`; `5 → 5.00 → 5.0`; `0 → 0.0`.

## Why the function returns `float`, not `Decimal` (tradeoff)

- The acceptance criteria compare against float literals, for example
  `round_currency(2.345) == 2.35`. A `Decimal` compares to a float **by exact
  value**, so `Decimal("2.35") == 2.35` is `False`, because the float 2.35 is
  not exactly 2.35. Returning `Decimal` would make the natural assertions for
  AC-2…AC-7 fail.
- `float(Decimal("2.35"))` is the float closest to 2.35, so it equals the
  literal `2.35`, and `str()` shows `"2.35"`. Integers come back as `5.0` and
  `0.0`, which equal `5.00` and `0.00` and show no more than 2 decimal digits
  (AC-7, AC-8).
- **Cost:** callers that add up many rounded floats can still pick up binary
  error. The BA already listed a wider `Decimal`-for-money policy as a
  follow-up, so that is out of scope here.
- **Edge case:** a small negative amount that rounds to zero, such as `-0.001`,
  returns `-0.0`. This equals `0` numerically and has 1 decimal digit, so it is
  acceptable. The Developer does not need to normalise it.

## Error behaviour (A4 — not in the ACs, chosen to avoid silently wrong output)

- `bool`, `str`, `None` or any other type → `TypeError`.
- NaN or ±infinity, whether given as a float or a `Decimal` → `ValueError`.
- Amounts too large for the default decimal context precision (28 significant
  digits once quantized) will raise `decimal.InvalidOperation` from
  `quantize`. That is acceptable: it is an error, not a wrong number. Do not
  add special handling.

These behaviours may be tested, but they are not required by any acceptance
criterion.

## Tests (AC-13; QA owns the final suite)

Create a new file `tests/test_round_currency.py`. Leave `tests/test_main.py`
untouched so AC-9 holds literally. At minimum, cover:

- Positive exact halves: `2.345 → 2.35`, `2.355 → 2.36`, `0.005 → 0.01`,
  `1.005 → 1.01`
- Negative exact halves: `-2.345 → -2.35`, `-0.005 → -0.01`
- Non-halves: `2.344 → 2.34`, `2.346 → 2.35`, `-2.344 → -2.34`
- Already at 2 or fewer decimal places: `2.34 → 2.34`, `5 → 5.00`, `0 → 0.00`
- For every one of these: `isinstance(result, (int, float))`, not `str`, and
  `str(result)` has no more than 2 digits after the `.` (AC-8)

A parametrized test fits well here. Compare with `==` against float literals,
because the design guarantees an exact match. Do not use `pytest.approx`,
which would hide a `2.34`-vs-`2.35` regression only if the tolerance is set
carelessly.

## Sequencing

1. Add the `decimal` import and `round_currency` (with its docstring) to
   `src/app_int/main.py`, below `add`.
2. Add `tests/test_round_currency.py`.
3. Run `uv run ruff check .`. Import order follows ruff's isort rules (`I`),
   and lines must be 100 characters or fewer. Then run `uv run pytest -q`
   (AC-11, AC-12).

## Acceptance-criteria coverage

| AC | Satisfied by |
|---|---|
| AC-1 | Public module-level function in `app_int.main` |
| AC-2, AC-3, AC-4 | `Decimal(str(float))` + `ROUND_HALF_UP` quantize |
| AC-5 | `ROUND_HALF_UP` rounds away from zero for negatives |
| AC-6 | Ordinary nearest-hundredth quantize |
| AC-7 | int → exact Decimal → float (`5.0`, `0.0`) |
| AC-8 | Returns `float`; quantized value converts to a float whose shortest repr has 2 or fewer decimal places |
| AC-9 | `health_check`, `add` and `tests/test_main.py` unchanged |
| AC-10 | Docstring wording requirement above |
| AC-11, AC-12 | Sequencing step 3 |
| AC-13 | New test file covering the four required categories |

## Open items (no blocker)

- Behaviour for invalid input is a design choice (A4) and can be revisited once
  the finance spec has been checked.
