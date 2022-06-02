from .common_imports import *


def delete_classroom_on_some_failure(id):
    try:
        College.objects.filter(id=id).delete()
    except:
        cprint("classroom not found", "red")


# @shared_task
@receiver(post_save, sender=Classroom)
def create_sems_for_new_classroom(sender, instance: Classroom, **kwargs):
    if kwargs.get("created"):
        if instance.end_year - instance.start_year >= 2:
            instance.no_of_semesters = (instance.end_year - instance.start_year) * 2
            instance.save(force_update=True)
        sems = [
            Semester(
                classroom=instance,
                sem_no=i + 1,
                is_current_sem=instance.current_sem == i + 1,
            )
            for i in range(instance.no_of_semesters)
        ]
        try:
            Semester.objects.bulk_create(sems)
        except:
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                "Classroom Sem creation Failed Due To Unknown Reason",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# @shared_task
@receiver(post_save, sender=Classroom)
def create_allowed_students(sender, instance: Classroom, created, **kwargs):
    if created:
        if instance.allowed_student_list == None:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                Allowed Student List Does Not Exists
                Classroom Creation Failed
                """,
                code=status.HTTP_404_NOT_FOUND,
            )
            # send_mail(
            #     "Allowed Student List Does Not Exists",
            #     "You Have To Create Allowed Students Manually",
            #     settings.EMAIL_HOST_USER,
            #     ["dba@admin.com"],  # FIXME: Send mail to session dba
            # )
            # return None
        file_abs_path = None
        student_file_path = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            instance.allowed_student_list.name,
        )
        if os.path.exists(student_file_path):
            file_abs_path = os.path.abspath(student_file_path)
        else:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                Allowed Student List Does Not Exists
                Classroom Creation Failed
                """,
                code=status.HTTP_404_NOT_FOUND,
            )

        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)

        if len(df.columns) != 2:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                Classroom Creation Failed.
                Student List should contain 2 columns namely : university_roll & email
                """,
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not df.shape[0] > 0:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                Classroom Creation Failed.
                Student List Cannot be empty
                """,
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not (
            "university_roll" in df.columns and "email" in df.columns
        ):  # TODO:check col name case insensitive
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                Allowed Student List should contain only two columns
                i.e - university_roll & email
                """,
                code=status.HTTP_400_BAD_REQUEST,
            )

        list_of_students = [
            AllowedStudents(classroom=instance, **args)
            for args in df.to_dict("records")
        ]
        try:
            AllowedStudents.objects.bulk_create(list_of_students)
        except:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """Bulk Student Creation Failed, 
                    May be you are trying to add 
                    same student to another class
                """,
                code=status.HTTP_400_BAD_REQUEST,
            )
        email_list = df["email"].to_list()
        subject = "Create Your Student Account"
        prompt = "please use your following mail id to sign up in the Classroom[LMS]"
        try:
            send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
        except BadHeaderError:
            cprint("Could not able to sen emails to students", "blue")
        os.remove(file_abs_path)
        Classroom.objects.update(allowed_student_list="")


@shared_task
@receiver(post_save, sender=Classroom)
def create_allowed_teacher_for_classroom_level(
    sender, instance: Classroom, created, **kwargs
):
    if created:
        if instance.allowed_teacher_list == None:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                Allowed Teacher List Does Not Exists
                Classroom Creation Failed
                """,
                code=status.HTTP_404_NOT_FOUND,
            )
        file_abs_path = None
        dba_file_path = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            instance.allowed_teacher_list.name,
        )
        if os.path.exists(dba_file_path):
            file_abs_path = os.path.abspath(dba_file_path)
        else:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            # finally:
            raise ValidationError(
                """
                Allowed Teacher List Does Not Exists
                Classroom Creation Failed
                """,
                code=status.HTTP_404_NOT_FOUND,
            )

        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df: pd.DataFrame = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)
        else:
            # try:
            #     College.objects.filter(id=instance.id).delete()
            # except:
            #     pass
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                only XL or CSV file format supported.
            """,
                code=status.HTTP_400_BAD_REQUEST,
            )

        if len(df.columns) != 1:
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                f"""
                Allowed Teacher List Should contain only one column named : email
                Classroom Creation Failed
                """,
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not df.shape[0] > 0:
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                f"""
                Allowed Teacher List Can not be Empty
                Classroom Creation Failed
                """,
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not "email" in df.columns:
            delete_classroom_on_some_failure(instance.id)
            raise ValidationError(
                """
                Allowed Teacher List Does Not Contain Column Name : email
                Allowed Teacher Creation Failed
                """,
                code=status.HTTP_400_BAD_REQUEST,
            )
        df_dict: list[dict] = df.to_dict("records")
        # print(df_dict)
        college_allowed_teacher_list = list(
            AllowedTeacher.objects.select_related("college")
            .filter(college=instance.college)
            .values_list("email", flat=True)
        )

        list_of_teachers = []
        rejected_teacher_mails = []
        from termcolor import cprint

        for allowed_teacher in df_dict:
            if allowed_teacher["email"] in college_allowed_teacher_list:
                list_of_teachers.append(
                    AllowedTeacherClassroomLevel(classroom=instance, **allowed_teacher)
                )
                cprint("OUTSIDE OF IF", "yellow")
                if (
                    Teacher.objects.select_related("user")
                    .filter(user__email=allowed_teacher["email"])
                    .exists()
                ):
                    cprint("INSIDE OF IF", "yellow")
                    teacher = Teacher.objects.select_related("user").get(
                        user__email=allowed_teacher["email"]
                    )
                    instance.teachers.add(teacher)
                    instance.save(force_update=True)
                    for tchr in instance.teachers.all():
                        cprint("Classrooms of teachers -> ", "cyan")
                        cprint(tchr, "cyan")
                # AllowedTeacherClassroomLevel.objects.create(
                #     classroom=instance, **allowed_teacher
                # )
            else:
                rejected_teacher_mails.append(allowed_teacher["email"])
        if len(rejected_teacher_mails) > 0:
            send_mail(
                "Some Teacher's don't belong to the college",
                f"""
                Please add this teachers to college first and 
                then add to CLASSROOM.
                Rejected teacher list : {rejected_teacher_mails}
                """,
                settings.EMAIL_HOST_USER,
                ["tmsl@owner.com"],
                "",
            )
        try:
            AllowedTeacherClassroomLevel.objects.bulk_create(list_of_teachers)
        except:
            delete_classroom_on_some_failure(instance.id)
            ValidationError(
                "Bulk Allowed Teacher Add for Classroom Failed",
                code=status.HTTP_400_BAD_REQUEST,
            )
        email_list = df["email"].to_list()
        subject = "Teacher Account Associated With Classroom"
        prompt = (
            "please use your following mail id to sign up/log in in the Classroom[LMS]"
        )
        try:
            send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
        except BadHeaderError:
            cprint("Could not able to send emails to students", "red")
        os.remove(file_abs_path)
        Classroom.objects.update(allowed_teacher_list="")


@receiver(post_save, sender=AllowedTeacherClassroomLevel)
def create_allowed_teacher_for_classroom_level_with_check(
    sender, instance: AllowedTeacherClassroomLevel, created, **kwargs
):
    if created:
        is_email_in_allowed_teacher_list = AllowedTeacher.objects.filter(
            email=instance.email
        )
        if not is_email_in_allowed_teacher_list.exists():
            try:
                AllowedTeacherClassroomLevel.objects.filter(
                    email=instance.email
                ).delete()
            except:
                cprint("this teacher email does not associated with any college", "red")
            raise ValidationError(
                "this teacher email does not associated with any college",
                code=status.HTTP_400_BAD_REQUEST,
            )
        classroom: Classroom = Classroom.objects.get(pk=instance.classroom.id)
        subject = f"Teacher Account Associated With Classroom-{classroom.title}"
        prompt = f"""
            please use your following mail id to sign up
            /log in in the Classroom[LMS]
                - {instance.email} 
            """
        send_mail(subject, prompt, classroom.college.owner_email_id, [instance.email])


@receiver(post_save, sender=AllowedStudents)
def send_mail_to_new_allowed_student(
    sender, instance: AllowedStudents, created, **kwargs
):
    subject = f"Welcome to Classroom - {instance.classroom.title}"
    body = f"""
        Welcome - {instance.email}
        University Roll - {instance.university_roll}
        Please Sign Up to join the classroom
        & update your contact number after login
    """
    try:
        college: College = College.objects.prefetch_related("classrooms").get(
            classrooms=instance.classroom
        )
        send_mail(subject, body, college.owner_email_id, [instance.email])
    except:
        cprint(
            f"{instance.email} - did not received any confirmation mail from classroom admin",
            "red",
        )

    # pass
