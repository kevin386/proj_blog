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

MANAGERS = ADMINS=(
    ('kevin', 'null_386@qq.com'),
    ('kevin', 'luozhiyong134@126.com'),
)

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

ALLOWED_HOSTS = ["*"]


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
    'django.middleware.locale.LocaleMiddleware',
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
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-ch'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'


WEB_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/site.log")
WORKER_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/worker.log")

LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

WORKER_LOG_LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
        },
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda x: DEBUG,
        }
    },
    'handlers': {

        'rotating_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': WEB_LOG_FILE_PATH,
            'maxBytes': 1024*1024*500,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'worker_file': {
            'level': WORKER_LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': WORKER_LOG_FILE_PATH,
            'maxBytes': 1024*1024*500,
            'backupCount': 5,
            'formatter': 'standard',
            },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },

    },
    'loggers': {
        'django': {
            'handlers': ['rotating_file', 'flylog'],
            'level': 'DEBUG',
            'propagate': False
        },

        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'worker': {
            'handlers': ['console', 'worker_file'],
            'level': WORKER_LOG_LEVEL,
            'propagate': False
        },
    }
}
