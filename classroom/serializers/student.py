from rest_framework.serializers import ModelSerializer as ms
from classroom.models import Student
from .classroom import ClassroomReadSerializer
from accounts.serializers import CurrentUserSerializer

class StudentReadSerializer(ms):
    """
    Returns Student ID & User Profile along with Classroom Details
    """
    user = CurrentUserSerializer()
    classroom = ClassroomReadSerializer()
    class Meta:
        model = Student
        fields = ("university_roll", "user", "classroom")
        # read_only_fields = "__all__"
        # depth = 1
