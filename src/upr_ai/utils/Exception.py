import traceback


class UPRException(Exception):
    """
    Base exception for the application.
    """

    def __init__(self, message: str, *, original_exception=None):
        super().__init__(message)

        self.message = message
        self.original_exception = original_exception

        if original_exception:
            tb = traceback.extract_tb(original_exception.__traceback__)
            frame = tb[-1] if tb else None

            self.file = frame.filename if frame else None
            self.line_no = frame.lineno if frame else None
            self.exception_type = type(original_exception).__name__
            self.exception_message = str(original_exception)
        else:
            self.file = None
            self.line_no = None
            self.exception_type = None
            self.exception_message = None

    def to_dict(self):
        return {
            "message": self.message,
            "exception_type": self.exception_type,
            "exception_message": self.exception_message,
            "file": self.file,
            "line_no": self.line_no,
        }

    def __str__(self):
        return str(self.to_dict())
