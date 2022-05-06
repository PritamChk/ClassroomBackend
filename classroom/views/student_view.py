from rest_framework.decorators import api_view
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Student, Teacher
from ..serializers.student import StudentReadSerializer


@api_view(["GET"])
def user_category(request, id):
    my_tags = ["User Category"]
    if Teacher.objects.select_related("user").filter(user__id=id).exists():
        return Response({"user_type": "teacher"})
    elif Student.objects.select_related("user").filter(user__id=id).exists():
        return Response({"user_type": "student"})
    else:
        return Response({"user_type": "user unknown"})


# class DynamicRetriveUser(RetrieveModelMixin, GenericAPIView):
#     my_tags = ["User Category"]
#     http_methods = ["GET"]

#     def get_queryset(self):
#         id = self.kwargs["pk"]
#         if Teacher.objects.select_related("user").filter(user__id=id).exists():
#             return (
#                 Teacher.objects.select_related("user")
#                 .prefetch_related("classroom")
#                 .all(pk=id)
#             )
#         elif Student.objects.select_related("user").filter(user__id=id).exists():
#             return (
#                 Student.objects.select_related("user")
#                 .select_related("classroom")
#                 .filter(pk=id)
#             )

#     def get_serializer_class(self):
#         if Student.objects.select_related("user").filter(user__id=id).exists():
#             return StudentReadSerializer


class StudentViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Student End point will return student profile details along with classroom details
    """

    my_tags = ["Student"]

    def get_queryset(self):
        return Student.objects.select_related("classroom").select_related("user").all()

    def get_serializer_class(self):
        return StudentReadSerializer

    def me(self):
        q = (
            Student.objects.select_related("classroom")
            .select_related("user")
            .get(pk=self.request.user.id)
        )
