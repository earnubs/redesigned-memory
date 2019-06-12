"""API serializers for the currencies app."""
from rest_framework import serializers

from apps.fixerio import currencies


class CurrencyListSerializer(serializers.Serializer):
    """Serializer for all available currencies."""

    currencies = serializers.MultipleChoiceField(choices=currencies.CHOICES)
