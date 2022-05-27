import os
from django.conf import settings
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from classroom.model import (
    Announcement,
    Classroom,
    Notes,
    NotesAttachmentFile,
    Semester,
    Subject,
    Teacher,
)
from classroom.models.assignment import Assignment, AssignmentSubmission
from classroom.serializers.classroom import (
    AnnouncementsPostOrUpdateSerializer,
    AnnouncementsReadSerializer,
    AssignmentPostByTeacherSerializer,
    AssignmentSubmissionEvaluationByTeacher,
    AssignmentSubmissionEvaluationReadByTeacher,
    AssignmentUpdateByTeacherSerializer,
    ClassroomReadForStudentSerializer,
    ClassroomReadForTeacherSerializer,
    NotesFileReadByStudentSerializer,
    NotesFileUploadByTeacherSerializer,
    NotesReadForStudentSerializer,
    NotesCreateForTeacherSerializer,
    NotesUpdateForTeacherSerializer,
    SemesterReadSerializer,
    SubjectCreateByTeacherSerializer,
    SubjectRetrieveForTeacherSerializer,
)

from classroom.serializers.teacher import (
    TeacherProfileForDBASerializer,
    TeacherProfileSerializer,
)


class TeacherProfileViewSet(RetrieveModelMixin, GenericViewSet):
    my_tags = ["[teacher] 1. profile"]
    serializer_class = TeacherProfileSerializer

    def get_queryset(self):
        return (
            Teacher.objects.select_related("user").prefetch_related("classrooms")
            # .filter(user__id=self.request.user.id) #TODO:This will work after permission applied
            .filter(id=self.kwargs.get("pk"))
        )


class TeacherProfilesForDBAViewSet(ListModelMixin, GenericViewSet):
    my_tags = ["[teacher] 1. profile"]
    serializer_class = TeacherProfileForDBASerializer

    def get_queryset(self):
        return (
            Teacher.objects.select_related("user", "college")
            # .filter(user__id=self.request.user.id) #TODO:This will work after permission applied
            .filter(college__slug=self.kwargs.get("college_slug"))
        )


class ClassroomsForTeacherViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["[teacher] 2. classrooms"]
    serializer_class = ClassroomReadForTeacherSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Classroom.objects.prefetch_related("teachers", "semesters").filter(
            teachers__id=self.kwargs["teacher_pk"]
        )


class SemesterForTeacherViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["[teacher] 3. semesters/classroom"]
    serializer_class = SemesterReadSerializer
    # lookup_field = 'id'
    def get_queryset(self):
        sem = Semester.objects.select_related("classroom").filter(
            classroom__slug=self.kwargs.get("teacher_classrooms_slug")
        )
        return sem


class SubjectForTeacherViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    my_tags = ["[teacher] 4. subjects/classroom"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SubjectRetrieveForTeacherSerializer
        elif self.request.method == "POST":
            return SubjectCreateByTeacherSerializer
        return SubjectRetrieveForTeacherSerializer

    def get_queryset(self):
        return (
            Subject.objects.select_related("created_by", "semester")
            .filter(
                semester=self.kwargs.get("sem_pk"),
                created_by=self.kwargs.get("teacher_pk"),
            )
            .all()
        )

    def get_serializer_context(self):
        return {
            "created_by": self.kwargs.get("teacher_pk"),
            "sem_pk": self.kwargs.get("sem_pk"),
        }


class AnnouncementPostByTeacherViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    my_tags = ["[teacher] 5. announcement/subject"]
    # lookup_field='slug'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AnnouncementsReadSerializer
        return AnnouncementsPostOrUpdateSerializer

    def get_queryset(self):
        return Announcement.objects.select_related("posted_by", "subject").filter(
            posted_by=self.kwargs.get("teacher_pk"),
            subject__slug=self.kwargs.get("subject_slug"),
        )

    def get_serializer_context(self):
        return {
            "teacher_pk": self.kwargs.get("teacher_pk"),
            "subject_slug": self.kwargs.get("subject_slug"),
        }


class TeacherNotesUploadViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch", "head", "options"]
    my_tags = ["[teacher] 6.1 notes crud"]
    lookup_field = "slug"
    # serializer_class = NotesWriteForTeacherSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return NotesReadForStudentSerializer
        elif self.request.method == "PATCH":
            return NotesUpdateForTeacherSerializer
        return NotesCreateForTeacherSerializer

    def get_queryset(self):
        return (
            Notes.objects.select_related("posted_by", "subject")
            .prefetch_related("attached_files")
            .filter(
                posted_by=self.kwargs.get("teacher_pk"),
                subject__slug=self.kwargs.get("subject_slug"),
            )
        )

    def get_serializer_context(self):
        return {
            "teacher_pk": self.kwargs.get("teacher_pk"),
            "subject_slug": self.kwargs.get("subject_slug"),
        }


from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView
from termcolor import cprint

# TODO: link : https://stackoverflow.com/questions/34326150/multipartparsererror-invalid-boundary
class FileUploadDeleteViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "options", "head"]
    my_tags = ["[teacher] 6.2 upload/delete attached notes file"]
    serializer_class = NotesFileUploadByTeacherSerializer
    lookup_field = "title"
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_serializer_context(self):
        return {"notes_slug": self.kwargs.get("notes_slug"), "request": self.request}

    def get_queryset(self):
        return NotesAttachmentFile.objects.select_related("notes").filter(
            notes__slug=self.kwargs.get("notes_slug"),
        )

    # def create(self, request, *args, **kwargs):
    #     cprint(request.data, "green")
    #     return super().create(request, *args, **kwargs)


class AssignmentPostViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "options", "head"]
    my_tags = ["[teacher] 7. assignment"]
    serializer_class = AssignmentPostByTeacherSerializer
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):
        return Assignment.objects.select_related("subject").filter(
            subject__slug=self.kwargs.get("subject_slug")
        )

    def get_serializer_context(self):
        return {"subject_slug": self.kwargs.get("subject_slug")}

    def get_serializer_class(self):
        method = self.request.method
        if method == "PATCH":
            return AssignmentUpdateByTeacherSerializer
        return AssignmentPostByTeacherSerializer


class AssignmentEvaluationViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "options", "head"]
    my_tags = ["[teacher] 8. assignment evaluation"]
    serializer_class = AssignmentSubmissionEvaluationByTeacher

    def get_serializer_class(self):
        method = self.request.method
        if method in SAFE_METHODS:
            return AssignmentSubmissionEvaluationReadByTeacher
        return AssignmentSubmissionEvaluationByTeacher

    def get_queryset(self):
        return AssignmentSubmission.objects.select_related("assignment").filter(
            assignment__id=self.kwargs.get("assignment_pk")
        )
