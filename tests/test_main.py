from app_int.main import add, health_check


def test_health_check_reports_ok() -> None:
    assert health_check() == {"status": "ok"}


def test_add_returns_the_sum() -> None:
    assert add(2, 3) == 5
