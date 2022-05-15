from .imports import *
from django.utils.translation import gettext_lazy as _


class CollegeDBA(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="college_dba"
    )
    college = models.OneToOneField(
        "classroom.College",
        on_delete=models.CASCADE,
        related_name="college_dbas",
    )

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} |  {self.user.email} |DBA"

    @admin.display(ordering=["user__email"])
    def get_email(self):
        return self.user.email

    @admin.display(ordering=["user__first_name"])
    def get_first_name(self):
        return self.user.first_name

    @admin.display(ordering=["user__last_name"])
    def get_last_name(self):
        return self.user.last_name
