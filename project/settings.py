"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from dataclasses import dataclass
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-mrvesblge+5oorwdld5%805wertabs2xpvlk4o)ix!degm2hjg'

#FOR DOCKER
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

#FOR DOCKER
DEBUG = int(os.environ.get("DEBUG", default=0))

#ALLOWED_HOSTS = ['127.0.0.1','testserver']


# 'DJANGO_ALLOWED_HOSTS' должен быть в виде одной строки с хостами разделенными символом пробела
# Для примера: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app_logs_apache',
    'rest_framework',
    'django_filters',
    "daterange.apps.DateRangeFilterConfig",
    'django_crontab',


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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# FOR UNIT (PYTEST)
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

#import sys
#
#TESTING = sys.argv[1:2] == ['test']
#if TESTING==False:
#    DATABASES = {
#    'default': {
#    'ENGINE': 'django.db.backends.postgresql_psycopg2',
#    'NAME': 'djangodb',
#    'USER': 'django',
#    'PASSWORD': '12345678',
#    'HOST': 'localhost',
#    'PORT': '',
#    }
#    }
#else:
#    DATABASES = {    
#        'default': {
#        "ENGINE": "django.db.backends.sqlite3",
#        "TEST": {
#            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
#        }
#    }}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False 

USE_TZ = False


CRONJOBS = [
 ('*/1 * * * *', 'app_logs_apache.services.cron.log_handler_apache')
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


@dataclass(frozen=True)
class ConfigParseLogs:
    PATH_FILE: str = r"/var/log/apache2/access.log"
    MASK_IPV4: str = r"^\d+[.]\d+[.]\d+"
    MASK_IPV6_V1: str = r"^\d+[:]\d+[:]\d+"
    MASK_IPV6_V2: str = r"::\d+"
    MASK_DATE: str = r"\d+[/]\D+[/]\d+[:]\d+[:]\d+[:]\d+ [+]\d+\d+\d+\d+"
    MASK_FORMAT_DATE: str = '%d/%b/%Y:%H:%M:%S +%f'
