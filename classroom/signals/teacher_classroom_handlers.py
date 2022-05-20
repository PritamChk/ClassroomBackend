from .common_imports import *


@shared_task
@receiver(post_save, sender=Teacher)
def auto_join_teacher_to_classes(sender, instance: Teacher, created, **kwargs):
    # from termcolor import cprint

    if created:
        qset = Classroom.objects.prefetch_related("allowed_teachers").filter(
            allowed_teachers__email=instance.user.email
        )
        # cprint(list(qset), "blue")
        try:
            instance.classrooms.add(*qset)
        except:
            pass
            # cprint("already assigned classrooms to teacher ", "yellow")


@receiver(
    post_save, sender=AllowedTeacherClassroomLevel
)  # FIXME: classroom pre signed up teachers are not saving
def assign_classroom_to_existing_teacher(
    sender, instance: AllowedTeacherClassroomLevel, created, **kwargs
):
    from termcolor import cprint

    t = (
        "assign_classroom_to_existing_teacher "
        + instance.email
        + "\n---> "
        + str(created)
    )
    cprint(t, "red")
    if created:
        classroom: Classroom = Classroom.objects.select_related("college").get(
            pk=instance.classroom.id
        )
        cprint(classroom, "red")
        teacher_query = Teacher.objects.select_related("user").filter(
            user__email=instance.email
        )
        cprint(str(teacher_query.exists()) + " -> " + instance.email, "blue")
        if teacher_query.exists():
            teacher = teacher_query.first()
            from django.db import transaction

            with transaction.atomic():
                classroom.teachers.add(teacher)
                classroom.save(force_update=True)
            for tchr in classroom.teachers.all():
                cprint("Classrooms of teacher -> ", "cyan")
                cprint(tchr, "cyan")
            owner_mail_id = classroom.college.owner_email_id
            cprint(f"owner mail id --> {owner_mail_id}", "red")
            subject = "Sir You have been Assigned A new Class"
            msg = f"Classroom - {classroom.title}"
            send_mail(subject, msg, owner_mail_id, [instance.email])


@shared_task
@receiver(post_delete, sender=AllowedTeacherClassroomLevel)
def remove_class_after_removal_of_assigned_teacher(
    sender, instance: AllowedTeacherClassroomLevel, **kwargs
):
    """
    this removes the classroom from the teacher if teacher
    has been removed from allowed class room level
    """
    classroom: Classroom = Classroom.objects.select_related("college").get(
        pk=instance.classroom.id
    )
    teacher_query = Teacher.objects.select_related("user").filter(
        user__email=instance.email
    )
    if teacher_query.exists():
        teacher_query.first().classrooms.remove(classroom)
        subject = "Sir You have been Removed From A Class"
        msg = f"Classroom - {classroom.title}"
        owner_mail_id = classroom.college.owner_email_id
        cprint(f"owner mail id --> {owner_mail_id}", "red")
        send_mail(subject, msg, owner_mail_id, [instance.email])
