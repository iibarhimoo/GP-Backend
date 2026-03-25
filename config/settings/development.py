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

# MongoDB Configuration for Development
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'gp-mongodb-service-dev'

CORS_ALLOW_ALL_ORIGINS = True