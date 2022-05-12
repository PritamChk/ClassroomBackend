from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from classroom.models import Teacher

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


class SubjectForTeacher(ModelViewSet):
    my_tags = ["subjects/classroom [teacher]"]
    
