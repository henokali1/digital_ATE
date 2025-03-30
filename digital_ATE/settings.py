"""
Django settings for digital_ATE project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-ug3l$63&ol=wj20_tf+c48($ofp8g5_=0%vp(of4sc%+k7j!hg'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ALLOWED_HOSTS = ['atemms.fans.ae','192.168.10.10', 'ate.henokcodes.com', 'localhost', '127.0.0.1', '*']

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# If you're using SSL/Cloudflare, add these
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False    

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds

# Add more complete CSRF settings
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_DOMAIN = None
CSRF_TRUSTED_ORIGINS = [
    'https://atemms.fans.ae',
    'http://192.168.10.10',
    'https://192.168.10.10',
    'https://ate.henokcodes.com',
    'http://ate.henokcodes.com',
    'http://localhost',
    'http://127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'job_card.templatetags',
    'widget_tweaks',
    'accounts',
    'pages',
    'asset',
    'logbook',
    'location',
    'admin_dashboard',
    'preventive_maintenance',
    'corrective_maintenance',
    'job_card',
    'daily_inspection',
    'django_select2',
    'bug_report',
    'feature_request',
    'spare_parts',
    'network_inventory',
    'om_manuals',
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

ROOT_URLCONF = 'digital_ATE.urls'

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
                'django.template.context_processors.media',
            ],
             'builtins': ['job_card.templatetags.job_card_tags'],
        },
    },
]

WSGI_APPLICATION = 'digital_ATE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
# DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
DEBUG = True
#ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  
# Add this to point to your static directory
# STATICFILES_DIRS = [Path(BASE_DIR) / "static"]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
#Manual folder Directory
MANUALS_ROOT = os.path.join(BASE_DIR, 'manuals')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

