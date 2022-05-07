from rest_framework.serializers import ModelSerializer as ms
from accounts.serializers import CurrentUserSerializer
from classroom.models import Teacher, User

class SubjectTeacherDetailsSerializer(ms):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class TeacherReadForSubjectSerializer(ms):
    user = SubjectTeacherDetailsSerializer()

    class Meta:
        model = Teacher
        exclude = ["classroom"]
        depth = 1
        select_related_fields = ["user"]
