from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import cprint

from ..views.student_view import (
    AnnouncementForStudentsViewSet,
    AssignmentSubmissionByStudentViewSet,
    AssignmentViewForStudentViewSet,
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

subject_assignment_router = NestedDefaultRouter(
    sem_subjects_router, "subject", lookup="subject"
)
subject_assignment_router.register(
    "assignment", AssignmentViewForStudentViewSet, basename="assignment"
)

assignment_submission_router = NestedDefaultRouter(
    subject_assignment_router, "assignment", lookup="assignment"
)
assignment_submission_router.register(
    "submission", AssignmentSubmissionByStudentViewSet, basename="submission"
)

stud_urlpatterns = []

stud_urlpatterns += (
    student_router.urls
    + classroom_router.urls
    + classroom_sems_router.urls
    + sem_subjects_router.urls
    + subject_announcement_router.urls
    + subject_notes_router.urls
    + subject_assignment_router.urls
    + assignment_submission_router.urls
)

# cprint("-------------------------------------------", "green")
# cprint("Student URLs -", "green")
# cprint("-------------------------------------------", "green")
# for url in stud_urlpatterns:
#     cprint(url, "cyan")
