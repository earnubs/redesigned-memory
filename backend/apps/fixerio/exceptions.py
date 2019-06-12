"""Exception and error handling utilities for fixerio."""
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError

__all__ = (
    "FixerIOUnrecoverableError",
    "FixerIOValidationError",
    "code_error_mappings",
    "error_response_to_exception",
)


class FixerIOUnrecoverableError(APIException):
    """Error representing an unrecoverable error from API."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"


class FixerIOValidationError(ValidationError):
    """Error representing validation errors from API."""

    pass


# https://fixer.io/documentation#errors
code_error_mappings = {
    404: FixerIOUnrecoverableError("The requested resource does not exist."),
    101: FixerIOUnrecoverableError(
        "No API Key was specified or an invalid API Key was specified."
    ),
    103: FixerIOUnrecoverableError("The requested API endpoint does not exist."),
    104: FixerIOUnrecoverableError(
        "The maximum allowed API amount of monthly API requests has been reached."
    ),
    105: FixerIOUnrecoverableError(
        "The current subscription plan does not support this API endpoint."
    ),
    106: FixerIOUnrecoverableError("The current request did not return any results."),
    102: FixerIOUnrecoverableError(
        "The account this API request is coming from is inactive."
    ),
    201: FixerIOValidationError("An invalid base currency has been entered."),
    202: FixerIOValidationError("One or more invalid symbols have been specified."),
    301: FixerIOValidationError("No date has been specified."),
    302: FixerIOValidationError("An invalid date has been specified."),
    403: FixerIOValidationError("No or an invalid amount has been specified"),
    501: FixerIOValidationError("No or an invalid timeframe has been specified."),
    502: FixerIOValidationError('No or an invalid "start_date" has been specified.'),
    503: FixerIOValidationError('No or an invalid "end_date" has been specified.'),
    504: FixerIOValidationError("An invalid timeframe has been specified."),
    505: FixerIOValidationError(
        "The specified timeframe is too long, exceeding 365 days."
    ),
}


def error_response_to_exception(error_code):
    """Map error_code with an API friendly exception."""
    fallback_exc = FixerIOUnrecoverableError(f"Unknown error '{error_code}'.")
    return code_error_mappings.get(error_code, fallback_exc)
