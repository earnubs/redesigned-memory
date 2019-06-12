from django.test import TestCase

from .. import exceptions


class FixerIOUnrecoverableErrorTest(TestCase):
    """Test the FixerIOUnrecoverableError exception."""

    def test_defaults(self):
        """Test exception configuration."""
        exc = exceptions.FixerIOUnrecoverableError("message")

        self.assertEqual(exc.status_code, 503)
        self.assertEqual(exc.default_code, "service_unavailable")
        self.assertEqual(exc.detail, "message")


class ErrorResponseToExceptionTest(TestCase):
    """Test the ErrorResponseToException utility function."""

    def test_extracts_error_code_from_mappings(self):
        """Test all known error codes."""
        for code, exc in exceptions.code_error_mappings.items():
            self.assertEqual(exceptions.error_response_to_exception(code), exc)

    def test_returns_fallback_if_code_is_unknown(self):
        exc = exceptions.error_response_to_exception(42)

        self.assertIsInstance(exc, exceptions.FixerIOUnrecoverableError)
        self.assertEqual(exc.detail, "Unknown error '42'.")
