from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "Not Exists")

# TODO: Make this false in production
DEBUG = True

ALLOWED_HOSTS = ["*", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "classroom",
        "USER": "root",
        "PASSWORD": "Abcd_1234",
        "HOST": "mysql",
        "PORT": "3306",
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': os.environ.get('POSTGRES_NAME','classroom'),
    #     'USER': os.environ.get('POSTGRES_USER','postgres'),
    #     'PASSWORD': os.environ.get('POSTGRES_PASSWORD','postgres'),
    #     'HOST': 'postgres',
    #     'PORT': 5432,
    # }
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
