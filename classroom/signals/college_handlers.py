from .common_imports import *

# @shared_task
@receiver(post_save, sender=College)
def create_allowed_teacher(sender, instance: College, created, **kwargs):
    if created:
        if instance.allowed_teacher_list == None:
            send_mail(
                "Allowed Teacher List Does Not Exists",
                "You Have To Create Allowed Teachers Manually",
                settings.EMAIL_HOST_USER,
                ["dba@admin.com"],  # FIXME: Send mail to session dba
            )
            return None
        file_abs_path = None
        dba_file_path = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            instance.allowed_teacher_list.name,
        )
        if os.path.exists(dba_file_path):
            file_abs_path = os.path.abspath(dba_file_path)
        else:
            send_mail(
                "Allowed Teacher List Does Not Exists",
                "You Have To Create Allowed Teachers Manually",
                settings.EMAIL_HOST_USER,
                ["dba@admin.com"],  # FIXME: Send mail to session dba
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
                ["dba@admin.com"],  # FIXME: Send mail to session dba
            )
            return None
        df_dict = df.to_dict("records")
        # print(df_dict)
        list_of_teachers = [
            AllowedTeacher(college=instance, **args) for args in df.to_dict("records")
        ]
        AllowedTeacher.objects.bulk_create(list_of_teachers)
        # create_bulk_allowed_teacher.delay(df_dict, instance)
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
    if created:
        college: College = College.objects.get(pk=instance.college)
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
