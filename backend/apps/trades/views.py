"""API views for the trades app."""
from rest_framework import mixins
from rest_framework import viewsets

from .models import Trade
from .serializers import TradeSerializer
from apps.rates.views import fetch_rate


class TradeViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Trade.objects.order_by("-date_booked")
    serializer_class = TradeSerializer

    def perform_create(self, serializer):
        fixerio_serializer = fetch_rate(
            base=serializer.validated_data["sell_currency"],
            target=serializer.validated_data["buy_currency"],
        )
        rate = fixerio_serializer.validated_data["rate"]
        # TODO: define and apply rounding rule here:
        buy_amount = serializer.validated_data["sell_amount"] * rate
        serializer.save(rate=rate, buy_amount=buy_amount)
