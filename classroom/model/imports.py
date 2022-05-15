from datetime import date, datetime, timedelta
from random import randint
from time import time

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from classroom.constants import LEVEL_CHOICES, SECTION_CHOICES
from classroom.managers import AllowedTeacherClassroomLevelManager
from classroom.validators import (
    assignment_date_gte_today,
    is_no_of_sem_even,
    pdf_file_size_lt_5mb,
)


User = get_user_model()