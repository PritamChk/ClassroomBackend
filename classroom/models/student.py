from .imports import *
from django.utils.translation import gettext_lazy as _


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
        "classroom.Classroom",
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
