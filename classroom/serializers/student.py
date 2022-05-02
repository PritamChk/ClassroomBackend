from rest_framework.serializers import ModelSerializer as ms
from classroom.models import Student


class StudentCreateSerializer(ms):
    class Meta:
        model = Student
        fields = "__all__"


class StudentReadSerializer(ms):
    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = "__all__"
