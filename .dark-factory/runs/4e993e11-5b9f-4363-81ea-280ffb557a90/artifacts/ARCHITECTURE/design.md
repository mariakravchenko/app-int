# Design: `round_currency`

## Decision

Implement `round_currency` in `src/app_int/main.py`, alongside the existing
small application helpers. The rounding mode is **round-half-up**
(`decimal.ROUND_HALF_UP`), as explicitly required by acceptance criteria AC-3
through AC-5. This resolves the issue body's stated uncertainty for this
delivery; do not substitute banker's rounding.

## Components and interface

- Add a public function in `app_int.main` with one positional parameter and
  annotations equivalent to `amount: Decimal | int | float` and `-> Decimal`.
- Import `Decimal` and `ROUND_HALF_UP` from Python's standard-library
  `decimal` module. Do not add runtime dependencies.
- Document in the function docstring that rounding is half-up.
- Leave `health_check` and `add` unchanged.

## Data flow

Convert the amount to `Decimal` from its decimal string representation before
rounding. This preserves a float's written decimal value rather than its
underlying binary approximation, and also supports `Decimal` and integer
inputs. Quantize the converted value to `Decimal("0.01")` using
`ROUND_HALF_UP`; return that `Decimal` directly. The quantization ensures the
result has exponent `-2`, including for whole amounts and zero. For ties,
`ROUND_HALF_UP` rounds away from zero for both positive and negative amounts.

## Test approach

Extend `tests/test_main.py` with coverage for:

- Importability, callability, and the one-argument interface; include type
  annotation and docstring checks for the declared public contract.
- Decimal result type and exponent `-2` for `Decimal("2.345")`, `10`, and `2.5`.
- Positive ties, including `2.345`, `2.335`, `0.005`, `1.125`, and the
  anti-banker's-rounding cases specified in AC-4.
- Negative ties `-2.345` and `-0.005`.
- Non-ties on either side of a cent boundary, including negative values.
- Already-rounded amounts and zero, retaining the two-decimal exponent.
- Float inputs `2.345`, `1.005`, and `-2.345`, to verify conversion by written
  decimal value.

Keep the existing health-check and addition tests unchanged and passing.
Confirm the runtime dependency list in `pyproject.toml` remains identical to
the base branch. The repository quality gate is `uv run pytest -q` followed by
`uv run ruff check .`.

## Acceptance-criteria traceability

| Criteria | Design coverage |
|---|---|
| AC-1 | Public one-argument `app_int.main.round_currency` interface. |
| AC-2 | Decimal conversion and quantization to `Decimal("0.01")`; tests assert type and exponent. |
| AC-3, AC-4, AC-5 | Explicit `ROUND_HALF_UP`; test positive and negative ties and anti-banker's cases. |
| AC-6 | Nearest-cent quantization tests for positive and negative non-ties. |
| AC-7 | Tests for integer, float, Decimal, and zero values already at cent precision. |
| AC-8 | Decimal-string conversion for floats and tests using the specified floats. |
| AC-9 | Preserve and run existing `health_check` and `add` tests. |
| AC-10 | Annotated parameter and return type; docstring names half-up. |
| AC-11 | Use only the standard library; do not change runtime dependencies. |
| AC-12 | Add the specified coverage and run both quality-gate commands. |

## Tradeoff and scope

String-based Decimal construction is chosen over direct float conversion to
honor the explicit written-decimal behavior. The change remains local to the
helper and its tests; it does not introduce a currency type, configurable
rounding, new dependency, or broader monetary API. The acceptance criteria
provide the rounding-mode decision, so no additional clarification is needed.
