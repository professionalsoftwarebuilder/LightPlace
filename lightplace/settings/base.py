import os
from decouple import config

from pathlib import Path

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["104.248.195.6",]

ROOT_URLCONF = f'{config("PROJECT_NAME")}.urls'

WSGI_APPLICATION = f'{config("PROJECT_NAME")}.wsgi.application'

ASGI_APPLICATION = f'{config("PROJECT_NAME")}.routing.application'

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [

    'channels',
    'chatApp',
    'accounts',
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
    'crispy_forms',
    'django_countries',

    'core',
    'contact',
    'mptt',
    'django_thumbs',
    'ckeditor',
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

#ROOT_URLCONF = 'lightplace.urls'

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

#WSGI_APPLICATION = 'lightplace.wsgi.application'

LANGUAGE_CODE = 'nl-nl'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

#STATIC_URL = '/static/'
#MEDIA_URL = '/media/'
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
#STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

# Auth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

SITE_ID = 1
#LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = 'core:home'
LOGIN_REDIRECT_URL = '/chat/room/empty'
#LOGIN_URL = 'accounts:login'
LOGIN_URL = '/accounts/login/'

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'

# django_thumbs
THUMBS_JPG = False
VALID_ORIGINAL_EXT = ['jgp', 'jpeg', 'png', 'gif', 'webp']

# django-avatar
AVATAR_ALLOWED_FILE_EXTS = ('.jgp', '.jpeg', '.png', '.gif', '.webp')
#AVATAR_ALLOWED_FILE_EXTS = ('jgp', 'jpeg', 'png', 'gif', 'webp','.jgp', '.jpeg', '.png', '.gif', '.webp')



# email settings
EMAIL_HOST = 'smtp03.hostnet.nl'
EMAIL_PORT = 465
#EMAIL_PORT = 587
EMAIL_HOST_USER = 'kaart@light-place.nl'
EMAIL_HOST_PASSWORD = '%rzF13jF1l'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# Channels
#ASGI_APPLICATION = 'lightplace.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379
)],
        },
    },
}

os.environ['wsgi.url_scheme'] = 'https'

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
CSRF_COOKIE_SECURE = True

#>>> From coding with mitch
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = config('AWS_LOCATION')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
TEMP = os.path.join(BASE_DIR, 'temp')
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'CodingWithMitch Team <noreply@codingwithmitch.com>'


BASE_URL = "http://104.248.195.6"