"""API views for the rates app."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ConversionRateParamsSerializer, FixerIOLatestResponseSerializer
from apps.fixerio import client


def fetch_rate(base, target) -> FixerIOLatestResponseSerializer:
    """View utility to fetch a serialized rate conversion from fixer.io."""
    response = client.latest(base=base, symbols=[target])
    response_serializer = FixerIOLatestResponseSerializer(
        data=response, target_currency=target
    )
    response_serializer.is_valid(raise_exception=True)
    return response_serializer


class RateViewSet(viewsets.GenericViewSet):
    """ViewSet for rate related endpoints.

    Views in this special viewset always receive a `base` kwarg with
    the base currency to work with.
    """

    lookup_url_kwarg = "target"

    def retrieve(self, request, base, target):
        """Retrieve rate conversion for given base and target currencies.

        Parameters:
        base -- three-letter currency code for the base currency
        target -- three-letter currency code for the target currency

        Returns a RetrieveRateFixerIOResponseSerializer formated response
        """
        params_serializer = ConversionRateParamsSerializer(
            data={"base": base.upper(), "target": target.upper()}
        )
        params_serializer.is_valid(raise_exception=True)

        # Ensure base and target sanitized version from now on
        base = params_serializer.validated_data["base"]
        target = params_serializer.validated_data["target"]

        return Response(fetch_rate(base, target).data)
