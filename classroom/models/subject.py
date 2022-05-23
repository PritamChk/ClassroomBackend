from django.utils.translation import gettext_lazy as _
from .imports import *


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
    CP_TEN = 20
    CP_CHOICE = [(i, _(str(i))) for i in range(CP_ONE, CP_TEN + 1)]
    # ----------------------------------------------
    slug = AutoSlugField(
        populate_from=[
            "title",
            "semester__sem_no",
            "subject_type",
            "credit_points",
            "created_by__user__first_name",
            "created_by__user__last_name",
        ]
    )
    subject_code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    subject_type = models.CharField(
        max_length=5, choices=SUBJECT_TYPE_CHOICE, default=THEORY
    )
    credit_points = models.PositiveSmallIntegerField(choices=CP_CHOICE, default=CP_ONE)
    semester = models.ForeignKey(
        "classroom.Semester", on_delete=models.CASCADE, related_name="subjects"
    )
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        "classroom.Teacher", on_delete=models.CASCADE, related_name="subjects"
    )

    class Meta:
        ordering = ["subject_code", "title", "-subject_type"]

    def __str__(self) -> str:
        return f"{self.title} - {self.subject_code}"
