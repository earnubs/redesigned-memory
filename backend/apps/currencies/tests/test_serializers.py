from django.test import TestCase

from .. import serializers
from apps.fixerio import currencies


class CurrencyListSerializerTest(TestCase):
    """Test CurrencyListSerializer."""

    def test_serialization(self):
        """Test happy path for params validation."""
        data = {"currencies": currencies.CHOICES}
        serializer = serializers.CurrencyListSerializer(data)
        expected = {"currencies": set(v for v in data["currencies"])}

        self.assertEqual(serializer.data, expected)
