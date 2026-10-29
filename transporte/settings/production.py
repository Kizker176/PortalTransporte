from .base import *
import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.environ.get("GMAIL_EMAIL", "transporte_guanajuato@guanajuato.gob.mx")
EMAIL_HOST_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "xuyolggavcuuzblh")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Correo que recibirá los mensajes del formulario
CONTACTO_DESTINO_EMAIL = os.environ.get(
    "CONTACTO_DESTINO_EMAIL",
    EMAIL_HOST_USER,
)

EMAIL_TIMEOUT = 20

DEBUG = False

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/6.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

try:
    from .local import *
except ImportError:
    pass
