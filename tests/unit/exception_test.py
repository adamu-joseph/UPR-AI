from upr_ai.utils.Exception import UPRException


def test_upr_exception():
    try:
        raise ValueError("This is a test error")
    except ValueError as e:
        exception = UPRException("An error occurred", original_exception=e)

    assert exception.message == "An error occurred"
    assert exception.exception_type == "ValueError"
    assert exception.exception_message == "This is a test error"
    assert exception.file is not None
    assert exception.line_no is not None
