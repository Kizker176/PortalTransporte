from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-y%a_zbte#4v@t8mebn*1z6qimuc82(8banp3&dzb4cencg^g)s"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

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

try:
    from .local import *
except ImportError:
    pass
