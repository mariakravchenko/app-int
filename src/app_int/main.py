"""A deliberately small application surface for Dark Factory to work against.

Each function here is a plausible unit of real work: something a Developer
role can extend and a QA role can write a test against, without needing a
web framework, a database, or any external service.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

_CENT = Decimal("0.01")


def health_check() -> dict[str, str]:
    """Report that the application is alive."""
    return {"status": "ok"}


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def round_currency(amount: int | float | Decimal) -> float:
    """Round a monetary amount to 2 decimal places using round-half-up.

    Round-half-up here means exact halves round away from zero, for both
    positive and negative amounts: ``2.345 -> 2.35``, ``-2.345 -> -2.35``.
    Banker's rounding (round-half-to-even) is deliberately not used.

    A ``float`` input is read by its shortest decimal form (``str(amount)``),
    so ``1.005`` counts as an exact half and rounds to ``1.01`` even though
    its binary value is slightly below 1.005.

    Accepts ``int``, ``float`` or ``decimal.Decimal`` and returns a ``float``.
    Raises ``TypeError`` for ``bool`` or any other type, and ``ValueError`` for
    NaN or infinite values.
    """
    if isinstance(amount, bool) or not isinstance(amount, (int, float, Decimal)):
        raise TypeError(f"amount must be int, float or Decimal, not {type(amount).__name__}")
    value = Decimal(str(amount)) if isinstance(amount, float) else Decimal(amount)
    if not value.is_finite():
        raise ValueError(f"amount must be finite, got {amount!r}")
    return float(value.quantize(_CENT, rounding=ROUND_HALF_UP))
