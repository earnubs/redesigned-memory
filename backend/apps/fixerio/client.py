"""Simple API client for the fixer.io service."""
from urllib.parse import urljoin

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import requests

from . import canned_responses
from . import exceptions

__all__ = ("BASE_URL", "LATEST_URL", "latest")

BASE_URL = "http://data.fixer.io/api/"
LATEST_URL = urljoin(BASE_URL, "latest")


def latest(base=None, symbols=None):
    """Retrieve the latest rates.

    Keyword arguments:
    base -- three-letter currency code for the preferred base currency
    symbols -- list of comma-separated currency codes to limit output

    Configuration depends on the following django.conf.settings:
    FIXERIO_API_ACCESS_KEY -- API Key to use when hitting endpoints
    FIXERIO_API_USE_CANNED_RESPONSES -- If set and True return canned
    responses and don't hit the API
    """
    if getattr(settings, "FIXERIO_API_USE_CANNED_RESPONSES", False):
        # TODO: make this response more dynamic and closer to IRL.
        return canned_responses.latest

    access_key = getattr(settings, "FIXERIO_API_ACCESS_KEY", "")
    if not access_key:
        raise ImproperlyConfigured("The FIXERIO_API_ACCESS_KEY setting is required.")

    params = {"access_key": access_key}

    if base is not None:
        params["base"] = base

    if symbols is not None:
        params["symbols"] = ",".join(symbols)

    response = requests.get(LATEST_URL, params=params)
    # this is a safety measure that should not raise as the API always
    # returns HTTP 200 even on errors.
    response.raise_for_status()

    data = response.json()
    if not data.get("success", False):
        error_code = data.get("error", {}).get("code")
        cls = exceptions.error_response_to_exception(error_code)
        raise cls

    return data
