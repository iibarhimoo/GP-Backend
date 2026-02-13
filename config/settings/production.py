import os
from .base import * 

DEBUG = False

# 1. SECURITY: GET KEYS FROM DOKPLOY ENVIRONMENT
SECRET_KEY = os.environ.get('SECRET_KEY')

# Defines who can connect to your app (e.g., 'api.yourdomain.com')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# 2. DATABASE: CONNECT TO YOUR DOKPLOY MYSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "gp_main_db"),
        "USER": os.environ.get("DB_USER", "gp_admin"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT", "55310"),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# 3. STATIC FILES
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 4. SECURITY & SSL (HTTPS)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ⚠️ THE "MAGIC" FIX FOR DOKPLOY/TRAEFIK
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 5. TRUSTED ORIGINS (REQUIRED FOR DJANGO 4.0+)
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')