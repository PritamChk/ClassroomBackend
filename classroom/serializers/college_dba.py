from django.db.transaction import atomic
from numpy import source
from rest_framework import serializers as _sz
from rest_framework.exceptions import ValidationError as _error
from rest_framework.serializers import ModelSerializer as _ms
from rest_framework.status import HTTP_409_CONFLICT, HTTP_412_PRECONDITION_FAILED

from classroom.models.college import AllowedCollegeDBA, College


class AllowedCollegeDBAReadSerializer(_ms):
    college = _sz.SlugRelatedField("college.slug", read_only=True)

    class Meta:
        model = AllowedCollegeDBA
        fields = ["id", "email", "college"]


class AllowedCollegeDBACreateSerializer(_ms):
    college_slug = _sz.SlugField(source="college.slug", read_only=True)

    class Meta:
        model = AllowedCollegeDBA
        fields = ["id", "email", "college_slug"]
        read_only_fields = ["id", "college_slug"]


class CollegeCreateSerializer(_ms):
    allowed_dbas = AllowedCollegeDBACreateSerializer(many=True)
    allowed_teacher_list = _sz.FileField(max_length=None, use_url=True, required=False)

    class Meta:
        model = College
        fields = [
            "id",
            "slug",
            "name",
            "city",
            "state",
            "address",
            "allowed_teacher_list",
            "allowed_dbas",
        ]
        read_only_fields = ["id", "slug"]

    # TODO:Transaction used
    @atomic
    def create(self, validated_data):
        dba_mails = validated_data.pop("allowed_dbas")
        for dba_mail in dba_mails:
            if AllowedCollegeDBA.objects.filter(email=dba_mail["email"]).exists():
                dba = dba_mail.get("email")
                raise _error(
                    detail=f"DBA --> {dba} already associated with a college & cannot create a new college",
                    code=HTTP_409_CONFLICT,
                )
        try:
            college = College.objects.create(**validated_data)
        except:
            raise _error(
                detail=f"College Creation Failed Due to Unknown reason",
                code=HTTP_412_PRECONDITION_FAILED,
            )
        try:
            allowed_dba_object_list = [
                AllowedCollegeDBA(college=college, **email) for email in dba_mails
            ]
            AllowedCollegeDBA.objects.bulk_create(
                allowed_dba_object_list
            )
        except:
            raise _error(
                detail=f"DBA Bulk Creation Failed Due to Unknown reason",
                code=HTTP_412_PRECONDITION_FAILED,
            )
        from classroom.tasks import send_email_after_bulk_object_creation

        subject = "Sign up to Create Your DBA Profile"
        prompt = f"""
            You have been assigned as DBA of college - {college.name}
        """
        mail_list = [email for email in dba_mails]
        send_email_after_bulk_object_creation.delay(subject, prompt, mail_list)
        self.instance = college
        return self.instance


# from drf_writable_nested import WritableNestedModelSerializer as _wnms

# class CollegeCreateSerializer(_wnms):
#     allowed_dbas = AllowedCollegeDBACreateSerializer(many=True)
#     allowed_teacher_list = _sz.FileField(max_length=None, use_url=True, required=False)

#     class Meta:
#         model = College
#         fields = [
#             "id",
#             "slug",
#             "name",
#             "city",
#             "state",
#             "address",
#             "allowed_teacher_list",
#             "allowed_dbas",
#         ]
#         read_only_fields = ["id", "slug"]
