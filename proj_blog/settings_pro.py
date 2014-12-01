"""
Django settings for proj_blog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from proj_blog.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["*"]

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
    EMAIL_HOST = config.get('email','EMAIL_HOST') 
    EMAIL_PORT = int(config.get('email','EMAIL_PORT'))
    EMAIL_HOST_USER = config.get('email','EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config.get('email','EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = True

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
