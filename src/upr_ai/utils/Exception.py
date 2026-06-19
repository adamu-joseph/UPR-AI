import traceback
from typing import Optional


class UPRException(Exception):
    """
    Base exception for the application.
    """

    def __init__(self, msg: str, original_exception=None):
        if not msg:
            msg = None

        if not isinstance(msg, str):
            msg = str(msg)

        if msg.lower() == "none":
            msg = None

        super().__init__(msg)

        self.message = msg

        self.original_exception = original_exception

        if original_exception:
            try:
                tb = traceback.extract_tb(original_exception.__traceback__)
                frame = tb[-1] if tb else None

                self.file = frame.filename if frame else None
                self.line_no = frame.lineno if frame else None
                self.exception_type: Optional[str] = type(original_exception).__name__
                self.exception_message: Optional[str] = str(original_exception)

            except Exception:
                print(
                    "You passed in a wrong exception. Original exception must be python's exception class"
                )

        else:
            self.file = None
            self.line_no = None
            self.exception_type = None
            self.exception_message = None

    def to_dict(self):
        """Converts custom excption to a dict

        Returns:
            dictionary: dictionary object containing error details
        """
        return {
            "message": self.message,
            "exception_type": self.exception_type,
            "exception_message": self.exception_message,
            "file": self.file,
            "line_no": self.line_no,
        }

    def __str__(self):
        return str(self.to_dict())


class FileError(UPRException):
    """Raised when there is a file error. The file does not exists,
    corrupted or no permission to the file
    """


class UnknownError(UPRException):
    """Raised when there is an unexpected and unknown errror"""
