from django.shortcuts import render
from .serializers.student import StudentReadSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from .models import Student


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
