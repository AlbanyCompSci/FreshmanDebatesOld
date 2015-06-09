#!/usr/bin/env python3.4
#file: settings.py
# Django settings for debates project.

import os
import socket
from debates_site.settings_secret import ( SECRET_KEY,
                                           SOCIAL_AUTH_GOOGLE_PLUS_KEY,
                                           SOCIAL_AUTH_GOOGLE_PLUS_SECRET,
                                           ADMINS
                                         )

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # using sqlite3
        'ENGINE': 'django.db.backends.sqlite3',
        # relative path to database file
        'NAME': 'debates.db',
    }
}

#not needed while testing with DEBUG = True
#ALLOWED_HOSTS = []

#Pacific Time Zone
TIME_ZONE = 'America/Vancouver'

#US English
LANGUAGE_CODE = 'en-us'

#?
SITE_ID = 1

#don't need internationalization
USE_I18N = False

#format dates for locale
USE_L10N = True

#use the timezone
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_ROOT + "/debates/static/",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'debates_site.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'debates_site.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_ROOT + "/debates/templates/"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    #TODO, are these necessary?
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.formtools',
    # Admin
    'django.contrib.admin',
    #'django.contrib.admindocs',
    # End of Admin
    'debates',
    #for social authentication with python-social-auth
    #(using default Django ORM)
    'social.apps.django_app.default',
    #for model imports using django-import-export
    'import_export',
)

#Google Login

AUTHENTICATION_BACKENDS = (
    #Google is deprecating OpenID and OAuth in favor of Google + authentication
    'social.backends.google.GooglePlusAuth',
    #needed because django.contrib.auth is in use
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/'

#using Google+ authorization
SOCIAL_AUTH_ENABLED_BACKENDS = ('google')
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
#only accept emails on the ausdk12.org domain
SOCIAL_AUTH_GOOGLE_WHITELISTED_DOMAINS = ['ausdk12.org']
SOCIAL_AUTH_GOOGLE_PLUS_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    #'log_details',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    #'social.pipeline.user.create_user',
    #'social.pipeline.social_auth.associate_user',
    #'social.pipeline.social_auth.load_extra_data',
    #'social.pipeline.user.user_details'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.static',
    #'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    #'django.core.context_processors.media',
    #'django.contrib.messages.context_processors.messages',
)
#End Google Login

LOG_DIR = PROJECT_ROOT + '/logs'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'dev_debug':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/debug.log'
        },
        'dev_info':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/info.log'
        },
        'dev_warning':{
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/warning.log'
        },
        'dev_error':{
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/error.log'
        },
        'dev_critical':{
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/critical.log'
        }

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'logview.debugger': {
            'handlers': ['dev_debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'logview.info': {
            'handlers': ['dev_info'],
            'level': 'INFO',
            'propagate': True,
        },
        'logview.warning': {
            'handlers': ['dev_warning'],
            'level': 'WARNING',
            'propagate': True,
        },
        'logview.error': {
            'handlers': ['dev_error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'logview.critical': {
            'handlers': ['dev_critical'],
            'level': 'CRITICAL',
            'propagate': True,
        },
    }
}
