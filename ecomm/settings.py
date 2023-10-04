from pathlib import Path
from decouple import config
from django.contrib import messages
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

# ALLOWED_HOSTS = ['127.0.0.1','192.168.100.9','10.62.16.77','youthful-mountain-70598.pktriot.net']
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://60a9-14-99-167-142.ngrok-free.app'
]


ADMINS = (('venkat','venkatnvs2005@gmail.com'),)
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = [
    "daphne",
    'channels',
    'compressor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    "debug_toolbar",
    'rest_framework',
    'django_celery_results',
    'django_celery_beat',
    'utils',
    'analytics',
    'store',
    'store.details.categories',
    'store.details.search',
    'store.details.ctm_admin',
    'store.details.seller',
    'clients',
    'chat',
    'blog',
    'blog.details.blog_admin',
    'notification',
    'order',
    'voice',
    'videos',
    'src',
    'draggables',
    'ipware',
    "geoip2",
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware', #This one
    'htmlmin.middleware.HtmlMinifyMiddleware', #This one
    'htmlmin.middleware.MarkRequestMiddleware', #This one
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'utils.middleware.TrackUserViewsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = [
    "127.0.0.1",
]

GEOIP_PATH = os.path.join(BASE_DIR, 'data_files/geoip')

# SITE_NAME = 'NvsTrades'
SITE_NAME = 'GreenStore'
ROOT_URLCONF = 'ecomm.urls'
USE_OBFUSCATED_JS = True
SHOW_ANIMATIONS = False

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
                'utils.context_processors.ecommdetails'
            ],
        },
    },
]

ASGI_APPLICATION = "ecomm.asgi.application"
# WSGI_APPLICATION = 'ecomm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR,"static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # Add this
    'compressor.finders.CompressorFinder',
)

LOGIN_URL = 'login'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR :'danger'
}


COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_FILTERS = {
    'css':[
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js':[
        'compressor.filters.jsmin.JSMinFilter',
    ]
}
HTML_MINIFY = False
KEEP_COMMENTS_ON_MINIFYING = False
CONSERVATIVE_WHITESPACE_ON_MINIFYING = False

SERVER_EMAIL = config('EMAIL_FROM_EMAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_USE_TLS = config('EMAIL_TLS', cast=bool)
EMAIL_FROM_EMAIL = config('EMAIL_FROM_EMAIL')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_FROM_EMAIL')

SESSION_COOKIE_AGE = 172800


# AUTH_USER_MODEL="clients.Customer"



CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_RESULT_BACKEND = 'django-db'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

if not os.path.exists(BASE_DIR / "logs"):
    os.mkdir(BASE_DIR / "logs")

LOG_FILE = BASE_DIR / "logs" / "debug.log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    # 'root': {
        # 'handlers': ['console','file'],
        # 'level': 'WARNING',
    # },
    'loggers': {
        'django': {
            'handlers': ['console','file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins','file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}