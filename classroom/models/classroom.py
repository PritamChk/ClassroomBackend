from .imports import *
from django.utils.translation import gettext_lazy as _


class Classroom(models.Model):
    slug = AutoSlugField(
        populate_from=[
            "title",
            "level",
            "stream",
            "section",
            "start_year",
            "end_year",
            "college__name",
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
        "classroom.College", on_delete=models.CASCADE, related_name="classrooms"
    )
    allowed_student_list = models.FileField(
        _("Upload Student List File(.csv/xl)"),
        null=True,
        blank=True,
        upload_to=f"classroom/students/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "xlsx"],
                message="Please Upload CSV/XLSX file only",
            )
        ],
    )
    teachers = models.ManyToManyField(
        "classroom.Teacher", related_name="classrooms", blank=True, editable=False
    )
    # TODO: use this to add teachers in classrooms and vice-versa
    allowed_teacher_list = models.FileField(
        _("Upload Teacher List File(.csv/xl)"),
        upload_to=f"classroom/teachers/",
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
        return str(self.id)


class Semester(models.Model):
    classroom = models.ForeignKey(
        "classroom.Classroom", on_delete=models.CASCADE, related_name="semesters"
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


class AllowedTeacherClassroomLevel(models.Model):
    objects = AllowedTeacherClassroomLevelManager()
    email = models.EmailField(_("Email Id"), max_length=255)
    classroom = models.ForeignKey(
        "classroom.Classroom", on_delete=models.CASCADE, related_name="allowed_teachers"
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
        "classroom.Classroom", on_delete=models.CASCADE, related_name="allowed_students"
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
