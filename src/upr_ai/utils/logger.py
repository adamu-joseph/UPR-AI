from inspect import trace
import logging
import logging.config
import traceback
import json
import time
from functools import wraps
from datetime import datetime, timezone, timedelta

from upr_ai.utils.config import ConfigManger


class JSONFormatter(logging.Formatter):
    """
    Converts log records into structured JSON format.
    """

    def format(self, record, timestamp=None):
        """Formats a log record as JSON.

        Args:
            log_record (log record): The log record to format.
            timestamp (datetime, optional): The timestamp for the log entry.

        Returns:
            json string: The formatted log entry as a JSON string.
        """

        if timestamp is None:
            timestamp = datetime.now(timezone.utc) + timedelta(
                hours=1
            )  # Convert to UTC+1

        log_record = {
            "timestamp": timestamp.isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
            "user_id": getattr(record, "user_id", None),
            "operation": getattr(record, "operation", None),
            "duration_ms": getattr(record, "duration_ms", None),
        }

        exc_info = getattr(record, "exc_info", None)

        if exc_info and exc_info[0] is not None:
            exc_type, exc_value, exc_tb = exc_info

            tb = traceback.extract_tb(exc_tb)
            last_frame = tb[-1] if tb else None

            log_record["exc_info"] = {
                "type": exc_type.__name__,
                "message": str(exc_value),
                "file": last_frame.filename if last_frame else None,
                "line_no": last_frame.lineno if last_frame else None,
            }
        else:
            log_record["exc_info"] = None

        return json.dumps(log_record)


class Logger:
    """
    Centralized structured logging system.
    """

    def __init__(self, request_id: str, user_id: str, name: str):

        self._initialize_logger()
        self.name = name
        self.user_id = user_id
        self.request_id = request_id
        self.logger = logging.getLogger(self.name)

        self.context = {"request_id": self.request_id, "user_id": self.user_id}

    # -----------------------------
    # Context-aware logging
    # -----------------------------

    def _reset_context(self):
        """Resets the logging context to the initial state."""
        self.context = {"request_id": self.request_id, "user_id": self.user_id}

    @staticmethod
    def _initialize_logger(path="config/logging_config.yaml"):
        """Initializes the logger to be able to log to logs folder

        Args:
            path (str): Path of the logging configuration
        """
        config = ConfigManger(path).get_config()

        logging.config.dictConfig(config)

    def _log(self, level, msg, **kwargs):

        print(level)
        extra = kwargs.get("extra", {})

        if level in (logging.ERROR, logging.CRITICAL):
            if level == logging.ERROR:
                self.logger.exception(msg, extra=extra)
            elif level == logging.CRITICAL:
                self.logger.log(level, msg, extra=extra, exc_info=True)
        else:
            self.logger.log(level, msg, extra=extra)

    def info(self, msg, **context):
        log_context = {**self.context, **context}
        self._log(logging.INFO, msg, extra=log_context)
        self._reset_context()

    def warning(self, msg, **context):
        log_context = {**self.context, **context}
        self._log(logging.WARNING, msg, extra=log_context)
        self._reset_context()

    def error(self, msg, **context):
        log_context = {**self.context, **context}
        self._log(logging.ERROR, msg, extra=log_context)
        self._reset_context()

    def critical(self, msg, **context):
        log_context = {**self.context, **context}
        self._log(logging.CRITICAL, msg, extra=log_context)
        self._reset_context()

    # -----------------------------
    # Performance monitoring
    # -----------------------------
    def time_operation(self, operation_name):
        """
        Decorator for measuring execution time.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()

                duration_ms = round((end - start) * 1000, 2)

                extra = {
                    "operation": operation_name,
                    "duration_ms": duration_ms,
                }

                self.context.update(extra)

                return result

            return wrapper

        return decorator
