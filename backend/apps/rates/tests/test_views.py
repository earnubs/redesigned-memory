from decimal import Decimal

from django.test import TestCase, override_settings
from requests.exceptions import HTTPError
from rest_framework import exceptions, status
from rest_framework.test import APIClient
import responses

from apps.fixerio import currencies, client
from ..views import fetch_rate


@override_settings(FIXERIO_API_USE_CANNED_RESPONSES=True)
class FetchRateTest(TestCase):
    """Test the fetch_rate view utility."""

    def test_success(self):
        """Test happy path with canned response."""
        s = fetch_rate(currencies.EUR, currencies.USD)

        self.assertEqual(s.data, {"rate": Decimal("1.116744")})

    @override_settings(
        FIXERIO_API_USE_CANNED_RESPONSES=False, FIXERIO_API_ACCESS_KEY="key"
    )
    @responses.activate
    def test_response_with_missing_rates(self):
        """Test validation error is returned when rates are missing."""
        responses.add(responses.GET, client.LATEST_URL, body='{"success": true}')

        with self.assertRaises(exceptions.ValidationError):
            fetch_rate(currencies.EUR, currencies.USD)

        self.assertEqual(len(responses.calls), 1)

    @override_settings(
        FIXERIO_API_USE_CANNED_RESPONSES=False, FIXERIO_API_ACCESS_KEY="key"
    )
    @responses.activate
    def test_client_error(self):
        """Test client errors are raised to the caller."""
        responses.add(
            responses.GET,
            client.LATEST_URL,
            body="{}",
            status=status.HTTP_400_BAD_REQUEST,
        )

        with self.assertRaises(HTTPError):
            fetch_rate(currencies.EUR, currencies.USD)

        self.assertEqual(len(responses.calls), 1)


@override_settings(FIXERIO_API_USE_CANNED_RESPONSES=True)
class RateViewSetConversionTest(TestCase):
    """Test the conversion view of the RateViewSet."""

    def setUp(self):
        self.client = APIClient()

    def test_conversion_success(self):
        """Test happy path for params validation."""
        response = self.client.get("/api/rates/EUR/USD/", format="json")

        # Expected response rates come from rates.fixerio.canned_responses
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"rate": 1.116744})

    def test_invalid_base_currencies(self):
        """Test various inputs for invalid base currencies."""
        bad_currencies = ("ZZZ", "INVALID", "WRONG", "WHAT")

        for bad_currency in bad_currencies:
            response = self.client.get(f"/api/rates/{bad_currency}/USD/", format="json")

            # Expected response rates come from rates.fixerio.canned_responses
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.json(), {"base": [f'"{bad_currency}" is not a valid choice.']}
            )

    def test_invalid_target_currencies(self):
        """Test various inputs for invalid target currencies."""
        bad_currencies = ("ZZZ", "INVALID", "WRONG", "WHAT")

        for bad_currency in bad_currencies:
            response = self.client.get(f"/api/rates/USD/{bad_currency}/", format="json")

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.json(),
                {"target": [f'"{bad_currency}" is not a valid choice.']},
            )

    def test_invalid_same_base_and_target_currency(self):
        """Test invalid case when base and target equal."""
        response = self.client.get(f"/api/rates/USD/USD/", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["Same currency for base and target given"]},
        )
