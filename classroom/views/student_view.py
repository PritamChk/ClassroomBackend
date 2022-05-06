from rest_framework.decorators import api_view
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView

from classroom.serializers.student import StudentReadSerializer
from ..models import Student, Teacher


@api_view(["GET"])
def user_category(request, id):
    my_tags = ["User Category"]
    if Teacher.objects.select_related("user").filter(user__id=id).exists():
        teacher = (
            Teacher.objects.select_related("user").filter(user__id=id)
            # .only("id")
            .first()
        )
        return Response({"user_type": "teacher", "teacher_id": teacher.id})
    elif Student.objects.select_related("user").filter(user__id=id).exists():
        student = (
            Student.objects.select_related("user").filter(user__id=id)
            # .only("id")
            .first()
        )
        return Response({"user_type": "student", "student_id": student.id})
    else:
        return Response({"user_type": "user unknown"})


class StudentViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Student End point will return student profile details along with classroom details
    """

    my_tags = ["Student"]
    queryset = Student.objects.select_related("user").select_related("classroom").all()
    serializer_class = StudentReadSerializer

    def get_serializer_context(self):
        return {"request": self.request}
