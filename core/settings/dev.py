from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',"Not Exists")

# TODO: Make this false in production
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "classroom",
        "USER": "pritam",
        "PASSWORD": "Abcd_1234",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

DEV_APPS = [
    "debug_toolbar",
]

DEV_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
MIDDLEWARE += DEV_MIDDLEWARE
INSTALLED_APPS += DEV_APPS
INTERNAL_IPS = [
    "127.0.0.1",
]

# TODO: FAKE-MAIL Comment this in production
# TODO:Mail Settings for Fake Mail
EMAIL_BACKEND = EMAIL_CREDS.EMAIL_BACKEND
EMAIL_HOST = "localhost"
EMAIL_PORT = 2525
EMAIL_HOST_USER = "classroom@lms.com"
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "classroom@lms.com"