from .imports import *
from django.utils.translation import gettext_lazy as _


class Announcement(models.Model):
    heading = models.TextField(_("Heading"), default="No Heading Given")
    body = models.TextField(_("Description[Optional] "), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At "), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At "), auto_now=True)
    subject = models.ForeignKey(
        "classroom.Subject", on_delete=models.CASCADE, related_name="announcements"
    )
    posted_by = models.ForeignKey(
        "classroom.Teacher", on_delete=models.CASCADE, related_name="announcements"
    )

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self) -> str:
        return f"{self.heading}"

    def heading_short(self):
        return f"{self.heading[:10]}..."
