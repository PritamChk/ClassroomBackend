from celery import shared_task
from django.core.mail import send_mass_mail, send_mail
from .model import AllowedTeacher
import os
from django.conf import settings
import pandas as pd


@shared_task
def send_email_after_bulk_object_creation(subject: str, prompt: str, email_list):
    """
    # It sends mass mail
        - takes 3 `parameter`
        - subject
        - common prompt
        - email_list
    """
    mails = [
        (
            subject,
            f"{prompt} - \nUSED MAIL ID : {m}",
            settings.EMAIL_HOST_USER,
            [m],
        )
        for m in email_list
    ]
    send_mass_mail(mails, fail_silently=True)
