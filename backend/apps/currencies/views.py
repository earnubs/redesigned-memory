"""API views for the currencies app."""
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CurrencyListSerializer
from apps.fixerio import currencies


class CurrencyViewSet(viewsets.GenericViewSet):
    """ViewSet for currency related endpoints."""

    def list(self, request):
        """Return all acceptable currencies.

        Returns a CurrencyListSerializer formated response
        """
        response_serializer = CurrencyListSerializer({"currencies": currencies.CHOICES})
        return Response(response_serializer.data)
