"""Backend URL Configuration."""
from django.conf import settings
from django.conf.urls import url, include, re_path
from django.contrib.staticfiles import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from apps.currencies.views import CurrencyViewSet
from apps.rates.views import RateViewSet
from apps.trades.views import TradeViewSet

router = routers.DefaultRouter()
router.register(r"currencies", CurrencyViewSet, "currency")
# RateViewSet always requires a base currency
router.register(r"rates/(?P<base>[\w-]+)", RateViewSet, "rate")
router.register(r"trades", TradeViewSet)

urlpatterns = [
    url(r"^api/", include(router.urls)),
    url(r"^api/docs/", include_docs_urls(title="forex API")),
]

if settings.DEBUG:
    # Serve staticfiles on development, useful for the API console and docs.
    urlpatterns += [re_path(r"^api/static/(?P<path>.*)$", views.serve)]
