from decimal import Decimal
import itertools

from django.test import TestCase

from .. import serializers
from apps.fixerio import currencies


class ConversionRateParamsSerializerTest(TestCase):
    """Test ConversionRateParamsSerializer."""

    def test_validation_ok(self):
        """Test happy path for params validation."""
        valid_data = {"base": currencies.EUR, "target": currencies.USD}
        serializer = serializers.ConversionRateParamsSerializer(data=valid_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, valid_data)

    def test_invalid(self):
        """Tests several invalid inputs."""
        fields = ("base", "target")
        values = ("INVALID", "", None)
        test_cases = itertools.product(fields, values)

        for field, value in test_cases:
            params = {"base": currencies.EUR, "target": currencies.USD}
            params[field] = value
            serializer = serializers.ConversionRateParamsSerializer(data=params)

            self.assertFalse(
                serializer.is_valid(),
                msg=f"{field} validation with value {value} must be False.",
            )


class FixerIOLatestResponseSerializerTest(TestCase):
    """Test FixerIOLatestResponseSerializer."""

    def test_serialization_ok(self):
        """Test rate is extracted from input to serialize."""
        expected_rate = Decimal("1.123456")
        s = serializers.FixerIOLatestResponseSerializer(
            {"rates": {"USD": expected_rate}}, target_currency=currencies.USD
        )
        self.assertEqual(s.data, {"rate": expected_rate})

    def test_validation_ok(self):
        """Test happy path for rate validation."""
        expected_rate = Decimal("1.123456")
        s = serializers.FixerIOLatestResponseSerializer(
            data={"rates": {"USD": expected_rate}}, target_currency=currencies.USD
        )

        self.assertTrue(s.is_valid())
        self.assertEqual(s.data, {"rate": expected_rate})
        self.assertEqual(s.validated_data, {"rate": expected_rate})

    def test_invalid(self):
        """Tests several invalid inputs."""
        test_cases = ({}, {"base": "EUR"}, {"rates": {"OTHER": 1.0}})
        for data in test_cases:
            serializer = serializers.FixerIOLatestResponseSerializer(
                data=data, target_currency=currencies.USD
            )

            self.assertFalse(
                serializer.is_valid(),
                msg=f"Expected validation with data {data} to be False.",
            )
