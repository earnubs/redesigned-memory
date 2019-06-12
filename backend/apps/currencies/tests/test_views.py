from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.fixerio import currencies


class CurrencyViewSetListTest(TestCase):
    """Test the list view of the CurrencyViewSet."""

    def setUp(self):
        self.client = APIClient()

    def test_success(self):
        """Test happy path."""
        response = self.client.get("/api/currencies/", format="json")
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response_json.keys(), ["currencies"])
        self.assertCountEqual(
            response_json["currencies"], [list(c) for c in currencies.CHOICES]
        )
