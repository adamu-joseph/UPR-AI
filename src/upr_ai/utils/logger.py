import json
import logging
import logging.config
import time
import traceback
from datetime import UTC, datetime, timedelta
from functools import wraps

import yaml

from upr_ai.utils.config import ConfigManager
from upr_ai.utils.Exception import FileError, UnknownError


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
            timestamp = datetime.now(UTC) + timedelta(hours=1)  # Convert to UTC+1

        try:
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

            # Add exceptions to log record
            exc_info = getattr(record, "exc_info", None)

            if exc_info and exc_info[0] is not None:
                exc_type, exc_value, exc_tb = exc_info

                tb = traceback.extract_tb(exc_tb)
                last_frame = tb[-1] if tb else None

                log_record["exc_info"] = {
                    "type": exc_type.__name__,
                    "message": (
                        str(exc_value)["exception_message"]
                        if hasattr(exc_value, "exception_message")
                        else str(exc_value)
                    ),
                    "file": last_frame.filename if last_frame else None,
                    "line_no": last_frame.lineno if last_frame else None,
                }
            else:
                log_record["exc_info"] = None

        except Exception:
            log_record = {
                "timestamp": timestamp.isoformat(),
                "level": "Critical",
                "name": "Incorrect Json Formatter",
                "message": "The JsonFormatter is not functioning",
            }

        return json.dumps(log_record)


class Logger:
    """
    Centralized structured logging system.
    """

    def __init__(self, request_id: str, user_id: str, name: str):

        self.logging_state = True  # True if logging is working else False

        self.name: str | None = name
        self.user_id: str | None = user_id
        self.request_id: str | None = request_id

        self.exception_info: tuple | None = (None, None, None)

        # Convert args to string
        if not isinstance(self.name, str):
            self.name = str(self.name)
        if not isinstance(self.user_id, str):
            self.user_id = str(self.user_id)
        if not isinstance(self.request_id, str):
            self.request_id = str(self.request_id)

        # Fallback
        if not self.name or self.name.lower() == "none":
            self.name = __name__
        if not self.request_id or self.request_id.lower() == "none":
            self.request_id = None
        if not self.user_id or self.user_id.lower() == "none":
            self.user_id = None

        self.context = {"request_id": self.request_id, "user_id": self.user_id}
        self.fixed_context = self.context.copy()  # For getting the original context

        self.logger = self._initialize_logger()

    def _reset_context(self):
        """Resets the logging context to the initial state."""
        self.context = self.fixed_context.copy()

    def _log(self, level, msg, **kwargs):
        """Creates log object
        Args:
            level (log level)
            msg (str): custom message to log
        """

        extra = kwargs.get("extra", {})

        exc = extra.get("exc", None)

        if isinstance(exc, BaseException):
            self.exception_info = (
                type(exc),
                exc,
                exc.__traceback__,
            )

        if self.logging_state is False:
            self.logging_error(level, msg)
            return

        msg = self.edit_message(msg)

        if level in (logging.ERROR, logging.CRITICAL):
            if level == logging.ERROR:
                self.logger.exception(msg, extra=extra)
            elif level == logging.CRITICAL:
                self.logger.log(level, msg, extra=extra, exc_info=True)
        else:
            self.logger.log(level, msg, extra=extra)
        self._reset_context()

    def info(self, msg: str | None):
        """Logs at INFO level

        Args:
            msg (str): log message
        """

        log_context = {**self.context}
        self._log(logging.INFO, msg, extra=log_context)

    def warning(self, msg, exc=None):
        """Logs at WARNING level

        Args:
            msg (str): log message

            exc_info (BaseException):
                Pass python base exception to get the exception to log file
        """

        log_context = {**self.context}
        log_context["exc"] = exc

        self._log(logging.WARNING, msg, extra=log_context)

    def error(self, msg, exc=None):
        """Logs at ERROR level

        Args:
            msg (str): log message

            exc_info (BaseException): 
                Pass python base exception to get the exception to log file
        """
        log_context = {**self.context}
        log_context["exc"] = exc

        self._log(logging.ERROR, msg, extra=log_context)

    def critical(self, msg, exc=None):
        """Logs at CRITICAL level

        Args:
            msg (str): log message

            exc_info (BaseException): 
                Pass python base exception to get the exception to log file
        """

        log_context = {**self.context}
        log_context["exc"] = exc

        self._log(logging.CRITICAL, msg, extra=log_context)

    # -----------------------------
    # Performance monitoring
    # -----------------------------
    def time_operation(self, operation_name):
        """
        Decorator for measuring execution time.
        """

        operation_name = self.edit_message(operation_name)

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

    def _initialize_logger(self):
        """Initializes the logger to be able to log to logs folder"""
        my_logger = logging.getLogger(self.name)

        try:
            default_paths = "config/default_paths.yaml"
            with open(default_paths, encoding="utf-8") as file:

                logging_config_path = yaml.safe_load(file)["logging"]

        except FileNotFoundError as exc:
            self.logging_state = False
            self.error("Logging configuration file not found", exc=exc)
            return

        except TypeError as exc:
            self.logging_state = False
            self.error("Logging configuration is invalid", exc=exc)
            return

        except Exception as exc:
            self.logging_state = False
            self.error(
                "An unexpected error occurred while initializing logging", exc=exc
            )
            return

        try:
            config = ConfigManager(logging_config_path).get_config()

        except FileError as exc:
            self.logging_state = False
            self.error(
                "An unexpected error occurred while initializing logging", exc=exc
            )

        except UnknownError as exc:
            self.logging_state = False
            self.error(
                "An unexpected error occurred while initializing logging", exc=exc
            )
            return

        except Exception as exc:
            self.logging_state = False
            self.error(
                "An unexpected error occurred while initializing logging", exc=exc
            )
            return

        try:
            logging.config.dictConfig(config)

        except Exception as exc:
            self.logging_state = False
            self.error(
                "An unexpected error occurred while initializing logging", exc=exc
            )
            return

        return my_logger

    def edit_message(self, msg):
        """Validate msg input and edit message to be string only

        Args:
            msg (_type_): _description_
        """
        if not msg:
            msg = None

        if not isinstance(msg, str):
            msg = str(msg)

        if msg.lower() == "none":
            msg = None

        return msg

    def logging_error(self, level, msg):
        """
        Fallback logger used when the main logging system fails.
        Writes logs in JSON format using JSONFormatter.
        """

        if self.logging_state is not False:
            self.warning("False logging error raised")
            return

        fallback_logger = logging.getLogger(self.name)
        fallback_logger.setLevel(logging.INFO)
        log_file = "artifacts/logs/fallback_logs.json"

        # Prevent duplicate handlers if called multiple times
        try:
            if not fallback_logger.handlers:
                handler = logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=10485760, backupCount=5, encoding="utf-8"
                )

                handler.setFormatter(JSONFormatter())

                fallback_logger.addHandler(handler)

            fallback_logger.log(
                level,
                msg,
                extra=self.context,
                exc_info=self.exception_info,
            )
        except Exception as e:
            print("Error occured while initializing fallback logger", e)
