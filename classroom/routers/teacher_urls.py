from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import cprint

from classroom.views.teacher_view import TeacherProfileViewSet

teacher_router = DefaultRouter()
teacher_router.register("teacher", TeacherProfileViewSet, basename="teacher")

teacher_urlpatterns = []
teacher_urlpatterns += teacher_router.urls

for turl in teacher_urlpatterns:
    cprint(turl, "yellow")
