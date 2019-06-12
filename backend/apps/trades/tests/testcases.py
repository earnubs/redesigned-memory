from contextlib import ContextDecorator

from django.utils.timezone import now
from django.test import TestCase as DjangoTestCase

from ..models import Trade
from apps.fixerio import currencies


__all__ = ("TestCase",)


class Factory:
    def make_trade(
        self,
        sell_currency=currencies.USD,
        sell_amount="1.00",
        buy_currency=currencies.ARS,
        buy_amount="46.42",
        rate="0.0217",
        save=True,
    ):
        trade = Trade(
            sell_currency=sell_currency,
            sell_amount=sell_amount,
            buy_currency=buy_currency,
            buy_amount=buy_amount,
            rate=rate,
        )
        if save:
            trade.save()
            trade.refresh_from_db()
        return trade


class TestCase(DjangoTestCase):
    """Custom TestCase with factory and extra useful assertions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = Factory()

    def assert_trade_id(self, trade_id):
        """Assert that given trade_id follows the specification."""
        self.assertEqual(
            Trade.TRADE_IDENTIFIER_LENGTH,
            len(trade_id),
            msg=f"Trade must be of length {Trade.TRADE_IDENTIFIER_LENGTH}",
        )
        self.assertTrue(
            trade_id.startswith("TR"),
            msg=f"Trade must start with the TR prefix: {trade_id}",
        )
        for char in trade_id[2:]:
            self.assertIn(
                char,
                Trade.TRADE_IDENTIFIER_CHARS,
                msg=f"Invalid char '{char}' in trade identifier: {trade_id}",
            )

    def assert_timestamp_interval(
        self, timestamp, start, end, msg="Timestamp is outside of interval."
    ):
        """Assert that timestamp is between before and after."""
        self.assertLessEqual(start, timestamp, msg=msg)
        self.assertLessEqual(timestamp, end, msg=msg)

    class timestamp_interval(ContextDecorator):
        """Records the start and end of the execution of a code block."""

        def __enter__(self):
            self.start = now()
            return self

        def __exit__(self, exc_type, exc, exc_tb):
            self.end = now()
