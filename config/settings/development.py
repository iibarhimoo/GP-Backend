from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'django-insecure-dev-key'

# Local SQLite for fast testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True