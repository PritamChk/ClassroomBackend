from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class BaseAccountManager(BaseUserManager):
    def create_user(self, first_name: str, last_name: str, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not first_name:
            raise ValueError(_('The First Name must be set'))
        if not last_name:
            raise ValueError(_('The Last Name must be set'))
        if not first_name:
            raise ValueError(_('The First Name must be set'))
        if not last_name:
            raise ValueError(_('The Last Name must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name.title(),
            last_name=last_name.title(),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(first_name, last_name, email, password, **extra_fields)
