from celery import shared_task
from django.core.mail import send_mass_mail, send_mail
from .models import Classroom
import os

@shared_task
def send_email_after_mass_profile_creation(
    mails
):
    send_mass_mail(mails, fail_silently=True)
    
