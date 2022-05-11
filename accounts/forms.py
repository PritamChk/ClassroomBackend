from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import BaseAccount


class AccountCreationForm(UserCreationForm):
    class Meta:
        mdoel = BaseAccount
        fields = ("email", "first_name", "last_name")


class AccountChangeForm(UserChangeForm):
    class Meta:
        mdoel = BaseAccount
        fields = ("email", "first_name", "last_name", "contact_no", "date_joined")
