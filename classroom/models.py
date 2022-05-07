from datetime import date
from random import randint
from uuid import uuid4

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

# from classroom.managers import ClassroomManager

User = get_user_model()


class College(models.Model):
    slug = AutoSlugField(
        populate_from=["name", "state", "city"],
        editable=True,
    )
    name = models.CharField(_("College Name"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    state = models.CharField(_("State"), max_length=255)
    address = models.TextField(null=True, blank=True)
    # classrooms
    class Meta:
        ordering = ["name", "city", "state"]

    def __str__(self) -> str:
        return self.name


class Classroom(models.Model):
    # objects = ClassroomManager.as_manager() #FIXME: won't work
    slug = AutoSlugField(
        populate_from=[
            "title",
            "level",
            "stream",
            "section",
            "start_year",
            "end_year",
            "college",
        ],
        editable=True,
    )
    title = models.CharField(_("Classroom Name"), max_length=255, null=True, blank=True)
    level = models.CharField(
        _("Level"),
        max_length=40,
        help_text="e.g - UG/PG/MASTERS",
    )
    stream = models.CharField(
        _("Your Stream"),
        max_length=255,
    )
    start_year = models.PositiveSmallIntegerField(
        _("Starting Year"),
        # default=2022,
        default=date.today().year - 2,
        db_index=True,
        help_text="Write your session starting year (e.g. - 2020)",
        validators=[
            MinValueValidator(2000, "You can't select year less than 2000"),
            MaxValueValidator(
                (date.today().year + 1),  # FIXME: Make this dynamic
                # 2023,
                "Max Year Can be selected only 1 year ahead of current year",
            ),
        ],
    )
    end_year = models.PositiveSmallIntegerField(
        _("Ending Year"),
        db_index=True,
        default=date.today().year,
        help_text="Write your session ending year (e.g. - 2020)",
        validators=[
            MinValueValidator(2000, "You can't select year less than 2000"),
            MaxValueValidator(
                (2200),  # FIXME: Make this dynamic
                "Max Year Can be selected only 1 year ahead of current year",
            ),
        ],
    )
    section = models.CharField(
        _("Section(optional)"),
        max_length=10,
        null=True,
        blank=True,
        default="A",
    )
    no_of_semesters = models.PositiveSmallIntegerField(
        _("Number of Sem"),
        default=4,
        validators=[
            MinValueValidator(4, "Min Course Duration is of 2 Years(4 semesters)"),
            MaxValueValidator(14),
        ],
    )
    current_sem = models.PositiveSmallIntegerField(
        _("On Going Sem"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(14),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="classrooms"
    )
    allowed_student_list = models.FileField(
        _("Upload student List File(.csv)"),
        # null=,
        # blank=True,
        upload_to="classroom/students/",
        default="",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "xlsx"],
                message="Please Upload CSV/XLSX file only",
            )
        ],
    )
    allowed_teacher_list = models.FileField(
        _("Upload teacher List File(.csv)"),
        upload_to="classroom/teachers/",
        # null=True,
        # blank=True,
        default="",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "xlsx"],
                message="Please Upload CSV/XLSX file only",
            )
        ],
    )

    class Meta:
        unique_together = [
            "level",
            "stream",
            "start_year",
            "end_year",
            "section",
            "college",
        ]

    def __str__(self) -> str:
        return self.title


class Semester(models.Model):
    #TODO:Introduce Slug for Sem
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="semesters"
    )
    sem_no = models.PositiveSmallIntegerField(
        _("Semester No"),
        # editable=False,
        validators=[
            MinValueValidator(1, "sem value > 0"),
            MaxValueValidator(14, "sem value < 15"),
        ],
    )
    is_current_sem = models.BooleanField(_("is this sem going on? "), default=False)

    class Meta:
        unique_together = ["classroom", "sem_no"]


class Teacher(models.Model):
    """
    # Teacher
    ----
        -  user : FKey to User()
        -  classroom : m2m classroom
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="teacher_profile",
    )
    classroom = models.ManyToManyField(Classroom, related_name="teachers", blank=True)


class Student(models.Model):
    """
    ## `Student`
    ---
        - user: takes User()
        - classroom: takes User()
    """

    university_roll = models.PositiveBigIntegerField(
        _("University Roll"),
        help_text="Your University Roll No - (e.g. - 13071020030)",
        null=True,
        blank=False,
        default=randint(10,9999999)
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_profile",
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self) -> str:
        return f"{self.id}"

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    @admin.display(ordering="classroom__college__name")
    def college_name(self):
        return self.classroom.college.name


class AllowedTeacher(models.Model):
    email = models.EmailField(_("Email Id"), max_length=255)
    classrooms = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="allowed_teachers"
    )

    def __str__(self) -> str:
        return f"{self.email}"


class AllowedStudents(models.Model):
    email = models.EmailField(_("Email Id"), max_length=255)
    university_roll = models.PositiveBigIntegerField(
        _("University Roll"),
        help_text="Your University Roll No - (e.g. - 13071020030)",
    )
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="allowed_students"
    )

    class Meta:
        unique_together = [
            ("university_roll", "classroom"),
            ("university_roll", "email"),
            ("classroom", "email"),
        ]
        verbose_name_plural = "Allowed Students"

    def __str__(self) -> str:
        return f"{self.email} || {self.university_roll}"
