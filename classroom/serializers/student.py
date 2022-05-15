from rest_framework.serializers import ModelSerializer as ms
from classroom.model import Student, User
from .classroom import ClassroomReadForStudentSerializer
from accounts.serializers import CurrentUserSerializer


class StudentUserReadSerializer(ms):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "contact_no", "email")


class StudentReadSerializer(ms):
    """
    Returns Student ID & User Profile along with Classroom Details
    """

    user = StudentUserReadSerializer()
    classroom = ClassroomReadForStudentSerializer()

    class Meta:
        model = Student
        fields = ("university_roll", "user", "classroom")
        # read_only_fields = "__all__"
        # depth = 1
