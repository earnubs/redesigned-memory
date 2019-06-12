from ..serializers import TradeSerializer
from .testcases import TestCase


class TradeSerializerTest(TestCase):
    def test_selected_fields(self):
        """Tests Trade serialization selects expected fields."""
        trade = self.factory.make_trade()

        self.assertCountEqual(
            TradeSerializer(trade).data.keys(),
            (
                "id",
                "sell_currency",
                "sell_amount",
                "buy_currency",
                "buy_amount",
                "rate",
                "date_booked",
            ),
        )
