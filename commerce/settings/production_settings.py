import os
from .base_settings import *
import django_heroku

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['cornu-exchange.herokuapp.com',
                 'localhost', '127.0.0.1']

STATIC_URL = 'stacitfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


django_heroku.settings(locals())
