from classroom.serializers.classroom import (
    AnnouncementsReadSerializer,
    ClassroomReadForStudentSerializer,
    NotesReadForStudentSerializer,
    SemesterReadSerializer,
    SubjectReadSerializer,
)
from classroom.serializers.student import StudentReadSerializer
from rest_framework.decorators import api_view
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Announcement, Classroom, Notes, Student, Subject, Teacher, Semester


@api_view(["GET"])
def user_category(request, id):  # TODO: Shift this code in other file
    my_tags = ["User Category"]
    if Teacher.objects.select_related("user").filter(user__id=id).exists():
        teacher = (
            Teacher.objects.select_related("user").filter(user__id=id)
            # .only("id")
            .first()
        )
        return Response({"user_type": "teacher", "teacher_id": teacher.id})
    elif Student.objects.select_related("user").filter(user__id=id).exists():
        student = (
            Student.objects.select_related("user").filter(user__id=id)
            # .only("id")
            .first()
        )
        return Response({"user_type": "student", "student_id": student.id})
    else:
        return Response({"user_type": "user unknown"})


class StudentProfileViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Student End point will return student profile details along with classroom details
    """

    my_tags = ["student"]
    queryset = (
        Student.objects.select_related("user")
        .select_related("classroom")
        .select_related("classroom__college")
        .all()
    )
    serializer_class = StudentReadSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ClassroomForStudentViewSet(RetrieveModelMixin, GenericViewSet):
    """
    This view is used by student only
    student can only retrive but won't be able to see the other classrooms
    """

    my_tags = ["classroom For student"]
    swagger_schema = None
    serializer_class = ClassroomReadForStudentSerializer
    lookup_field = "slug"

    def get_queryset(self):
        classroom = (
            Classroom.objects.select_related("college")
            .prefetch_related("students")
            .filter(slug=self.kwargs["slug"])
        )
        return classroom


class SemesterForStudentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["semester for student"]
    serializer_class = SemesterReadSerializer
    # lookup_field = 'id'
    def get_queryset(self):
        sem = Semester.objects.select_related("classroom").filter(
            classroom__slug=self.kwargs["classroom_slug"]
        )
        return sem


class SubjectsForStudentsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["subjects / sem [student]"]
    serializer_class = SubjectReadSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Subject.objects.select_related("semester")
            .select_related("semester__classroom")
            .filter(semester__id=self.kwargs["semester_pk"])
        )  # FIXME: This might be slow in future. Req: Optimization


class AnnouncementForStudentsViewSet(ListModelMixin, GenericViewSet):
    """
    Announcements for the particular subject will be shown in decreasing order
    """

    my_tags = ["announcements /subject  [student]"]
    serializer_class = AnnouncementsReadSerializer

    def get_queryset(self):
        return Announcement.objects.select_related("subject").filter(
            subject__slug=self.kwargs["subject_slug"]
        )


class NotesForStudentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Notes for the particular subject will be shown in decreasing order
    """

    my_tags = ["notes/subject [student]"]
    serializer_class = NotesReadForStudentSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Notes.objects.select_related("subject", "posted_by", "posted_by__user")
            .prefetch_related("attached_files")
            .filter(subject__slug=self.kwargs["subject_slug"])
        )


# TODO: Add Assignment View
