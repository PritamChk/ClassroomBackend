from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "Not Exists")

# TODO: Make this false in production
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        # "NAME": os.getenv(
        #     "DB_NAME",
        #     "classroom",
        # ),
        "NAME": "classroom",
        # "USER": os.getenv("DB_USER", "pritam"),
        "USER": "root",
        # "PASSWORD": os.getenv("DB_USER_PASSWORD", "Abcd_1234"),
        "PASSWORD": "Abcd_1234",
        # "HOST": "localhost",
        "HOST": "mysql",
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
# EMAIL_HOST = "localhost"
EMAIL_HOST = "smtp4dev"
EMAIL_PORT = 25
EMAIL_HOST_USER = "classroom@lms.com"
EMAIL_HOST_PASSWORD = ""
# DEFAULT_FROM_EMAIL = "classroom@lms.com"

# CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_BROKER_URL = "redis://redis:6379/1"

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}
