from .imports import *
from django.utils.translation import gettext_lazy as _


class Notes(models.Model):
    slug = AutoSlugField(
        populate_from=["title", "subject__title", "posted_by__user__first_name"]
    )
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description[optional]"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At "), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At "), auto_now=True)
    subject = models.ForeignKey(
        "classroom.Subject", on_delete=models.CASCADE, related_name="notes"
    )
    posted_by = models.ForeignKey(
        "classroom.Teacher",
        on_delete=models.SET_NULL,
        related_name="created_notes",
        null=True,
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
        "classroom.Notes", on_delete=models.CASCADE, related_name="attached_files"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return str(self.file_path.name)
