import os

import pandas as pd
from celery import shared_task
from classroom.model import (
    AllowedStudents,
    AllowedTeacher,
    AllowedTeacherClassroomLevel,
    Classroom,
    College,
    Semester,
    Student,
    Teacher,
    User,
)
from classroom.models.college import AllowedCollegeDBA
from classroom.models.college_dba import CollegeDBA
from classroom.serializers import teacher
from classroom.tasks import send_email_after_bulk_object_creation
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.http import BadHeaderError
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from termcolor import cprint