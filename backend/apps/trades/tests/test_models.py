from django.core.exceptions import ValidationError
from django.utils.timezone import now

from decimal import Decimal
import itertools

from .testcases import TestCase
from apps.fixerio import currencies


class TradeTest(TestCase):
    """Test Trade model."""

    def test_creation_ok(self):
        """Tests Trade creation with valid values."""
        with self.timestamp_interval() as ctx:
            trade = self.factory.make_trade(
                sell_currency=currencies.USD,
                sell_amount="1.00",
                buy_currency=currencies.ARS,
                buy_amount="46.42",
                rate="0.0217",
            )

        self.assert_trade_id(trade.id)
        self.assertEqual(trade.sell_currency, "USD")
        self.assertEqual(trade.sell_amount, Decimal("1.00"))
        self.assertEqual(trade.buy_currency, "ARS")
        self.assertEqual(trade.buy_amount, Decimal("46.42"))
        self.assertEqual(trade.rate, Decimal("0.0217"))
        self.assert_timestamp_interval(trade.date_booked, ctx.start, ctx.end)

    def test_manual_field_validation(self):
        """Tests validation for all manual fields."""
        fields = ("sell_currency", "sell_amount", "buy_currency")
        values = ("INVALID", "", None)
        test_cases = itertools.product(fields, values)
        for field, value in test_cases:
            trade = self.factory.make_trade(save=False)
            setattr(trade, field, value)
            with self.assertRaises(
                ValidationError, msg=f"Expected {field} with value {value} to raise."
            ):
                trade.full_clean()

    def test_allowed_decimal_places(self):
        """Tests allowed decimal places limit."""
        test_cases = (("sell_amount", 2), ("buy_amount", 2), ("rate", 6))
        value = "1.0987654321"
        non_decimal_places = 2
        for field, expected_places in test_cases:
            trade = self.factory.make_trade(save=False)
            setattr(trade, field, value[: non_decimal_places + expected_places])
            trade.full_clean()
            trade.save()
            trade.refresh_from_db()
            # overflow by one digit
            setattr(trade, field, value[: non_decimal_places + expected_places + 1])
            with self.assertRaises(
                ValidationError,
                msg=f"Expected {field} with {value} to raise ValidationError.",
            ):
                trade.full_clean()

    def test_same_currency_for_sell_and_buy_is_not_allowed(self):
        """Tests sell_currency and buy_currency cannot be the same."""
        trade = self.factory.make_trade(
            buy_currency=currencies.USD, sell_currency=currencies.USD, save=False
        )
        with self.assertRaisesRegexp(
            ValidationError, r"Currencies must be different\."
        ):
            trade.full_clean()

    def test_date_booked_is_not_editable(self):
        """Tests date_booked field cannot be manually assigned."""
        date_booked = now()
        trade = self.factory.make_trade(save=False)
        trade.date_booked = date_booked
        trade.save()
        trade.refresh_from_db()
        self.assertNotEqual(trade.date_booked, date_booked)
