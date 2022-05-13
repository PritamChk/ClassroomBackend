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


class College(models.Model):
    slug = AutoSlugField(
        populate_from=["name", "state", "city"],
        editable=True,
    )
    name = models.CharField(_("College Name"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    state = models.CharField(_("State"), max_length=255)
    address = models.TextField(null=True, blank=True)
    # TODO: send signal by college instead of Classroom
    allowed_teacher_list = models.FileField(
        _("Upload teacher List File(.csv/.xl)"),
        upload_to=f"{settings.MEDIA_ROOT}/classroom/teachers/",
        # default=f"{settings.BASE_DIR}/{settings.MEDIA_ROOT}/classroom/teacher/no_file_of_teacher.csv",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "xlsx"],
                message="Please Upload CSV/XLSX file only",
            )
        ],
    )

    class Meta:
        ordering = ["name", "city", "state"]

    def __str__(self) -> str:
        return f"{self.name} - {self.city}"


class AllowedTeacher(models.Model):
    email = models.EmailField(_("Email Id"), max_length=255)
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="allowed_teachers"
    )

    def __str__(self) -> str:
        return f"{self.email}"


class Teacher(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        related_name="teacher_profile",
    )
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name="teachers"
    )
    # classroom = models.ManyToManyField(
    #     "Classroom", related_name="teachers", blank=True
    # )  # TODO: Add this after classroom table created

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} |  {self.user.email} "

    @admin.display(ordering=["user__email"])
    def get_email(self):
        return self.user.email

    @admin.display(ordering=["user__first_name"])
    def get_first_name(self):
        return self.user.first_name

    @admin.display(ordering=["user__last_name"])
    def get_last_name(self):
        return self.user.last_name


class Classroom(models.Model):
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
    )
    title = models.CharField(_("Classroom Name"), max_length=255, null=True, blank=True)
    level = models.CharField(
        _("Level"),
        max_length=40,
        choices=LEVEL_CHOICES.choices,
        default=LEVEL_CHOICES.UnderGraduate,
        help_text="e.g - Masters/Bachelors",
    )
    stream = models.CharField(
        _("Your Stream"),
        max_length=255,
    )  # TODO: Make Drop Down
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
        choices=SECTION_CHOICES.choices,
        default=SECTION_CHOICES.A,
    )
    no_of_semesters = models.PositiveSmallIntegerField(
        _("Number of Sem"),
        default=4,
        validators=[
            MinValueValidator(4, "Min Course Duration is of 2 Years(4 semesters)"),
            MaxValueValidator(14),
            is_no_of_sem_even,
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
        _("Upload Student List File(.csv/xl)"),
        null=True,
        blank=True,
        upload_to=f"{settings.MEDIA_ROOT}/classroom/students/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "xlsx"],
                message="Please Upload CSV/XLSX file only",
            )
        ],
    )
    teachers = models.ManyToManyField(
        Teacher, related_name="classrooms", blank=True, editable=False
    )
    # TODO: use this to add teachers in classrooms and vice-versa
    allowed_teacher_list = models.FileField(
        _("Upload Teacher List File(.csv/xl)"),
        upload_to=f"{settings.MEDIA_ROOT}/classroom/teachers/",
        null=True,
        blank=True,
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
        ordering = [
            "college__name",
            "level",
            "-start_year",
            "-end_year",
            "section",
            "stream",
        ]

    def __str__(self) -> str:
        return self.title


class AllowedTeacherClassroomLevel(models.Model):
    objects = AllowedTeacherClassroomLevelManager()
    email = models.EmailField(_("Email Id"), max_length=255)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="allowed_teachers"
    )

    def __str__(self) -> str:
        return f"{self.email}"


class Semester(models.Model):
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
        ordering = ["classroom__title", "sem_no"]

    def __str__(self) -> str:
        return str(self.sem_no)

    @admin.display(ordering=["classroom__title"])
    def classroom_name(self):
        return self.classroom.title


class Student(models.Model):

    university_roll = models.PositiveBigIntegerField(
        _("University Roll"),
        help_text="Your University Roll No - (e.g. - 13071020030)",
        null=True,
        blank=True,
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

    @admin.display(ordering=["user__email"])
    def get_email(self):
        return self.user.email

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    @admin.display(ordering="classroom__college__name")
    def college_name(self):
        return self.classroom.college.name


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
        ordering = ["university_roll"]
        verbose_name_plural = "Allowed Students"

    def __str__(self) -> str:
        return f"{self.email} || {self.university_roll}"

    @admin.display(ordering=["classroom__title"])
    def get_classroom_name(self):
        return self.classroom.title


class Subject(models.Model):
    """
    # Subject belongs to semester
        - **slug** will be used as filter key
        - **subject_code** is [`optional`]
        - **title** is required
        - **subject_type** is required [Practical/Theory/Elective]
        - **credit_points** [`optional`] type: positive small integer
        - **credit_points** [`optional`] type: positive small integer
    """

    # --------------Choice Fields------------------
    THEORY = "TH"
    PRACTICAL = "PRC"
    ELECTIVE = "ELC"
    PROJECT = "PRJ"
    SUBJECT_TYPE_CHOICE = [
        (THEORY, _("Theory")),
        (PRACTICAL, _("Practical")),
        (ELECTIVE, _("Elective")),
        (PROJECT, _("Project")),
    ]
    CP_ONE = 1
    CP_TEN = 15
    CP_CHOICE = [(i, _(str(i))) for i in range(CP_ONE, CP_TEN + 1)]
    # ----------------------------------------------
    slug = AutoSlugField(
        populate_from=[
            "title",
            "semester__sem_no",
            "subject_type",
            "credit_points",
            "created_by",
        ]
    )
    subject_code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    subject_type = models.CharField(
        max_length=5, choices=SUBJECT_TYPE_CHOICE, default=THEORY
    )
    credit_points = models.PositiveSmallIntegerField(choices=CP_CHOICE, default=CP_ONE)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="subjects"
    )
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="subjects"
    )

    class Meta:
        ordering = ["-created_at", "title", "-credit_points"]

    def __str__(self) -> str:
        return f"{self.title} - {self.subject_code}"


class Announcement(models.Model):
    heading = models.TextField(_("Heading"), default="No Heading Given")
    body = models.TextField(_("Description[Optional] "), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At "), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At "), auto_now=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="announcements"
    )
    posted_by = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="announcements"
    )

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self) -> str:
        return f"{self.heading}"

    def heading_short(self):
        return f"{self.heading[:10]}..."


class Notes(models.Model):
    slug = AutoSlugField(
        populate_from=["title", "subject__title", "posted_by__user__first_name"]
    )
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description[optional]"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At "), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At "), auto_now=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="notes")
    posted_by = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, related_name="created_notes", null=True
    )

    class Meta:
        verbose_name_plural = "Notes"
        ordering = ["title", "-created_at"]

    def __str__(self) -> str:
        return self.title

    @admin.display(ordering="description")
    def short_description(self):
        return self.description[:40]


class NotesAttachmentFile(models.Model):
    title = AutoSlugField(
        populate_from=["notes__title", "notes__subject__title", "created_at"],
    )
    file_path = models.FileField(
        _("Upload File Here"),
        null=True,
        blank=True,
        max_length=400,
        upload_to=f"{settings.MEDIA_ROOT}/classroom/notes/%Y/%m/%d",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["xlsx", "pdf", "doc"],
                message="Please Upload XLSX/PDF/Doc file only",
            )
        ],
    )
    created_at = models.DateTimeField(_("Created At "), auto_now_add=True)
    notes = models.ForeignKey(
        Notes, on_delete=models.CASCADE, related_name="attached_files"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return str(self.file_path.name)


class Assignment(models.Model):
    title = models.CharField(_("Assignment Title"), max_length=300)
    description = models.TextField(null=True, blank=True)
    alloted_marks = models.PositiveSmallIntegerField(
        _("Marks:"),
        default=100,
        validators=[
            MaxValueValidator(100, "assignments can't be alloted more than 100 marks 😑")
        ],
    )
    attached_pdf = models.FileField(
        _("Upload File Here📁"),
        null=True,
        blank=True,
        max_length=500,
        upload_to=f"{settings.MEDIA_ROOT}/classroom/assignments/%Y/%m/%d",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"],
                message="Please Upload PDF file only",
            ),
            pdf_file_size_lt_5mb,
        ],
    )
    due_date = models.DateField(
        _("Due by"),
        default=(date.today() + timedelta(days=1)),
        validators=[assignment_date_gte_today],
    )
    due_time = models.TimeField(_("Due time"), default=datetime.now())
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="assignments"
    )
    given_by = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name="assignments_given"
    )

    created_at = models.DateTimeField(
        _("Created At "), auto_now_add=True, editable=False
    )

    class Meta:
        ordering = ["due_date", "due_time", "alloted_marks", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def file_path(self):
        return self.attached_pdf

    def short_description(self) -> str:
        return self.description[:30]


# class SubmittedAssignment(models.Model):
#     # FK to assignment
#     assignment = models.ForeignKey(
#         Assignment, on_delete=models.CASCADE, related_name="submissions"
#     )
#     # ----------------FOR STUDENT ----------------------------------------------
#     submitted_by = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="attempted_assignments"
#     )
#     answer_section = models.TextField(null=True, blank=True)
#     submitted_file = models.FileField(
#         _("Upload File Here📁"),
#         null=True,
#         blank=True,
#         max_length=500,
#         upload_to=f"{settings.MEDIA_ROOT}/classroom/assignment_submitions/%Y/%m/%d",
#         validators=[
#             FileExtensionValidator(
#                 allowed_extensions=["pdf"],
#                 message="Please Upload PDF file only",
#             ),
#             pdf_file_size_lt_5mb,
#         ],
#     )
#     is_submitted = models.BooleanField(_("submitted : "), default=False)
#     submission_time = models.DateTimeField(auto_now_add=True, editable=False)

#     # ------------- FOR TEACHER Control -------------
#     score = models.IntegerField(
#         _("0<=x<=100"),
#         default=0,
#         validators=[
#             MinValueValidator(0, "Score should be >= 0"),
#             MaxValueValidator(
#                 100,
#                 "score should be <= 100",
#             ),
#         ],
#     )
#     has_scored = models.BooleanField(_("Scored by teacher : "), default=False)
#     remarks = models.TextField(_("remarks"), blank=True, null=True, max_length=400)
#     scored_by = models.ForeignKey(
#         Teacher,
#         on_delete=models.SET_NULL,
#         related_name="scored_assignments",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         unique_together = [["assignment", "submitted_by"]]
#         ordering = ["-submission_time", "-score"]
