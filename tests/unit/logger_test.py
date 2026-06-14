import time

import pytest

from upr_ai.utils.logger import Logger


@pytest.fixture
def log():
    name = "Tests"
    request_id = "A333"
    user_id = "User223"

    return Logger(request_id, user_id, name)


@pytest.fixture
def msg():
    return "Test message - Fixed critical level showing error level"


def test_logging_levels(log, msg) -> bool:
    log.info(msg)
    log.warning(msg)
    log.error(msg)
    log.critical(msg)


def test_timing(log, msg) -> bool:
    @log.time_operation("db query")
    def demo_db():
        time.sleep(0.2)

    demo_db()

    log.info(msg)
