"""A deliberately small application surface for Dark Factory to work against.

Each function here is a plausible unit of real work: something a Developer
role can extend and a QA role can write a test against, without needing a
web framework, a database, or any external service.
"""

from __future__ import annotations


def health_check() -> dict[str, str]:
    """Report that the application is alive."""
    return {"status": "ok"}


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def cube(n: int) -> int:
    """Return ``n`` raised to the third power."""
    return n * n * n
