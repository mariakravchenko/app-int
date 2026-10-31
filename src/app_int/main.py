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


def round_currency(amount: int | float | Decimal) -> Decimal:
    """Round a monetary amount to 2 decimal places using round-half-up (ties away from zero).

    A float is read by its shortest decimal representation (``str(amount)``),
    not its exact binary value, so ``2.345`` rounds to ``Decimal('2.35')``.
    The result is always a ``Decimal`` with exactly 2 digits after the point.
    """
    value = Decimal(str(amount)) if isinstance(amount, float) else Decimal(amount)
    return value.quantize(_CENT, rounding=ROUND_HALF_UP)
