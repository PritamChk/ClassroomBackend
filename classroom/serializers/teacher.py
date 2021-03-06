from rest_framework.serializers import ModelSerializer as ms, IntegerField, FileField
from accounts.serializers import CurrentUserSerializer
from classroom.model import Classroom, Teacher, User


class MinimalUserDetailsSerializer(ms):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "contact_no"]


class MinimalTeacherDetailsSerializer(ms):
    user = MinimalUserDetailsSerializer()
    teacher_id = IntegerField(source="id")

    class Meta:
        model = Teacher
        fields = ["user", "teacher_id"]


class TeacherReadForSubjectSerializer(ms):
    user = MinimalUserDetailsSerializer()

    class Meta:
        model = Teacher
        fields = "__all__"
        depth = 1
        select_related_fields = ["user"]


class TeacherClassroomsGetSerializer(ms):
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
        )


# ----------------- teacher view serializers -----------------
class TeacherProfileSerializer(ms):
    user = MinimalUserDetailsSerializer()
    teacher_id = IntegerField(source="id")
    classroom_list = TeacherClassroomsGetSerializer(many=True, source="classrooms")

    class Meta:
        model = Teacher
        fields = ["teacher_id", "user", "classroom_list"]


class TeacherProfileForDBASerializer(ms):
    user = MinimalUserDetailsSerializer()
    teacher_id = IntegerField(source="id")
    # classroom_list = TeacherClassroomsGetSerializer(many=True, source="classrooms")

    class Meta:
        model = Teacher
        fields = ["teacher_id", "user"]
