from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from classroom.models import Classroom, Subject, Teacher
from classroom.serializers.classroom import (
    ClassroomReadForStudentSerializer,
    ClassroomReadForTeacherSerializer,
    SubjectCreateByTeacherSerializer,
    SubjectRetriveForTeacherSerializer,
)

from classroom.serializers.teacher import TeacherProfileSerializer


class TeacherProfileViewSet(RetrieveModelMixin, GenericViewSet):
    my_tags = ["teacher profile"]
    serializer_class = TeacherProfileSerializer

    def get_queryset(self):
        return (
            Teacher.objects.select_related("user").prefetch_related("classrooms")
            # .filter(user__id=self.request.user.id) #TODO:This will work after permission applied
            .filter(id=self.kwargs["pk"])
        )


class ClassroomsForTeacherViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["classrooms for teacher"]
    serializer_class = ClassroomReadForTeacherSerializer
    lookup_field='slug'

    def get_queryset(self):
        return Classroom.objects.prefetch_related("teachers",'semesters').filter(
            teachers__id=self.kwargs["teacher_pk"]
        )


# class SubjectForTeacher(ModelViewSet):
#     my_tags = ["subjects/classroom [teacher]"]

#     def get_serializer_class(self):
#         if self.request.method == "GET" or self.request.method == "PATCH":
#             return SubjectRetriveForTeacherSerializer
#         elif self.request.method == "POST":
#             return SubjectCreateByTeacherSerializer

#     def get_queryset(self):
#         return Subject.objects.select_related('created_by','semester').filter(semester=)
