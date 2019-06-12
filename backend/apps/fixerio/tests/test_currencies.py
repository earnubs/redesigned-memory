from django.test import TestCase

from .. import currencies


class CurrenciesTest(TestCase):
    """Test the currencies module."""

    def test_generated_symbols(self):
        """Test all generated symbols are available."""
        for symbol, _ in currencies.CHOICES:
            self.assertTrue(hasattr(currencies, symbol))
            self.assertEqual(getattr(currencies, symbol), symbol)
