from decimal import Decimal

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from .. import serializers
from ..models import Trade
from .testcases import TestCase
from apps.fixerio import currencies


@override_settings(FIXERIO_API_USE_CANNED_RESPONSES=True)
class TradeViewSetCreateTest(TestCase):
    """Test the create view of the TradeViewSet."""

    def setUp(self):
        self.client = APIClient()

    def test_create_success(self):
        """Test happy path."""
        data = {
            "sell_currency": currencies.EUR,
            "buy_currency": currencies.ARS,
            "sell_amount": "500.00",
        }
        with self.timestamp_interval() as ctx:
            response = self.client.post("/api/trades/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()
        created_trade = Trade.objects.get(pk=response_json["id"])

        self.assertEqual(created_trade.buy_amount, Decimal("25102.19"))
        self.assertEqual(created_trade.buy_currency, currencies.ARS)
        self.assertEqual(created_trade.rate, Decimal("50.204387"))
        self.assertEqual(created_trade.sell_amount, Decimal("500.00"))
        self.assertEqual(created_trade.sell_currency, currencies.EUR)
        self.assert_timestamp_interval(created_trade.date_booked, ctx.start, ctx.end)


class TradeViewSetListTest(TestCase):
    """Test the list view of the TradeViewSet."""

    def setUp(self):
        self.client = APIClient()

    def test_list_empty(self):
        """Test happy path with no instances."""
        response = self.client.get("/api/trades/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_list_success(self):
        """Test happy path."""
        first = self.factory.make_trade()
        second = self.factory.make_trade()
        third = self.factory.make_trade()

        response = self.client.get("/api/trades/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                serializers.TradeSerializer(third).data,
                serializers.TradeSerializer(second).data,
                serializers.TradeSerializer(first).data,
            ],
            msg="Instances should be ordered by descending date_booked",
        )
