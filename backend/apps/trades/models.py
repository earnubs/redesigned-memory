"""Data models for the trades app."""
import random
import string

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.fixerio import currencies

__all__ = ("Trade",)


def _trade_pk():
    """Generate random valid primary keys for Trade objects."""
    rng = random.SystemRandom()
    return "TR" + "".join(rng.sample(Trade.TRADE_IDENTIFIER_CHARS, 7))


class Trade(models.Model):
    """Trade records all trading transactions in the system.

    The `id` primary_key is not the typical auto-increment integer but
    an auto-generated string with the format "TR" + 7 alphanumerics.

    """

    TRADE_IDENTIFIER_CHARS = string.ascii_uppercase + string.digits
    TRADE_IDENTIFIER_LENGTH = 9  # TR + 7 alphanumerics

    id = models.CharField(
        blank=False,
        default=_trade_pk,
        editable=False,
        max_length=TRADE_IDENTIFIER_LENGTH,
        null=False,
        primary_key=True,
        help_text=_("Auto-generated unique trade identifier."),
    )
    sell_currency = models.CharField(
        blank=False,
        choices=currencies.CHOICES,
        max_length=3,
        null=False,
        help_text=_("Currency to sell."),
    )
    sell_amount = models.DecimalField(
        blank=False,
        decimal_places=2,
        max_digits=1024 + 2,
        null=False,
        help_text=_("Amount to sell."),
    )
    buy_currency = models.CharField(
        blank=False,
        choices=currencies.CHOICES,
        max_length=3,
        null=False,
        help_text=_("Currency to buy."),
    )
    buy_amount = models.DecimalField(
        blank=False,
        decimal_places=2,
        editable=False,
        max_digits=1024 + 2,
        null=False,
        help_text=_("Amount to buy."),
    )
    rate = models.DecimalField(
        blank=False,
        decimal_places=6,
        editable=False,
        max_digits=1024 + 6,
        null=False,
        help_text=_("Calculated rate at the time of transaction."),
    )
    date_booked = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        editable=False,
        null=False,
        help_text=_("Timestamp of the transaction."),
    )

    def clean(self):
        # Don't allow same currency for buy and sell
        if self.sell_currency == self.buy_currency:
            raise ValidationError(_("Currencies must be different."))
