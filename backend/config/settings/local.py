"""
Django local settings for backend project.

These settings are intended for local development.
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "backend",
    "localhost",
]

SECRET_KEY = '%vrfkgv9iq=@m-ln-$_)4=b8e%gda)4p8#4)(#iwbg84aj39rk'

# Only use staticfiles in dev for the API browser.
STATIC_URL = '/api/static/'
