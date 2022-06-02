from .common_imports import *


# @shared_task
@receiver(post_delete, sender=Student)
def delete_user_on_student_delete(sender, instance: Student, **kwargs):
    try:
        user = User.objects.filter(pk=instance.user.id)
        if user.exists():
            user.delete()
            try:
                subject = "You Have Been Removed from Classroom"
                body = f"""
                    your mail - {instance.user.email} is no more associated with any college or classroom
                """
            except:
                cprint(
                    "student profile deletion confirmation mail sending failed", "red"
                )
    except:
        pass


# @shared_task
@receiver(post_delete, sender=CollegeDBA)
def delete_user_on_dba_delete(sender, instance: CollegeDBA, **kwargs):
    try:
        user = User.objects.filter(pk=instance.user.id)
        if user.exists():
            user.delete()
            try:
                subject = "Your DBA Profile Have Been Removed from College"
                body = f"""
                    your mail - {instance.user.email} is no more associated with any college or classroom
                """
            except:
                cprint("admin profile deletion confirmation mail sending failed", "red")
    except:
        pass


# @shared_task
@receiver(
    post_delete, sender=Teacher
)  # FIXME: Off this code if teacher removal from class deletes user
def delete_user_on_teacher_delete(sender, instance: Teacher, **kwargs):
    try:
        if instance.user:
            user = User.objects.filter(pk=instance.user.id)
            if user.exists():
                user.delete()
                try:
                    subject = "Your Teacher Profile Have Been Removed from College"
                    body = f"""
                        your mail - {instance.user.email} is no more associated with any college or classroom
                    """
                except:
                    cprint(
                        "teacher profile deletion confirmation mail sending failed",
                        "red",
                    )
    except:
        pass
