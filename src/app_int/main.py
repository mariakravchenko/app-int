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


def round_currency(amount: Decimal | int | float) -> Decimal:
    """Round a monetary amount to exactly 2 decimal places using half-up rounding.

    Ties (exactly half a cent) round away from zero (``ROUND_HALF_UP``), for
    both positive and negative amounts: ``2.345 -> 2.35``,
    ``-2.345 -> -2.35``. This is the finance reporting spec's required mode;
    it is not banker's rounding.

    Floats are converted via their written decimal value (``str(amount)``),
    not their binary approximation, so ``1.005`` rounds to ``1.01``.
    """
    return Decimal(str(amount)).quantize(_CENT, rounding=ROUND_HALF_UP)
