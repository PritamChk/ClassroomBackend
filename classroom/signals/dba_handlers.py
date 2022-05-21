from .common_imports import *


@shared_task
@receiver(post_save, sender=College)
def create_allowed_dba(sender, instance: College, created, **kwargs):
    if created:
        is_owner_of_college_exists = AllowedCollegeDBA.objects.filter(
            email=instance.owner_email_id
        ).exists()
        if is_owner_of_college_exists:
            from rest_framework import status

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
                College.objects.filter(
                    pk=instance.id
                ).delete()  # FIXME: Delete this line if not works
                send_mail(
                    "Allowed DBA List Does Not Exists",
                    "You Have To Create Allowed DBAs Manually",
                    settings.EMAIL_HOST_USER,
                    ["dba@admin.com"],  # FIXME: Send mail to session dba
                )
                return None
            file_abs_path = None
            dba_file_path = os.path.join(
                settings.BASE_DIR,
                settings.MEDIA_ROOT,
                instance.allowed_dba_list.name,
            )
            if os.path.exists(dba_file_path):
                file_abs_path = os.path.abspath(dba_file_path)
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

            if not "email" in df.columns:
                send_mail(
                    "Wrong File Structure",
                    "column name should be => 'email' ",
                    settings.EMAIL_HOST_USER,
                    [instance.owner_email_id],  # FIXME: Send mail to session dba
                )
                return None
            df_dict = df.to_dict("records")
            if len(df_dict) < 1:

                raise ValidationError(
                    detail="Please give at least one mail-id in the fail "
                )

            # print(df_dict)
            list_of_teachers = [
                AllowedCollegeDBA(college=instance, **args)
                for args in df.to_dict("records")
            ]
            AllowedCollegeDBA.objects.bulk_create(list_of_teachers)
            email_list = df["email"].to_list()
            subject = "Open Your DBA Account"
            prompt = "please use your following mail id to sign up in the Classroom[LMS]"
            try:
                send_email_after_bulk_object_creation.delay(subject, prompt, email_list)
            except BadHeaderError:
                print("Could not able to send emails to DBAs")
            os.remove(file_abs_path)
            instance.allowed_teacher_list = ""
            instance.allowed_dba_list = ""
