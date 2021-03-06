from .imports import *
from django.utils.translation import gettext_lazy as _


class College(models.Model):
    """
    # College
    >  `params`:
    >  ('slug', 'name', 'city', 'state', 'address', 'allowed_teacher_list', 'allowed_dba_list','owner_email_id')
    """

    slug = AutoSlugField(
        populate_from=["name", "state", "city"],
        editable=True,
    )
    name = models.CharField(_("College Name"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    state = models.CharField(_("State"), max_length=255)
    address = models.TextField(null=True, blank=True)
    owner_email_id = models.EmailField(
        _("College Owner DBA Mail [unique]"), unique=True
    )
    stream_list = models.FileField(
        _("Upload Stream List File(.csv/.xl)"),
        upload_to="college/streams/",
        null=True,
        max_length=500,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "xlsx"],
                message="Please Upload CSV/XLSX file only",
            )
        ],
    )
    allowed_teacher_list = models.FileField(
        _("Upload teacher List File(.csv/.xl)"),
        upload_to="classroom/teachers/",
        null=True,
        max_length=500,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["csv", "xlsx"],
                message="Please Upload CSV/XLSX file only",
            )
        ],
    )
    allowed_dba_list = (
        models.FileField(  # TODO: Allowed DBA Auto Create Signal by College
            _("Upload DBA List File(.csv/.xl)"),
            upload_to="college/dbas/%Y/%m/%d",
            null=True,
            max_length=500,
            blank=True,
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["csv", "xlsx"],
                    message="Please Upload CSV/XLSX file only",
                )
            ],
        )
    )

    class Meta:
        ordering = ["name", "city"]

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


class Stream(models.Model):
    title = models.CharField(max_length=255)
    college = models.ForeignKey(
        "classroom.College", on_delete=models.CASCADE, related_name="streams"
    )
    dba = models.ForeignKey(
        "classroom.CollegeDBA",
        on_delete=models.CASCADE,
        related_name="streams",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["college__name", "title"]
        unique_together = ["title", "dba"]

    def __str__(self) -> str:
        return f"{self.title} || Clg: {self.college.name}"
