from .imports import *
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta


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
        upload_to="classroom/assignments/",
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
        default=now,
        validators=[assignment_date_gte_today],
    )
    due_time = models.TimeField(_("Due time"), default=now)
    subject = models.ForeignKey(
        "classroom.Subject", on_delete=models.CASCADE, related_name="assignments"
    )
    given_by = models.ForeignKey(
        "classroom.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        related_name="assignments_given",
    )

    created_at = models.DateTimeField(
        _("Created At "), auto_now_add=True, editable=False
    )

    class Meta:
        ordering = ["due_date", "due_time", "alloted_marks", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def file_path(self):
        return self.attached_pdf.name

    def short_description(self) -> str:
        return self.description[:30]


class SubmittedAssignment(models.Model):
    # FK to assignment
    assignment = models.ForeignKey(
        "classroom.Assignment", on_delete=models.CASCADE, related_name="submissions"
    )
    # ----------------FOR STUDENT ----------------------------------------------
    submitted_by = models.ForeignKey(
        "classroom.Student",
        on_delete=models.CASCADE,
        related_name="attempted_assignments",
    )
    answer_section = models.TextField(null=True, blank=True)
    submitted_file = models.FileField(
        _("Upload File Here📁"),
        null=True,
        blank=True,
        max_length=500,
        upload_to=f"classroom/assignment_submissions/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"],
                message="Please Upload PDF file only",
            ),
            pdf_file_size_lt_5mb,
        ],
    )
    is_submitted = models.BooleanField(_("submitted : "), default=False)
    submission_date = models.DateField(auto_now_add=True, editable=False)
    submission_time = models.TimeField(auto_now_add=True, editable=False)

    # ------------- FOR TEACHER Control -------------
    score = models.IntegerField(
        _("0<=x<=100"),
        default=0,
        validators=[
            MinValueValidator(0, "Score should be >= 0"),
            MaxValueValidator(
                100,
                "score should be <= 100",
            ),
        ],
    )
    has_scored = models.BooleanField(_("Scored by teacher : "), default=False)
    remarks = models.TextField(_("remarks"), blank=True, null=True, max_length=400)
    scored_by = models.ForeignKey(
        "classroom.Teacher",
        on_delete=models.SET_NULL,
        related_name="scored_assignments",
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = [["assignment", "submitted_by"]]
        ordering = ["-submission_date", "-submission_time", "-score"]

    def __str__(self) -> str:
        return self.submitted_by
