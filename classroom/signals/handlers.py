import os
from celery import shared_task
from classroom.tasks import (
    send_email_after_mass_profile_creation,
    # create_bulk_allowed_teacher,
)

import pandas as pd
from classroom.models import (
    AllowedStudents,
    AllowedTeacher,
    Classroom,
    Semester,
    Student,
    Teacher,
    User,
)
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import BadHeaderError


@receiver(post_save, sender=Classroom)
def create_sems_for_new_classroom(sender, instance: Classroom, **kwargs):
    if kwargs.get("created"):
        sems = [
            Semester(
                classroom=instance,
                sem_no=i + 1,
                is_current_sem=instance.current_sem == i + 1,
            )
            for i in range(instance.no_of_semesters)
        ]
        Semester.objects.bulk_create(sems)


@shared_task
@receiver(post_save, sender=Classroom)
def create_allowed_students(sender, instance: Classroom, **kwargs):
    file_abs_path: os.PathLike = os.path.abspath(instance.allowed_student_list.name)
    df = None
    if str(file_abs_path).split(".")[-1] == "csv":
        df = pd.read_csv(file_abs_path)
    elif str(file_abs_path).split(".")[-1] == "xlsx":
        df = pd.read_excel(file_abs_path)
    else:
        raise FileNotFoundError("File ta nei")  # FIXME: Don't Raise error in frontend
    list_of_students = [
        AllowedStudents(classroom=instance, **args) for args in df.to_dict("records")
    ]
    AllowedStudents.objects.bulk_create(list_of_students)
    # create_bulk_allowed_teacher_or_student.delay(df, instance, AllowedStudents)
    email_list = df["email"].to_list()
    subject = "Create Your Student Account"
    prompt = "please use your following mail id to sign up in the Classroom[LMS]"
    # mails = [
    #     (
    #         subject,
    #         f"{prompt} - \nUSED MAIL ID : {str(m)}",
    #         settings.EMAIL_HOST_USER,
    #         [m],
    #     )
    #     for m in email_list
    # ]
    try:
        send_email_after_mass_profile_creation.delay(subject, prompt, email_list)
        # send_mass_mail(mails, fail_silently=True)
    except BadHeaderError:
        print("Could not able to sen emails to students")
    os.remove(file_abs_path)
    Classroom.objects.update(allowed_student_list="")


@shared_task
@receiver(post_save, sender=Classroom)
def create_allowed_teacher(sender, instance: Classroom, created, **kwargs):
    if created:
        file_abs_path: os.PathLike = os.path.join(
            settings.MEDIA_ROOT, instance.allowed_teacher_list.name
        )#FIXME: Not working on taths pc
        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)
        else:
            raise FileNotFoundError(
                "File ta nei"
            )  # FIXME: Don't Raise error in frontend
        df_dict = df.to_dict("records")
        print(df_dict)
        list_of_teachers = [
            AllowedTeacher(classrooms=instance, **args)
            for args in df.to_dict("records")
        ]
        AllowedTeacher.objects.bulk_create(list_of_teachers)
        # create_bulk_allowed_teacher.delay(df_dict, instance)
        email_list = df["email"].to_list()
        subject = "Create Your Teacher Account"
        prompt = "please use your following mail id to sign up in the Classroom[LMS]"
        # mails = [
        #     (
        #         subject,
        #         f"{prompt} - \nUSED MAIL ID : {m}",
        #         settings.EMAIL_HOST_USER,
        #         [m],
        #     )
        #     for m in email_list
        # ]
        try:
            send_email_after_mass_profile_creation.delay(subject, prompt, email_list)
            # send_mass_mail(mails, fail_silently=True)
        except BadHeaderError:
            print("Could not able to sen emails to students")
        os.remove(file_abs_path)
        Classroom.objects.update(allowed_teacher_list="")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance: settings.AUTH_USER_MODEL, created, **kwargs):
    if created:
        if (
            AllowedStudents.objects.filter(email=instance.email).exists()
            and not Student.objects.select_related("user")
            .filter(user=instance)
            .exists()
        ):
            classroom: Classroom = AllowedStudents.objects.get(
                email=instance.email
            ).classroom
            university_roll = AllowedStudents.objects.get(
                email=instance.email
            ).university_roll
            s = Student.objects.create(
                university_roll=university_roll, user=instance, classroom=classroom
            )
            # TODO:send mail Abcd_1234
            subject = "Your Student Profile Has Been Created Successfully"
            msg = f"""
                Student ID :{s.id}
                mail : {instance.email}
                classroom : {classroom.title}
                
                You Can Login After Activation Of your account
            """
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
        elif (
            AllowedTeacher.objects.filter(email=instance.email).exists()
            and not Teacher.objects.select_related("user")
            .filter(user=instance)
            .exists()
        ):
            t = Teacher.objects.create(user=instance)
            subject = "Your Teacher Profile Has Been Created Successfully"
            msg = f"""
                Teacher ID :{t.id}
                mail : {instance.email}
                
                You Can Login After Activation Of your account
            """
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
        elif instance.is_superuser or instance.is_staff:  # ADMIN
            print("Admin")
        else:
            subject = "Profile Creation Failed"
            msg = f"""
                You have not been assigned any class, but your account has been created.
                So to create a profile contact ADMIN

                contact mail id: {settings.EMAIL_HOST_USER}
            """
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])


@receiver(post_delete, sender=Student)
def delete_user_on_student_delete(sender, instance: Student, **kwargs):
    user = User.objects.filter(pk=instance.user.id)
    if user.exists():
        user.delete()
