from django.db import models
from django.db.models.signals import post_save


class AllowedTeacherClassroomLevelManager(models.Manager):
    def delete(self):
        return super().delete()

    def bulk_create(self, objs, **kwargs):
        a = super(models.Manager, self).bulk_create(objs, **kwargs)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True)
        return a
