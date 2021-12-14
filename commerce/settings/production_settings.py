import os
from .base_settings import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['cornu-exchange.herokuapp.com',
                 'localhost', '127.0.0.1']

STATIC_URL = 'stacitfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'commerce_db',
        'USER': 'postgres',
        'PASSWORD': 'pTu2TfRrcjtNb2zYyTKv',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}
