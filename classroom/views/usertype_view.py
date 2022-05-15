from rest_framework.generics import RetrieveAPIView as _rav
from rest_framework import status
from classroom.models.college_dba import CollegeDBA
from classroom.models.student import Student

from classroom.models.teacher import Teacher
from rest_framework.response import Response

from classroom.serializers.usertype import UserTypeSerializer


class UserTypeAPIView(_rav):
    my_tags = ["auth [user category]"]

    def get_serializer_class(self):
        return UserTypeSerializer

    def get(self, request, id, **kwargs):
        if Teacher.objects.select_related("user").filter(user__id=id).exists():
            teacher = (
                Teacher.objects.select_related("user").filter(user__id=id)
                # .only("id")
                .first()
            )
            return Response(
                {"user_type": "teacher", "teacher_id": teacher.id},
                status=status.HTTP_200_OK,
            )

        elif Student.objects.select_related("user").filter(user__id=id).exists():
            student = (
                Student.objects.select_related("user").filter(user__id=id)
                # .only("id")
                .first()
            )
            return Response(
                {"user_type": "student", "student_id": student.id},
                status=status.HTTP_200_OK,
            )

        elif CollegeDBA.objects.select_related("user").filter(user__id=id).exists():

            dba = (
                CollegeDBA.objects.select_related("user").filter(user__id=id)
                # .only("id")
                .first()
            )
            return Response(
                {"user_type": "college_dba", "dba_id": dba.id},
                status=status.HTTP_200_OK,
            )

        else:

            return Response(
                {"error": {"user_type": "user unknown"}},
                status=status.HTTP_404_NOT_FOUND,
            )
