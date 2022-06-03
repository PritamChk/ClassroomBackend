from .common_imports import *
from rest_framework import status


@shared_task
@receiver(post_save, sender=College)
def create_allowed_dba(sender, instance: College, created, **kwargs):
    if created:
        is_owner_of_college_exists = AllowedCollegeDBA.objects.filter(
            email=instance.owner_email_id
        ).exists()
        if is_owner_of_college_exists:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                detail=f"""
                college owner {instance.owner_email_id} already associated with 
                college - {instance.name}""",
                code=status.HTTP_400_BAD_REQUEST,
            )
        else:
            AllowedCollegeDBA.objects.create(
                college=instance, email=instance.owner_email_id
            )
            subject = f"Welcome to {instance.name}"
            body = f"""
                You are the owner admin of college {instance.name}
                Now you can sign up with mail id - {instance.owner_email_id}
                ----------------
                NB: Only you will be able to add other DBAs or remove them    
            """
            send_mail(
                subject, body, settings.EMAIL_HOST_USER, [instance.owner_email_id]
            )
        if instance.allowed_dba_list == None:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                detail="Allowed Admin List Not Found,College Creation Failed",
                code=status.HTTP_404_NOT_FOUND,
            )
        file_abs_path = None
        dba_file_path = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            instance.allowed_dba_list.name,
        )
        if os.path.exists(dba_file_path):
            file_abs_path = os.path.abspath(dba_file_path)
        else:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                detail="Stream List Not Found,College Creation Failed",
                code=status.HTTP_404_NOT_FOUND,
            )

        df = None
        if str(file_abs_path).split(".")[-1] == "csv":
            df: pd.DataFrame = pd.read_csv(file_abs_path)
        elif str(file_abs_path).split(".")[-1] == "xlsx":
            df = pd.read_excel(file_abs_path)
        else:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                detail="Allowed Admin List Not of Type [Xl/CSV] ,College Creation Failed",
                code=status.HTTP_400_BAD_REQUEST,
            )

        if df.shape[1] != 1:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.allowed_dba_list.name} file should contain ONE Column namely email",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not df.shape[0] > 0:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.allowed_dba_list.name} file can not be empty",
                code=status.HTTP_400_BAD_REQUEST,
            )

        if not "email" in df.columns:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"{instance.stream_list.name} file should contain ONE Column namely email",
                code=status.HTTP_400_BAD_REQUEST,
            )
        # df_dict = df.to_dict("records")
        # if len(df_dict) < 1:

        #     raise ValidationError(
        #         detail="Please give at least one mail-id in the fail "
        #     )

        # print(df_dict)
        try:
            list_of_teachers = [
                AllowedCollegeDBA(college=instance, **args)
                for args in df.to_dict("records")
            ]
            with atomic():
                AllowedCollegeDBA.objects.bulk_create(list_of_teachers)
        except:
            delete_college_on_any_failure(instance.id)
            raise ValidationError(
                f"Bulk Allowed College DBA creation failed, College Creation Failed",
                code=status.HTTP_400_BAD_REQUEST,
            )
        email_list = df["email"].to_list()
        subject = "Open Your DBA Account"
        prompt = "please use your following mail id to sign up in the Classroom[LMS]"
        try:
            send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
        except BadHeaderError:
            print("Could not able to send emails to DBAs")
        os.remove(file_abs_path)
        College.objects.update(allowed_dba_list="")


@receiver(post_delete, sender=AllowedCollegeDBA)
def delete_dba_account_on_deletion_of_allowed_cllg_dba(
    sender, instance: AllowedCollegeDBA, **kwargs
):
    try:
        college_dba = CollegeDBA.objects.select_related("user").filter(
            user__email=instance.email
        )
        if college_dba.exists():
            try:
                college_dba.delete()
            except:
                pass
    except:
        pass
