import time

import pytest

from upr_ai.utils.logger import Logger


@pytest.fixture
def log():
    name = "Tests"
    request_id = 123
    user_id = "User5"

    return Logger(request_id, user_id, name)


@pytest.fixture
def msg():
    return "none"


def test_logging_levels(log, msg) -> bool:
    log.info(msg)
    try:
        1 / 0
    except ZeroDivisionError as exc:
        log.error("An error occurred", exc=exc)
    log.warning("Credential logging")
    try:
        raise ValueError("This is a critical error")
    except ValueError as exc:
        log.critical("Critical error occurred", exc=exc)


def test_timing(log, msg) -> bool:
    @log.time_operation("db query")
    def demo_db():
        time.sleep(0.2)

    demo_db()

    log.info(msg)
