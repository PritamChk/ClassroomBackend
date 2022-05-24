from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import cprint

from classroom.views.teacher_view import (
    AnnouncementPostByTeacherViewSet,
    AssignmentEvaluationViewSet,
    AssignmentPostViewSet,
    ClassroomsForTeacherViewSet,
    FileUploadDeleteViewSet,
    SemesterForTeacherViewSet,
    SubjectForTeacherViewSet,
    TeacherNotesUploadViewSet,
    TeacherProfileViewSet,
    TeacherProfilesForDBAViewSet,
)
from .dba_urls import college_create_router

teacher_router = DefaultRouter()
teacher_router.register("teacher", TeacherProfileViewSet, basename="teacher")

all_teacher_profiles_for_dba_router = NestedDefaultRouter(
    college_create_router, "college-create", lookup="college"
)
all_teacher_profiles_for_dba_router.register(
    "teacher-profiles", TeacherProfilesForDBAViewSet, basename="teachers"
)

teacher_classrooms = NestedDefaultRouter(teacher_router, "teacher", lookup="teacher")
teacher_classrooms.register(
    "teacher-classrooms", ClassroomsForTeacherViewSet, basename="teacher-classrooms"
)

teacher_sem = NestedDefaultRouter(teacher_router, "teacher", lookup="teacher")
teacher_sem.register("sem", SemesterForTeacherViewSet, basename="sem")
# TODO: implement announcement routers

teacher_subject = NestedDefaultRouter(teacher_sem, "sem", lookup="sem")
teacher_subject.register("subject", SubjectForTeacherViewSet, basename="subject")

teacher_subject_sub_urls = NestedDefaultRouter(
    teacher_router, "teacher", lookup="teacher"
)
teacher_subject_sub_urls.register(
    "subject", SubjectForTeacherViewSet, basename="subject"
)

teacher_subject_announcement = NestedDefaultRouter(
    teacher_subject_sub_urls, "subject", lookup="subject"
)
teacher_subject_announcement.register(
    "announcement", AnnouncementPostByTeacherViewSet, basename="announcement"
)

teacher_subject_notes = NestedDefaultRouter(
    teacher_subject_sub_urls, "subject", lookup="subject"
)
teacher_subject_notes.register("notes", TeacherNotesUploadViewSet, basename="notes")

teacher_notes_file_upload = NestedDefaultRouter(
    teacher_subject_notes, "notes", lookup="notes"
)
teacher_notes_file_upload.register(
    "notes-files", FileUploadDeleteViewSet, basename="notes_files"
)
teacher_assignment_router = NestedDefaultRouter(
    teacher_subject_sub_urls, "subject", lookup="subject"
)
teacher_assignment_router.register(
    "assignment", AssignmentPostViewSet, basename="assignment"
)

teacher_assignment_evaluation_router = NestedDefaultRouter(
    teacher_assignment_router, "assignment", lookup="assignment"
)
teacher_assignment_evaluation_router.register(
    "submission", AssignmentEvaluationViewSet, basename="submission"
)

teacher_urlpatterns = []
teacher_urlpatterns += (
    teacher_router.urls
    + teacher_classrooms.urls
    + teacher_sem.urls
    + teacher_subject.urls
    + teacher_subject_announcement.urls
    + teacher_subject_notes.urls
    + teacher_notes_file_upload.urls
    + teacher_assignment_router.urls
    + teacher_assignment_evaluation_router.urls
    + all_teacher_profiles_for_dba_router.urls
)

# cprint("-------------------------------------------", "red")
# cprint("Teacher URLs -", "red")
# cprint("-------------------------------------------", "red")
# for url in teacher_urlpatterns:
#     cprint(url, "red")
