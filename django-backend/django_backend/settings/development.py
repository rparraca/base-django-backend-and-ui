from django_backend.settings.base import *

DEBUG=True
# ALLOWED_HOSTS = ['*']
AUTH_PASSWORD_VALIDATORS = []

INSTALLED_APPS.append(
    'drf_yasg',
)
