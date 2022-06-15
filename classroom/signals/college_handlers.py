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
            delete_college_on_any_failure(instance.id)
            ValidationError(
                """
            Allowed Teacher List Does Not Exists. College Creation Failed
            """,
                code=status.HTTP_400_BAD_REQUEST,
            )
        file_abs_path = None
        teacher_file_path = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            instance.allowed_teacher_list.name,
        )
        if os.path.exists(teacher_file_path):
            file_abs_path = os.path.abspath(teacher_file_path)
        else:
            delete_college_on_any_failure(instance.id)
            ValidationError(
                """
            Allowed Teacher List Does Not Exists. College Creation Failed
            """,
                code=status.HTTP_400_BAD_REQUEST,
            )

        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df: pd.DataFrame = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)
        else:
            # FIXME: delete college instance & add proper message
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.allowed_teacher_list.name} is not of type xlsx or csv",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if df.shape[1] != 1:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.allowed_teacher_list.name} file should contain ONE Column namely email",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not df.shape[0] > 0:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.allowed_teacher_list.name} file can not be empty",
                code=status.HTTP_400_BAD_REQUEST,
            )

        if not "email" in df.columns:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                """
                Wrong File Structure
                column name should be => 'email',allowed teacher creation skipped.
                College Creation Failed""",
                code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            list_of_allowed_teacher = [
                AllowedTeacher(college=instance, **args)
                for args in df.to_dict("records")
            ]
            with atomic():
                AllowedTeacher.objects.bulk_create(list_of_allowed_teacher)
        except:
            delete_college_on_any_failure(instance.id)
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
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                detail="Stream List Not Found,College Creation Failed",
                code=status.HTTP_400_BAD_REQUEST,
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
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                detail="Stream List Not Found,College Creation Failed",
                code=status.HTTP_400_BAD_REQUEST,
            )

        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df: pd.DataFrame = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)
        else:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.stream_list.name} is not of type xlsx or csv,Stream have to added manually",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if df.shape[1] != 1:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.stream_list.name} file should contain ONE Column namely title",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not df.shape[0] > 0:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.stream_list.name} file can not be empty",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not "title" in df.columns:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.stream_list.name} file should contain ONE Column namely title",
                code=status.HTTP_400_BAD_REQUEST,
            )
        list_of_streams = [
            Stream(college=instance, **args) for args in df.to_dict("records")
        ]
        try:
            with atomic():
                Stream.objects.bulk_create(list_of_streams)
        except:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                detail="Bulk Stream Create Failed Due to unknown reason, College Creation Failed",
                code=status.HTTP_400_BAD_REQUEST,
            )
        os.remove(file_abs_path)
        College.objects.update(stream_list="")


# @receiver(pre_save, sender=College)
# def validate_all_file_formats_and_data(sender, instance: College, **kwargs):
#     """
#     checks teacher , dba and stream list files if they are in correct format
#     """
#     # 1. check streams first
#     # if instance.stream_list == None:
#     #     raise ValidationError(
#     #         detail="Stream List Not Found",
#     #         code=status.HTTP_404_NOT_FOUND,
#     #     )
#     # file_abs_path = None
#     # stream_file_path = os.path.join(
#     #     settings.BASE_DIR,
#     #     settings.MEDIA_ROOT,
#     #     instance.stream_list.name,
#     # )
#     # if os.path.exists(stream_file_path):
#     #     file_abs_path = os.path.abspath(stream_file_path)
#     # else:
#     #     raise ValidationError(
#     #         detail="Stream List Not Found, Or Corrupted",
#     #         code=status.HTTP_404_NOT_FOUND,
#     #     )

#     df = None
#     if str(file_abs_path).split(".")[-1] == "csv":
#         df: pd.DataFrame = pd.read_csv(file_abs_path)
#     elif str(file_abs_path).split(".")[-1] == "xlsx":
#         df = pd.read_excel(file_abs_path)
#     else:
#         raise ValidationError(
#             f"{instance.stream_list.name} is not of type xlsx or csv,Stream have to added manually",
#             code=status.HTTP_400_BAD_REQUEST,
#         )

#     if not "title" in df.columns:
#         raise ValidationError(
#             """
#             column name should be => 'streams' without quotation,
#             Auto Stream Creation Failed,
#             """,
#             code=status.HTTP_404_NOT_FOUND,
#         )
#     # - end of check for stream

#     # 2. check teacher
#     # if instance.allowed_teacher_list == None:
#     #     raise ValidationError(
#     #         detail="Teacher List Not Found",
#     #         code=status.HTTP_404_NOT_FOUND,
#     #     )
#     # file_abs_path = None
#     # teacher_file_path = os.path.join(
#     #     settings.BASE_DIR,
#     #     settings.MEDIA_ROOT,
#     #     instance.allowed_teacher_list.name,
#     # )
#     # if os.path.exists(teacher_file_path):
#     #     file_abs_path = os.path.abspath(teacher_file_path)
#     # else:
#     #     raise ValidationError(
#     #         detail="Teacher List Not Found Or Corrupted",
#     #         code=status.HTTP_404_NOT_FOUND,
#     #     )

#     df = None
#     if str(file_abs_path).split(".")[-1] == "csv":
#         df: pd.DataFrame = pd.read_csv(file_abs_path)
#     elif str(file_abs_path).split(".")[-1] == "xlsx":
#         df = pd.read_excel(file_abs_path)
#     else:
#         # FIXME: delete college instance & add proper message
#         raise ValidationError(
#             f"{instance.allowed_teacher_list.name} is not of type xlsx or csv",
#             code=status.HTTP_400_BAD_REQUEST,
#         )

#     if not "email" in df.columns:
#         raise ValidationError(
#             """
#             column name should be => 'email' without quotation and small letters,
#             Auto Teacher Creation Failed,
#             """,
#             code=status.HTTP_404_NOT_FOUND,
#         )
#     # - end of check for teacher
#     # 3. check dba
#     # is_owner_of_college_exists = AllowedCollegeDBA.objects.filter(
#     #     email=instance.owner_email_id
#     # ).exists()
#     # if is_owner_of_college_exists:
#     #     # from rest_framework import status

#     #     raise ValidationError(
#     #         detail=f"""
#     #         college owner {instance.owner_email_id} already associated with
#     #         college - {instance.name}""",
#     #         code=status.HTTP_400_BAD_REQUEST,
#     #     )

#     if instance.allowed_dba_list == None:
#         raise ValidationError(
#             detail="Admin List Not Found",
#             code=status.HTTP_404_NOT_FOUND,
#         )
#     file_abs_path = None
#     dba_file_path = os.path.join(
#         settings.BASE_DIR,
#         settings.MEDIA_ROOT,
#         instance.allowed_dba_list.name,
#     )
#     if os.path.exists(dba_file_path):
#         file_abs_path = os.path.abspath(dba_file_path)
#     else:
#         raise ValidationError(
#             detail="Admin List Not Found or Corrupted",
#             code=status.HTTP_404_NOT_FOUND,
#         )

#     df = None
#     if str(file_abs_path).split(".")[-1] == "csv":
#         df: pd.DataFrame = pd.read_csv(file_abs_path)
#     elif str(file_abs_path).split(".")[-1] == "xlsx":
#         df = pd.read_excel(file_abs_path)
#     else:
#         raise ValidationError(
#             f"Admin File - [{instance.allowed_dba_list.name}] not of type -> xlsx or csv, Please Upload proper file"
#         )

#     if not "email" in df.columns:
#         raise ValidationError(
#             """
#             Wrong File Structure,
#             column name should be => 'email' without the quot
#             """,
#             code=status.HTTP_400_BAD_REQUEST,
#         )
#     df_dict = df.to_dict("records")
#     if len(df_dict) < 1:

#         raise ValidationError(
#             detail="Please give at least one mail-id in the file ",
#             code=status.HTTP_400_BAD_REQUEST,
#         )
#     # - end of check for dba
