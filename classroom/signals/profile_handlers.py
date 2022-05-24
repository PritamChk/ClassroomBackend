from .common_imports import *


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
            # TODO: Add some other info also in the mail
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
            college_detail = College.objects.get(
                pk=(
                    AllowedTeacher.objects.filter(email=instance.email)
                    .select_related("college")
                    .values_list("college", flat=True)
                )[0]
            )
            from termcolor import cprint

            cprint(college_detail, "red")
            t = Teacher.objects.create(user=instance, college=college_detail)
            subject = "Your Teacher Profile Has Been Created Successfully"
            msg = f"""
                Teacher ID :{t.id}
                mail : {instance.email}

                You Can Login After Activation Of your account
            """
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
        elif (
            AllowedCollegeDBA.objects.filter(email=instance.email).exists()
            and not CollegeDBA.objects.select_related("user")
            .filter(user=instance)
            .exists()
        ):
            from termcolor import cprint

            # cprint("In DBA Creation", "red")
            college_detail: College = College.objects.get(
                pk=(
                    AllowedCollegeDBA.objects.filter(email=instance.email)
                    .select_related("college")
                    .values_list("college", flat=True)
                )[0]
            )

            # cprint(college_detail, "red")
            is_owner = False
            if instance.email == college_detail.owner_email_id:
                is_owner = True
            # cprint(f"is owner --> [ {is_owner} ]", "red")
            t: CollegeDBA = CollegeDBA.objects.create(
                user=instance, college=college_detail, is_owner=is_owner
            )
            subject = "Your DBA Profile Has Been Created Successfully"
            msg = f"""
                COLLEGE DBA ID :{t.id}
                mail : {instance.email}

                You Can Login After Activation Of your account
            """
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
        elif instance.is_superuser or instance.is_staff:  # ADMIN
            print("Admin")
        else:
            subject = "Profile Creation Failed"
            msg = f"""
                You have not been assigned any profile for any college

                contact mail id: {settings.EMAIL_HOST_USER}
            """
            # FIXME: Delete below line of code if gives error
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [instance.email])
            # User.objects.filter(pk=instance.id).delete()
            raise ValidationError(
                "Profile creation failed, as you have no profile attached with any college",
                code=status.HTTP_401_UNAUTHORIZED,
            )
