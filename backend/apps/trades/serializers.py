"""API serializers for the trades app."""
from rest_framework import serializers

from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    """Serializes the Trade model."""

    class Meta:
        model = Trade
        fields = (
            "id",
            "sell_currency",
            "sell_amount",
            "buy_currency",
            "buy_amount",
            "rate",
            "date_booked",
        )
