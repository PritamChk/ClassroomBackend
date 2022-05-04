from rest_framework.serializers import ModelSerializer as ms
from classroom.models import Student
from .classroom import ClassroomReadSerializer


class StudentReadSerializer(ms):
    """
        Returns Student ID & User Profile along with Classroom Details
    """
    class Meta:
        model = Student
        fields = "__all__"
        # read_only_fields = "__all__"
        depth = 1
