from django.db.transaction import atomic
from django.core.mail import send_mail
from rest_framework import serializers as _sz
from rest_framework.exceptions import ValidationError as _error
from rest_framework.serializers import ModelSerializer as _ms
from rest_framework import status
from classroom.models.classroom import Classroom
from classroom.models.college import AllowedCollegeDBA, College
from classroom.models.college_dba import CollegeDBA
from classroom.serializers.classroom import CollegeReadSerializer
from classroom.serializers.teacher import MinimalUserDetailsSerializer


class AllowedCollegeDBAReadSerializer(_ms):
    college_slug = _sz.SlugField(source="college.slug", read_only=True)

    class Meta:
        model = AllowedCollegeDBA
        fields = ["id", "email", "college_slug"]


class AllowedCollegeDBACreateSerializer(_ms):
    college = _sz.SlugField(source="college.slug", read_only=True)

    class Meta:
        model = AllowedCollegeDBA
        fields = ["id", "email", "college"]
        read_only_fields = ["id", "college"]

    @atomic
    def create(self, validated_data):
        college_slug = self.context.get("college_slug")
        try:
            college: College = College.objects.get(slug=college_slug)
        except:
            raise _error(
                f"College not exists with slug --> {college_slug}",
                code=status.HTTP_404_NOT_FOUND,
            )
        try:
            self.instance = AllowedCollegeDBA.objects.create(
                college=college, **validated_data
            )
            subject = f"You have been added to DBA list of {college.name}"
            body = f"""
                Now you can sign up with mail id - {validated_data.get('email')}
                1. Sign Up
                2. Verify Email by activation
                3. Login
                ----------------
                NB: You will be able to manage classrooms for {college.name}    
            """

            send_mail(
                subject, body, college.owner_email_id, [validated_data.get("email")]
            )
        except:
            dba_email = validated_data.get("email", "No Email Found")
            raise _error(
                f"Could not able to add DBA {dba_email}",
                status=status.HTTP_204_NO_CONTENT,
            )
        return self.instance


class CollegeReadForDBASerializer(_ms):
    class Meta:
        model = College
        fields = ["slug", "name"]
        read_only_fields = ["slug", "name"]


class CollegeCreateSerializer(_ms):
    allowed_teacher_list = _sz.FileField(max_length=None, use_url=True, required=False)

    class Meta:
        model = College
        fields = [
            "slug",
            "name",
            "city",
            "state",
            "address",
            "owner_email_id",
            "allowed_teacher_list",
            "allowed_dba_list",
        ]
        read_only_fields = ["slug"]


class CollegeDBAProfileSerializer(_sz.ModelSerializer):
    dba_id = _sz.IntegerField(source="id", read_only=True)
    user = MinimalUserDetailsSerializer()
    college = CollegeReadSerializer()

    class Meta:
        model = CollegeDBA
        fields = ("dba_id", "is_owner", "user", "college")


class ClassroomCreateByDBASerializer(_ms):
    college = _sz.SlugField(source="college.slug", read_only=True)
    allowed_teacher_list = _sz.FileField(max_length=None, use_url=True, required=False)
    allowed_student_list = _sz.FileField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Classroom
        fields = (
            "slug",
            "title",
            "level",
            "stream",
            "start_year",
            "end_year",
            "section",
            "no_of_semesters",
            "current_sem",
            "created_at",
            "college",
            "allowed_student_list",
            "allowed_teacher_list",
            # "teachers",
        )
        read_only_fields = ["slug", "created_at", "college"]

    def create(self, validated_data):
        college_slug = self.context.get("college_slug")
        try:
            college: College = College.objects.get(slug=college_slug)
        except:
            raise _error(
                f"College not exists with slug --> {college_slug}",
                code=status.HTTP_404_NOT_FOUND,
            )

        try:
            self.instance = Classroom.objects.create(college=college, **validated_data)
        except:
            # dba_email = validated_data.get("email", "No Email Found")
            raise _error(
                f"Could not able to classroom",
                status=status.HTTP_204_NO_CONTENT,
            )
        return self.instance


class ClassroomUpdateByDBASerializer(_ms):
    # college = _sz.SlugField(source="college.slug", read_only=True)
    # allowed_teacher_list = _sz.FileField(max_length=None, use_url=True, required=False)
    # allowed_student_list = _sz.FileField(max_length=None, use_url=True, required=False)
    teachers_count = _sz.SerializerMethodField(method_name="get_teachers_count")

    class Meta:
        model = Classroom
        fields = (
            "slug",
            "title",
            "level",
            "stream",
            "start_year",
            "end_year",
            "section",
            "no_of_semesters",
            "current_sem",
            "created_at",
            "college",
            "teachers_count",
            # "allowed_student_list",
            # "allowed_teacher_list",
        )
        read_only_fields = [
            "slug",
            "stream",
            "start_year",
            "end_year",
            "no_of_semesters",
            "created_at",
            "college",
        ]

    def get_teachers_count(self, obj: Classroom) -> int:
        return obj.teachers.count()


class ClassroomReadByDBASerializer(_ms):
    teachers_count = _sz.SerializerMethodField(method_name="get_teachers_count")

    class Meta:
        model = Classroom
        fields = (
            "slug",
            "title",
            "level",
            "stream",
            "start_year",
            "end_year",
            "section",
            "no_of_semesters",
            "current_sem",
            "created_at",
            "college",
            "teachers_count",
        )

    def get_teachers_count(self, obj: Classroom) -> int:
        return obj.teachers.count()
