"""
WSGI config for gameshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gameshop.settings")
application = get_wsgi_application()
application = DjangoWhiteNoise(application)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gameshop.settings")
os.environ.setdefault("PAYMENT_SELLER_ID", "S544333A51301BP62686F")
os.environ.setdefault("PAYMENT_SECRET_KEY", "c58df406f0575f96b80ecd2dd441ee2d")
