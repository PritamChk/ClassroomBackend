from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import cprint

from ..views.student_view import (
    AnnouncementForStudentsViewSet,
    ClassroomForStudentViewSet,
    NotesForStudentViewSet,
    SemesterForStudentViewSet,
    StudentProfileViewSet,
    SubjectsForStudentsViewSet,
)

student_router = DefaultRouter()
student_router.register("student", StudentProfileViewSet, "student")


classroom_router = DefaultRouter()
classroom_router.register("classroom", ClassroomForStudentViewSet, "classroom")

classroom_sems_router = NestedDefaultRouter(
    classroom_router, "classroom", lookup="classroom"
)
classroom_sems_router.register("semester", SemesterForStudentViewSet, basename="sem")

sem_subjects_router = NestedDefaultRouter(
    classroom_sems_router, "semester", lookup="semester"
)
sem_subjects_router.register("subject", SubjectsForStudentsViewSet, basename="subject")


subject_announcement_router = NestedDefaultRouter(
    sem_subjects_router, "subject", lookup="subject"
)
subject_announcement_router.register(
    "announcement", AnnouncementForStudentsViewSet, basename="announcement"
)

subject_notes_router = NestedDefaultRouter(
    sem_subjects_router, "subject", lookup="subject"
)
subject_notes_router.register("notes", NotesForStudentViewSet, basename="notes")

# stud_urlpatterns = [path("user-type/<uuid:id>", user_category, name="user-category")]
stud_urlpatterns = []

stud_urlpatterns += (
    student_router.urls
    + classroom_router.urls
    + classroom_sems_router.urls
    + sem_subjects_router.urls
    + subject_announcement_router.urls
    + subject_notes_router.urls
)

# for url in stud_urlpatterns:
#     cprint(url, "green")
