"""
Django settings for proj_blog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates'),
    os.path.join(BASE_DIR,'blog/templates'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2tpji9&$=xic@ytaqiq4$1&f*rj&&p$k3c!0o9q)x6v4el2t#4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'blog',
    'south',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proj_blog.urls'

WSGI_APPLICATION = 'proj_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
import ConfigParser as CP
configPath = os.path.join(BASE_DIR,'psw.cfg')
config = CP.ConfigParser()
with open(configPath, 'r') as cfgfile:
	config.readfp(cfgfile)
	user = config.get("dbinfo",'user')
	psw = config.get("dbinfo",'psw')
	host = config.get("dbinfo",'host')
	port = config.get("dbinfo",'port')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'proj_blog',                      # Or path to database file if using sqlite3.
        'USER': user,                      # Not used with sqlite3.
        'PASSWORD': psw,                  # Not used with sqlite3.
        'HOST': host,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': port,                      # Set to empty string for default. Not used with sqlite3.
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
