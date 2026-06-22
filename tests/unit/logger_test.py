import time

import pytest
import yaml

from upr_ai.utils.config import ConfigManager
from upr_ai.utils.logger import Logger


@pytest.fixture
def log():
    name = "Tests"
    request_id = 123
    user_id = "User5"

    with open("config/default_paths.yaml", encoding="utf-8") as file:
        defaults = yaml.safe_load(file)
    fallback_path = defaults["fall_back_logging_file"]
    logging_path = defaults["logging_file"]
    config = ConfigManager(logging_path).get_config()

    return Logger(request_id, user_id, name, config, fallback_path)


@pytest.fixture
def msg():
    return "none"


def test_logging_levels(log, msg):
    log.info(msg)
    try:
        raise ZeroDivisionError("This is an error")
    except ZeroDivisionError as exc:
        log.error("An error occurred", exc=exc)
    log.warning("Credential logging")
    try:
        raise ValueError("This is a critical error")
    except ValueError as exc:
        log.critical("Critical error occurred", exc=exc)


def test_timing(log, msg):
    @log.time_operation("db query")
    def demo_db():
        time.sleep(0.2)

    demo_db()

    log.info(msg)
