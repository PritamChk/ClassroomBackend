from classroom.models.college import Stream
from .common_imports import *

# @shared_task
@receiver(post_save, sender=College)
def create_allowed_teacher(sender, instance: College, created, **kwargs):
    """
    at the time of college creation: reads teacher list from the excel or csv file and creates bulk allowed teacher and send bulk mail
    """
    if created:
        if instance.allowed_teacher_list == None:
            send_mail(
                "Allowed Teacher List Does Not Exists",
                "You Have To Create Allowed Teachers Manually",
                settings.EMAIL_HOST_USER,
                [instance.owner_email_id],
            )
            return None
        file_abs_path = None
        teacher_file_path = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            instance.allowed_teacher_list.name,
        )
        if os.path.exists(teacher_file_path):
            file_abs_path = os.path.abspath(teacher_file_path)
        else:
            send_mail(
                "Allowed Teacher List Does Not Exists",
                "You Have To Create Allowed Teachers Manually",
                settings.EMAIL_HOST_USER,
                [instance.owner_email_id],
            )
            return None

        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df: pd.DataFrame = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)
        else:
            # FIXME: delete college instance & add proper message
            raise ValidationError(
                f"{instance.stream_list.name} is not of type xlsx or csv",
                code=status.HTTP_412_PRECONDITION_FAILED,
            )

        if not "email" in df.columns:
            send_mail(
                "Wrong File Structure",
                """column name should be => 'email',allowed teacher creation skipped.
                   You have to create teachers manually. """,
                settings.EMAIL_HOST_USER,
                [instance.owner_email_id],
            )
            return None
        try:
            list_of_allowed_teacher = [
                AllowedTeacher(college=instance, **args)
                for args in df.to_dict("records")
            ]
            with atomic():
                AllowedTeacher.objects.bulk_create(list_of_allowed_teacher)
        except:
            raise ValidationError(
                detail="Bulk Allowed Teacher Insertion Failed Due to unknown reason",
                code=status.HTTP_304_NOT_MODIFIED,
            )
        email_list = df["email"].to_list()
        subject = "Create Your Teacher Account"
        prompt = "please use your following mail id to sign up in the Classroom[LMS]"
        try:
            send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
        except BadHeaderError:
            print("Could not able to sen emails to students")
        os.remove(file_abs_path)
        College.objects.update(allowed_teacher_list="")


@receiver(post_save, sender=AllowedTeacher)
def send_mail_after_create_allowed_teacher(
    sender, instance: AllowedTeacher, created, **kwargs
):
    """Send mails to manually added allowed teachers

    Args:
        sender (AllowedTeacher): This func. triggers when college DBA manually adds teacher to college
        instance (AllowedTeacher):
        created (bool):
    """
    if created:
        college: College = College.objects.get(pk=instance.college.id)
        subject = "Create Your Teacher Account"
        prompt = f"please use your following mail id - {instance.email} \n to sign up in the Classroom[LMS]"
        try:
            send_mail(subject, prompt, college.owner_email_id, [instance.email])
        except BadHeaderError:
            cprint("Could not able to sen emails to students", "red")


@receiver(post_delete, sender=AllowedTeacher)
def remove_teacher_profile_after_allowed_teacher_deletion(
    sender, instance: AllowedTeacher, **kwargs
):
    """remove teacher profile after allowed teacher deletion

    Args:
        sender (AllowedTeacher): when allowed teacher is removed from the college
        instance (AllowedTeacher):

    Raises:
        ValidationError: when there no teacher profile exists or tries to delete wrong teacher profile

    """
    try:
        teacher_profile = Teacher.objects.select_related("user").filter(
            user__email=instance.email
        )
        if teacher_profile.exists():
            Teacher.objects.filter(
                pk=teacher_profile.get(user__email=instance.email).id
            ).delete()
        # teacher_profile.delete()
        return Response(
            data={"massage": f"{instance.email} has been successfully removed."},
            status=status.HTTP_202_ACCEPTED,
        )
    except:
        raise ValidationError(
            "Either teacher profile does not exists or couldn't able to delete that",
            code=status.HTTP_302_FOUND,
        )


@receiver(post_save, sender=College)
def create_streams_from_file(sender, instance: College, created, **kwargs):
    """Reads stream titles from the given stream file and streams in a bulk"""
    if created:
        if instance.stream_list == None:
            send_mail(
                "Allowed Stream List Does Not Exists",
                "You Have To Create Streams Manually",
                settings.EMAIL_HOST_USER,
                [instance.owner_email_id],  # FIXME: Send mail to session dba
            )
            raise ValidationError(
                detail="Stream List Not Found,Stream have to added manually",
                code=status.HTTP_206_PARTIAL_CONTENT,
            )
        file_abs_path = None
        stream_file_path = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            instance.stream_list.name,
        )
        if os.path.exists(stream_file_path):
            file_abs_path = os.path.abspath(stream_file_path)
        else:
            send_mail(
                "Allowed Stream List Does Not Exists",
                "You Have To Create Streams Manually",
                settings.EMAIL_HOST_USER,
                [instance.owner_email_id],  # FIXME: Send mail to session dba
            )
            raise ValidationError(
                detail="Stream List Not Found,Stream have to added manually",
                code=status.HTTP_206_PARTIAL_CONTENT,
            )

        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df: pd.DataFrame = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)
        else:
            raise ValidationError(
                f"{instance.stream_list.name} is not of type xlsx or csv,Stream have to added manually",
                code=status.HTTP_206_PARTIAL_CONTENT,
            )

        if not "title" in df.columns:
            send_mail(
                "Wrong File Structure",
                "column name should be => 'streams' ",
                settings.EMAIL_HOST_USER,
                [instance.owner_email_id],  # FIXME: Send mail to session dba
            )
            raise ValidationError(
                """
                column name should be => 'streams' without quotation,
                Auto Stream Creation Failed, 
                Streams have to added manually
                """,
                code=status.HTTP_206_PARTIAL_CONTENT,
            )
        list_of_streams = [
            Stream(college=instance, **args) for args in df.to_dict("records")
        ]
        try:
            with atomic():
                Stream.objects.bulk_create(list_of_streams)
        except:
            raise ValidationError(
                detail="Bulk Stream Create Failed Due to unknown reason,Stream have to added manually",
                code=status.HTTP_206_PARTIAL_CONTENT,
            )
        os.remove(file_abs_path)
        College.objects.update(stream_list="")
