import os
import lightplace.settings.hidden as h
from decouple import config as cnfg
from pathlib import Path

DEBUG = h.DEBUG

ROOT_URLCONF = 'lightplace.urls'

WSGI_APPLICATION = 'lightplace.wsgi.application'
#ASGI_APPLICATION = f'{config("PROJECT_NAME")}.asgi.application'

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = h.SECRET_KEY

ALLOWED_HOSTS = ['127.0.0.1', '127.0.0.2', 'localhost', 'localhost:8080', 'light-place.nl', 'www.light-place.nl']

INSTALLED_APPS = [
    'channels',
    'chatApp',
    'avatar',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_countries',

    'core',
    'contact',
    'mptt',
    'django_thumbs',
    'ckeditor',

    'accounts',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lightplace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LANGUAGE_CODE = 'nl-nl'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

#STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

# Auth

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend'
# )

SITE_ID = 1
#LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = 'core:home'
LOGIN_REDIRECT_URL = '/chat/room/empty'
#LOGIN_URL = 'accounts:login'
LOGIN_URL = '/accounts/login/'

# allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'

# django_thumbs
THUMBS_JPG = False
VALID_ORIGINAL_EXT = ['jgp', 'jpeg', 'png', 'gif', 'webp']

# django-avatar
AVATAR_ALLOWED_FILE_EXTS = ('.jgp', '.jpeg', '.png', '.gif', '.webp')
#AVATAR_ALLOWED_FILE_EXTS = ('jgp', 'jpeg', 'png', 'gif', 'webp','.jgp', '.jpeg', '.png', '.gif', '.webp')

# Channels


#>>> From coding with mitch
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config("DB_NAME"),
#         'USER': config("DB_USER"),
#         'PASSWORD': config("DB_PASSWORD"),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
TEMP = os.path.join(BASE_DIR, 'temp')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Let op: deze settings stonden allemaal aan 8-3-2023 uitgezet
# os.environ['wsgi.url_scheme'] = 'https'
#
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 3600
# SESSION_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
# CSRF_COOKIE_SECURE = True


# email settings
EMAIL_BACKEND = h.EMAIL_BACKEND
EMAIL_HOST = h.EMAIL_HOST
EMAIL_PORT = h.EMAIL_PORT
EMAIL_HOST_USER = h.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = h.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = h.EMAIL_USE_TLS
EMAIL_USE_SSL = h.EMAIL_USE_SSL

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379
            )],
        },
    },
}
