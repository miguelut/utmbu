from django.contrib.messages import constants as messages
try:
    from config import *
except:
    pass
"""
Django settings for utmbu project.

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
SECRET_KEY = 'p!&=iq9x%r#*_8w4+w**kup)dgn3im1y4trdiukath_j488@71'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Trying Something
APPEND_SLASH = True

# Template Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'mbu.context_processors.default_links',
    'mbu.context_processors.add_links',
    'mbu.context_processors.add_report_links',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paypal.standard.ipn',
    'social.apps.django_app.default',
    'crispy_forms',
    'widget_tweaks',
    'mbu',
    'dev',
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

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GooglePlusAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    # 'mbu.pipeline.user_type.user_get_names
    'mbu.pipeline.user_type.user_make_scout'
)

ROOT_URLCONF = 'utmbu.urls'

WSGI_APPLICATION = 'utmbu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

#USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#Template Directories
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'mbu_home'

#Setting up Message Tags to be Bootstrap Compliant
MESSAGE_TAGS = {
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
    messages.INFO: 'alert-info',
}

#MBU Settings
DEFAULT_LINKS = [
    {'href': 'reports', 'label': 'About'},
    {'href': 'reports', 'label': 'FAQ'},
    {'href': 'class_list', 'label': 'Class List'}
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SOCIAL_AUTH_FACEBOOK_KEY = '914815875236577'
SOCIAL_AUTH_FACEBOOK_SECRET = 'd195882a4187fd90ac06f450f3d05221'
SOCIAL_AUTH_FACBEOOK_SCOPE = 'email'
SOCIAL_AUTH_GOOGLE_PLUS_KEY = '792511177887-a4c3bmo8b4h2nqenj1jc6t0ikmfs9nf2.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'dY6poV-JymLr-fEmCxsQut1u'

EMAIL_HOST = 'mail.vexule.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mbu'
EMAIL_HOST_PASSWORD = 'etzilch'

SITE_URL = 'http://localhost:8000'
MBU_LOCATION = 'The University of Texas at Austin'

PAYPAL_RECEIVER_EMAIL='mbu@vexule.com'
PAYPAL_TEST=True
PAYPAL_NOTIFY_URL='http://localhost:8080/paypal/notify'

PRICE_PER_COURSE = 7.5