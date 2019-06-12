from urllib.parse import urlparse, parse_qsl
import json

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from requests.exceptions import HTTPError
import responses

from .. import canned_responses
from .. import client
from .. import exceptions


@override_settings(FIXERIO_API_USE_CANNED_RESPONSES=False)
@override_settings(FIXERIO_API_ACCESS_KEY="key")
class ClientTest(TestCase):
    @override_settings(FIXERIO_API_USE_CANNED_RESPONSES=True)
    def test_uses_canned_responses_if_enabled(self):
        self.assertEqual(client.latest(), canned_responses.latest)

    @override_settings(FIXERIO_API_ACCESS_KEY=None)
    def test_api_key_is_required(self):
        with self.assertRaises(ImproperlyConfigured):
            client.latest()

    @responses.activate
    def test_call_with_no_args(self):
        responses.add(responses.GET, client.LATEST_URL, body='{"success": true}')

        self.assertEqual(client.latest(), {"success": True})
        self.assertEqual(len(responses.calls), 1)

        parsed = urlparse(responses.calls[0].request.path_url)
        qs = dict(parse_qsl(parsed.query))

        self.assertEqual(qs, {"access_key": "key"})

    @responses.activate
    def test_call_with_no_base(self):
        responses.add(responses.GET, client.LATEST_URL, body='{"success": true}')

        self.assertEqual(client.latest(symbols=["USD", "EUR"]), {"success": True})
        self.assertEqual(len(responses.calls), 1)

        parsed = urlparse(responses.calls[0].request.path_url)
        qs = dict(parse_qsl(parsed.query))

        self.assertEqual(qs, {"access_key": "key", "symbols": "USD,EUR"})

    @responses.activate
    def test_call_with_no_symbols(self):
        responses.add(responses.GET, client.LATEST_URL, body='{"success": true}')

        self.assertEqual(client.latest(base="USD"), {"success": True})
        self.assertEqual(len(responses.calls), 1)

        parsed = urlparse(responses.calls[0].request.path_url)
        qs = dict(parse_qsl(parsed.query))

        self.assertEqual(qs, {"access_key": "key", "base": "USD"})

    @responses.activate
    def test_call_with_exception(self):
        responses.add(responses.GET, client.LATEST_URL, body="{}", status=400)

        with self.assertRaises(HTTPError):
            client.latest()

    @responses.activate
    def test_call_with_error(self):
        responses.add(
            responses.GET,
            client.LATEST_URL,
            body=json.dumps(canned_responses.missing_api_key_error),
            status=200,
        )

        with self.assertRaises(exceptions.FixerIOUnrecoverableError):
            client.latest()
