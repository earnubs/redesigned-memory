"""API serializers for the rates app."""
from decimal import Decimal

from rest_framework import serializers

from apps.fixerio import currencies


class ConversionRateParamsSerializer(serializers.Serializer):
    """Serializer for parameters given at the conversion rate retrieve view."""

    base = serializers.ChoiceField(choices=currencies.CHOICES)
    target = serializers.ChoiceField(choices=currencies.CHOICES)

    def validate(self, data):
        validated_data = super().validate(data)
        if self.initial_data["base"] == self.initial_data["target"]:
            raise serializers.ValidationError("Same currency for base and target given")
        return validated_data


class FixerIOLatestResponseSerializer(serializers.Serializer):
    """Serializer to handle fixer.io latest endpoint responses."""

    rate = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        target_currency = kwargs.pop("target_currency")
        super().__init__(*args, **kwargs)
        self.target_currency = target_currency

    def _rate_or_none(self, data):
        rate = data.get("rates", {}).get(self.target_currency)
        if rate is None:
            return
        # fixer.io API returns rates in float, in here they are
        # converted to Decimal for sanity. The main reason to cast it
        # to string first is so that Decimal receives the original API
        # value, otherwise the value may get rounded in weird ways.
        # For extra clarity here's a real life example:
        # >>> from decimal import Decimal
        # >>> Decimal(279.577253)
        # Decimal('279.57725299999998469502315856516361236572265625')
        # >>> Decimal(str(279.577253))
        # Decimal('279.577253')
        return Decimal(str(rate))

    def get_rate(self, data):
        if hasattr(self, "initial_data"):
            # This is called after validation when initial_data is
            # given, hence the rate can be returned safely from the
            # data dict directly as it's sanitized.
            return data["rate"]
        # With no validation there's a chance the given object does
        # not have the key, return None in those cases.
        return self._rate_or_none(data)

    def validate(self, data):
        validated_data = super().validate(data)
        rate = self._rate_or_none(self.initial_data)
        if rate is None:
            raise serializers.ValidationError(
                "rate for given target currency not found"
            )
        validated_data["rate"] = rate
        return validated_data
