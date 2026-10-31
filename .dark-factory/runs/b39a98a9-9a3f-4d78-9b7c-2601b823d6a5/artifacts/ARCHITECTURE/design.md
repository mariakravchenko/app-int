# Design: `round_currency` helper

Run: b39a98a9-9a3f-4d78-9b7c-2601b823d6a5
Source: mariakravchenko/app-int#8
Inputs: `artifacts/BA/acceptance_criteria.json` (AC-1 … AC-12) and `artifacts/BA/requirements.md`

## 1. Summary

Add one pure function, `round_currency(amount)`, to `src/app_int/main.py`.
It turns the input into a `decimal.Decimal`, then rounds it to 2 decimal
places with `ROUND_HALF_UP`. It returns a `Decimal`. The change uses only the
standard library and touches only that one file in `src/`.

## 2. The rounding mode (traceability note)

The issue asked that the rounding mode be confirmed by a person, not guessed.
The BA's `requirements.md` says: "using round-half-up as the finance reporting
spec requires. The human requester confirmed this rounding mode." AC-3 states
it as a testable rule: `2.345 → 2.35` and `2.335 → 2.34`. Banker's rounding
would give `2.34` for both.

This design relies on that recorded confirmation. It does **not** choose the
mode itself. The rounding mode is a compliance requirement, not something the
Developer may change (see constraint C-3). If a later reviewer finds there was
never a real human answer behind the BA's statement, the run should stop and go
back to the requester. The code would not need to be redesigned: only the
rounding constant changes.

## 3. Affected components

| Path | Change | Owner role |
|---|---|---|
| `src/app_int/main.py` | Add `from decimal import ROUND_HALF_UP, Decimal`. Add the function `round_currency`. | Developer |
| `tests/test_main.py` (or a new `tests/test_round_currency.py`) | Tests for AC-1 … AC-11 | QA (outside the Developer's write scope) |
| `pyproject.toml` | **No change** | — |

`health_check` and `add` are not changed (AC-9).

## 4. Interface

```
round_currency(amount: int | float | Decimal) -> Decimal
```

- **Name and location:** module-level function in `app_int.main`, next to
  `health_check` and `add`. It is importable as
  `from app_int.main import round_currency` (AC-1).
- **Parameter:** one positional amount, `amount`. Type hint:
  `int | float | Decimal`. The file already has
  `from __future__ import annotations`, and ruff's `UP` rules prefer the PEP 604
  union syntax.
- **Return value:** a `Decimal` with exactly 2 digits after the decimal point.
  For example, `Decimal('5.00')` or `Decimal('-2.35')`. It is never a float.
- **Docstring (AC-11):** must contain the literal text `half-up`. For example,
  "Round a monetary amount to 2 decimal places using round-half-up (ties away
  from zero)." The docstring should also say that a float is read by its
  shortest decimal representation (`str(amount)`), not by its exact binary
  value. Keep it short.

## 5. Algorithm (data flow)

1. **Convert the input to Decimal**, based on its type:
   - `Decimal`: use it as is.
   - `float`: `Decimal(str(amount))`. **Never `Decimal(amount)`.**
     `Decimal(2.345)` gives `2.34499999999999997…`, which rounds down to
     `2.34`. That breaks AC-3, AC-4, AC-6 and AC-8. `str()` gives the shortest
     round-trip text (`'2.345'`, `'1.005'`, `'0.125'`, `'2.675'`, `'7.005'`).
     This is exactly what R6 and BA assumption A3 require.
   - `int`: `Decimal(amount)`. This is exact. `Decimal(str(amount))` would also
     work.

   A simple way to write it: one `isinstance(amount, float)` branch that uses
   `str()`, and `Decimal(amount)` for everything else. Passing a `Decimal` to
   `Decimal()` returns an equal value.
2. **Round:** call `.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`. Pass
   `rounding` explicitly. Do not change or depend on the thread-local decimal
   context, which defaults to `ROUND_HALF_EVEN`. A module-level constant for
   `Decimal("0.01")` is fine.
3. **Return** the quantized `Decimal`.

`ROUND_HALF_UP` in Python's `decimal` module rounds ties *away from zero*.
That makes negative values symmetric with positive ones: `-2.345 → -2.35`,
which satisfies R4/AC-4. Do **not** use `ROUND_HALF_CEILING`-style logic or
`math.floor(x*100 + 0.5)`. Those round negative ties toward +∞ and also suffer
from float error.

## 6. How each acceptance criterion is satisfied

| AC | How it is met |
|---|---|
| AC-1 | Public function in `app_int.main` |
| AC-2 | `quantize(Decimal("0.01"))` always gives exponent −2, so `str(result)` has exactly 2 decimal digits |
| AC-3 | `ROUND_HALF_UP`: `2.345→2.35`, `2.335→2.34` |
| AC-4 | Ties go away from zero: `Decimal('-2.345')` and float `-2.345` (→ `'-2.345'`) both give `-2.35` |
| AC-5 | Values that are not ties round to the nearest hundredth: `2.344→2.34`, `2.346→2.35`, `-2.344→-2.34` |
| AC-6 | Converting floats with `str()` keeps the written decimal: `2.345→2.35`, `1.005→1.01`, `0.125→0.13`, `2.675→2.68` |
| AC-7 | Quantize pads with zeros: `2.3→2.30`, `5→5.00`, `0→0.00`, `Decimal('19.99')→19.99` |
| AC-8 | Handles int, float and Decimal: `7→7.00`, `7.005→7.01`, `Decimal('7.005')→7.01` |
| AC-9 | `health_check` and `add` are untouched |
| AC-10 | Only standard library code; imports sorted (ruff `I`); lines ≤ 100 chars; tests added by QA |
| AC-11 | The docstring contains "half-up" |
| AC-12 | Only `decimal` from the standard library; `pyproject.toml` untouched |

## 7. Sequencing

1. Developer: add the `decimal` import below `from __future__ import annotations`
   in the order ruff/isort expects, then add `round_currency` after `add`.
2. Developer: run `uv run ruff check .` and `uv run pytest -q`. The existing
   tests must still pass.
3. QA: add tests covering AC-1 … AC-11, using the exact values from the
   criteria and comparing results to `Decimal` values.

## 8. Tradeoffs and decisions

- **Return `Decimal`, not `float`.** A float cannot hold `2.35` exactly, and
  `5.00` would come back as `5.0`. Returning `Decimal` keeps the result exact,
  which matters for compliance output. It also meets AC-2 and AC-7 without
  extra work. The cost is that callers who expect a float must convert the
  result themselves. BA assumption A4 leaves the return type to the
  implementation, so this is allowed.
- **Convert floats with `str()`, not exact binary conversion.** This is the
  only way to meet R6/AC-6. The tradeoff: for a float whose shortest text form
  is not the value the caller meant (for example, the result of earlier float
  arithmetic like `0.1 + 0.2 = 0.30000000000000004`), the function rounds what
  `str()` shows. That is still correct to 2 decimal places in practice. Callers
  who need strict guarantees should pass `Decimal` (see the BA follow-up).
- **No input validation.** BA assumption A5 leaves `None`, strings, NaN and
  infinity unspecified, so add no special handling. Whatever `Decimal` raises
  (for example, `InvalidOperation` on quantizing NaN or infinity) is
  acceptable. `str` inputs are not part of the interface. They happen to work
  through `Decimal(amount)`, but do not document or test that. `bool` is an
  `int` subclass and is out of scope.
- **Edge cases noted but out of scope:** a tiny negative input such as
  `-0.001` returns `Decimal('-0.00')`. That compares equal to `Decimal('0.00')`
  but prints with a sign. Values beyond the default context precision (28
  significant digits) raise `InvalidOperation` on quantize. Neither case is
  covered by an AC, so do not handle them.
- **Rounding mode is not configurable** (BA out of scope).

## 9. Items for human attention

- The rounding mode (round-half-up) depends on the requester's confirmation,
  as recorded by the BA in `requirements.md`. Section 2 explains how to check
  that and what to do if it turns out to be wrong.
