from .imports import *
from django.utils.translation import gettext_lazy as _


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
    email = models.EmailField(_("Email Id"), max_length=255, unique=True)
    college = models.ForeignKey(
        "classroom.College", on_delete=models.CASCADE, related_name="allowed_teachers"
    )

    def __str__(self) -> str:
        return f"{self.email}"


class AllowedCollegeDBA(models.Model):
    email = models.EmailField(_("Email Id"), max_length=255, unique=True)
    college = models.ForeignKey(
        "classroom.College", on_delete=models.CASCADE, related_name="allowed_dbas"
    )

    def __str__(self) -> str:
        return f"{self.email}"
