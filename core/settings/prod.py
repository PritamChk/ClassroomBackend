from .common import *
import os
import dj_database_url


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")  # TODO: SET DJANGO_SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = [
    "lms-classroom-api.herokuapp.com",
    "classroom-lms-api.herokuapp.com" #NEW ONE
]  # TODO: allow only localhost , port-> 3000,8000,5000,8081

DATABASES = {"default": dj_database_url.config()}


# TODO: Mail Settings for Original GMAIL
EMAIL_BACKEND = EMAIL_CREDS.EMAIL_BACKEND
EMAIL_HOST = EMAIL_CREDS.EMAIL_HOST
EMAIL_PORT = EMAIL_CREDS.PORT
EMAIL_HOST_USER = EMAIL_CREDS.get_mail_id()
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
TIME_ZONE = "Asia/Kolkata"

CELERY_BROKER_URL = os.environ['REDIS_URL'] 
