"""
Django settings for unemployment_mining project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@qfnlkek3x48!u%=!7iyndvd_pgrtzzep+k1x4#i_1g#z+*u_w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), "templates/"),

)


ALLOWED_HOSTS = []

TEMPLATE_LOADERS = (
    'django.template.loaders.cached.Loader', 
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Application definition

INSTALLED_APPS = (
    #Custom admin interface (must be put before django.contrib.admin)
    'grappelli',
    # Django core packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External libraries
    'crispy_forms',
     # Project apps
    'data',
    'visualization',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'unemployment_mining.urls'

WSGI_APPLICATION = 'unemployment_mining.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'unemployment_mining_db',
        'USER': 'unemployment_admin',
        'PASSWORD': '12unemployment#$',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/webapps/unemployment_mining/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/webapps/unemployment_mining/media'
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# For crispy_forms

CRISPY_TEMPLATE_PACK = 'bootstrap3'

#For Django-Grapilly redesigned admin interface

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',

)