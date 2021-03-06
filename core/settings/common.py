"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from ..mail import EmailCreds
from datetime import timedelta
from pathlib import Path

EMAIL_CREDS = EmailCreds()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # FIXME: .parent added

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APP = [
    "corsheaders",
    "rest_framework",
    "djoser",
    "django_extensions",
    "drf_yasg",
]

OWN_APP = ["accounts", "classroom"]

INSTALLED_APPS += THIRD_PARTY_APP + OWN_APP

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # TODO: 3rd party middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


THIRD_PARTY_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

MIDDLEWARE = THIRD_PARTY_MIDDLEWARE + MIDDLEWARE


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"
# TIME_ZONE = "UTC"

USE_I18N = True

# USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(
    BASE_DIR, "static"
)  # This line will collect all static files

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # FIXME: if not works, delete these line

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------#3-RD PARTY APPS CONFIG -------------------


# TODO: Djoser Settings Open
DJOSER = {
    # "SET_PASSWORD_RETYPE": True, #TODO: Confirm Password [Djoser]
    "SEND_CONFIRMATION_EMAIL": True,
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_CONFIRM_URL": "reset_password_confirm/{uid}/{token}",
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "USERNAME_RESET_CONFIRM_URL": "reset_email_confirm/{uid}/{token}",
    # "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": False, #TODO: if want to expose details about email then open it else leave it
    "SERIALIZERS": {
        "current_user": "accounts.serializers.CurrentUserSerializer",
        "username_reset_confirm": "accounts.serializers.UseranmeResetConfirmSerializer",
    },
}

SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "core.swagger_schema.CustomAutoSchema",
    "LOGIN_URL": "admin/",
    "LOGOUT_URL": "admin/logout",
    "OPERATIONS_SORTER": "method",
    "TAGS_SORTER": "alpha",
    "DOC_EXPANSION": "none",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination", #TODO: Pagination Setting Open 1
    # "PAGE_SIZE": 5, # TODO: default pagination value:5
}
# -----------------------------END of #3-RD PARTY APPS CONFIG -------------------

# ======== CUSTOM CONSTANTS --------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_HEADERS = [
    "accept",
    "filename",
    "accept-encoding",
    "authorization",
    "content-type",
    "content-disposition",
    "dnt",
    "boundary",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "csrfmiddlewaretoken",
]


AUTH_USER_MODEL = "accounts.BaseAccount"

DOMAIN = "localhost:8081"  # TODO: change after frontend deployment
SITE_NAME = "Classroom[LMS]"
