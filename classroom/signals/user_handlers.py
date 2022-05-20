from .common_imports import *


# @shared_task
@receiver(post_delete, sender=Student)
def delete_user_on_student_delete(sender, instance: Student, **kwargs):
    user = User.objects.filter(pk=instance.user.id)
    if user.exists():
        user.delete()


# @shared_task
@receiver(post_delete, sender=CollegeDBA)
def delete_user_on_dba_delete(sender, instance: CollegeDBA, **kwargs):
    user = User.objects.filter(pk=instance.user.id)
    if user.exists():
        user.delete()


# @shared_task
@receiver(
    post_delete, sender=Teacher
)  # FIXME: Off this code if teacher removal from class deletes user
def delete_user_on_teacher_delete(sender, instance: Teacher, **kwargs):
    if instance.user:
        user = User.objects.filter(pk=instance.user.id)
        if user.exists():
            user.delete()
