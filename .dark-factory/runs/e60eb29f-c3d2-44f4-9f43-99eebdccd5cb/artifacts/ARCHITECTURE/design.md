# Design — Add a rounding helper (mariakravchenko/app-int#5)

## Summary

Add one public, pure function `round_number(value, ndigits=0)` to the existing
module `src/app_int/main.py`. It rounds **half away from zero** on the value's
**shortest decimal representation**, using only the standard-library `decimal`
module. Nothing else in the repository changes in the Developer's step. QA then
adds the tests under `tests/`.

## Affected components

| Path | Change | Owner (write scope) |
|---|---|---|
| `src/app_int/main.py` | Add imports and the new function `round_number`. `health_check` and `add` stay exactly as they are. | DEVELOPMENT (`src/**`) |
| `tests/test_round_number.py` (new; suggested name) | Tests for every AC that involves `round_number` (AC-1…AC-14, AC-18). | QA (`tests/**`) |
| `tests/test_main.py` | **Do not change** (AC-16). | — |
| `pyproject.toml` | **Do not change** (AC-15). | — |

There is no new module, no package-level re-export (`src/app_int/__init__.py` is
left alone), and no README change, because the BA marked docs out of scope.

## Interface

```
round_number(value: int | float, ndigits: int = 0) -> int | float
```

- `value` is positional and required. `ndigits` is optional, can be passed
  positionally or by keyword, and defaults to `0`.
- The return type is `int` when `ndigits <= 0` and `float` when `ndigits > 0`
  (AC-8, AC-9).
- The docstring must be non-empty. It must say in words that ties round
  **half away from zero** (use that exact phrase so AC-14 can be checked by
  searching the text). It should also describe the return-type rule, the
  meaning of negative `ndigits`, and the exceptions raised. (N-1)
- `from __future__ import annotations` is already in the module, so the
  `int | float` union syntax is fine. Ruff's `UP` rules prefer it over
  `Union`/`Optional`.

## Algorithm (data flow)

The steps run in this order. Validation order matters only where an input is
invalid in more than one way. The order below is the decision, so tests stay
deterministic.

1. **Validate `value` type → `TypeError`** (AC-10).
   Reject a `bool` first, because `bool` is a subclass of `int`. Then reject
   anything that is not an `int` or `float` (str, None, Decimal, etc.).
2. **Validate `ndigits` type → `TypeError`** (AC-11).
   Reject a `bool` first. Then reject anything that is not an `int`, including
   floats like `1.0` and strings like `"1"`.
3. **Validate finiteness → `ValueError`** (AC-12).
   If `value` is a float and not finite (NaN, +inf, -inf), raise `ValueError`.
   Use `math.isfinite`.
4. **Convert to an exact decimal on the shortest representation** (AC-7).
   - float → `Decimal(repr(value))` (or `str(value)`, which is the same in
     Python 3). **Do not** use `Decimal(value)` directly. That gives the exact
     binary expansion, where `2.675` is `2.67499999…`, and that would fail AC-7.
   - int → `Decimal(value)`. This is exact for ints of any size.
5. **Quantize with `ROUND_HALF_UP`** (AC-2…AC-6).
   - The quantum is `10 ** -ndigits` as a Decimal, i.e. `Decimal(1).scaleb(-ndigits)`.
     That is `Decimal('1')` for 0, `Decimal('0.01')` for 2, and `Decimal('1E+2')`
     for -2.
   - `decimal.ROUND_HALF_UP` is half away from zero for both signs: 2.5→3,
     -2.5→-3, -0.125→-0.13, -1250 at -2 → -1300. (Note: `ROUND_HALF_UP` is
     *not* "toward +∞". Python's decimal module defines it as away from zero.
     Do not use `ROUND_HALF_EVEN`, which is the default, or `ROUND_HALF_DOWN`.)
   - **Precision.** `quantize` raises `decimal.InvalidOperation` when the result
     coefficient needs more digits than the context precision (default 28).
     Large ints (e.g. `10**30`), large floats (e.g. `1e300` at `ndigits=0`) and
     large positive `ndigits` (e.g. `0.1, 50`) can trigger this. Do the quantize
     inside a `decimal.localcontext()` whose `prec` is the larger of 28 and the
     number of result digits, which is about
     `max(adjusted_exponent, 0) + max(ndigits, 0) + a small margin`.
     `localcontext` is thread-local and restored on exit, so R-13 (no global
     state) still holds. **Never** change `decimal.getcontext()` globally.
6. **Convert to the return type** (AC-8, AC-9).
   - `ndigits <= 0` → `int(quantized)`. This is exact. `1.3E+3` becomes `1300`.
   - `ndigits > 0` → `float(quantized)`. `Decimal('3.14')` becomes `3.14`, and
     `Decimal('7.00')` becomes `7.0`.

Worked checks against the ACs (traced by hand; nothing was run):

| Input | Decimal | Quantum | Quantized | Result |
|---|---|---|---|---|
| `3.7` | 3.7 | 1 | 4 | `4` (int) |
| `3.14159, 3` | 3.14159 | 0.001 | 3.142 | `3.142` |
| `1250, -2` | 1250 | 1E+2 | 1.3E+3 | `1300` (int) |
| `-1250, -2` | -1250 | 1E+2 | -1.3E+3 | `-1300` |
| `-0.5` | -0.5 | 1 | -1 | `-1` |
| `0.125, 2` | 0.125 | 0.01 | 0.13 | `0.13` |
| `1.005, 2` | 1.005 | 0.01 | 1.01 | `1.01` |
| `2.675, 2` | 2.675 | 0.01 | 2.68 | `2.68` |
| `7, 2` | 7 | 0.01 | 7.00 | `7.0` (float) |
| `2.4, 1` | 2.4 | 0.1 | 2.4 | `2.4` (float) |

The function does no I/O, does not log or print, and keeps no caches or module
state. Every call is a pure computation (AC-13).

## Sequencing

1. **DEVELOPMENT**: add `import math` and the needed `decimal` names
   (`Decimal`, `ROUND_HALF_UP`, `localcontext`) at the top of
   `src/app_int/main.py`, in an order that passes Ruff's isort rules (`I`). Put
   them after the `__future__` import, stdlib only. Then add `round_number`
   below `add`. Run `uv run ruff check .` and `uv run pytest -q`. Existing
   tests must still pass. The Developer cannot write under `tests/`, so they
   should check AC behaviour with an ad-hoc interpreter call, not a committed
   test.
2. **QA**: add `tests/test_round_number.py` (or a similar name). It should
   import `round_number` from `app_int.main` and cover every AC from AC-1 to
   AC-14, using parametrized cases where that fits. For AC-13, use pytest's
   `capsys` to check that nothing is written to stdout or stderr. For AC-14,
   check `__annotations__` (or `inspect.signature`) for `value`, `ndigits` and
   `return`, and check that `__doc__` contains "half away from zero",
   case-insensitive. Leave `tests/test_main.py` unchanged.

## Tradeoffs and decisions

- **`decimal` vs. arithmetic tricks** (`math.floor(abs(x) * 10**n + 0.5)`):
  the arithmetic approach gets binary-float cases like 2.675 and 1.005 wrong
  (AC-7), and it needs special handling for negative `ndigits`. `decimal`
  handles all of it in one call and is stdlib (N-2).
- **`repr`-based conversion** means the function treats a float as the decimal
  number it displays as. That is what the BA chose (A-4), and it is the
  intuitive "schoolbook" behaviour. The downside is that it differs from
  built-in `round` on such inputs. This is intended.
- **Return `int` for `ndigits <= 0`**: this follows A-6 and the built-in
  `round(x)` convention. With an explicit `ndigits <= 0`, the built-in returns
  a float for float input. We deliberately return `int` in every
  `ndigits <= 0` case (AC-8: `round_number(1250, -2)` is `int`).
- **Overflow edge (not covered by any AC):** a huge int (> ~1.8e308) with
  `ndigits > 0` turns into `float('inf')` when converted to float. This is a
  rare and harmless edge, so no special handling is needed. The Developer may
  leave it as it is. QA should not assert on it.
- **Validation order** (value type → ndigits type → finiteness) is an explicit
  choice. For example, `round_number(float("nan"), "1")` raises `TypeError`.

## Open items for humans (non-blocking)

These were carried over from the BA as non-blocking questions: Q-1 (accept
`Decimal` input?) and Q-2 (is half-away-from-zero preferred?). The design
assumes "no" and "yes" respectively. Either can be changed later without
changing the signature.
