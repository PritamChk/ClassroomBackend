from classroom.models.assignment import Assignment, AssignmentSubmission
from classroom.serializers.classroom import (
    AnnouncementsReadSerializer,
    ClassroomReadForStudentSerializer,
    NotesReadForStudentSerializer,
    SemesterReadSerializer,
    SubjectReadSerializer,
)
from classroom.serializers.student import (
    AssignmentReadByStudentSerializer,
    AssignmentSubmissionReadByStudent,
    AssignmentSubmissionWriteByStudent,
    StudentReadSerializer,
)
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from ..model import Announcement, Classroom, Notes, Semester, Student, Subject


class StudentProfileViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Student End point will return student profile details along with classroom details
    """

    my_tags = ["[student] 1. profile"]
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
    student can only retrieve but won't be able to see the other classrooms
    """

    my_tags = ["[student] -. classroom"]
    swagger_schema = None
    serializer_class = ClassroomReadForStudentSerializer
    lookup_field = "slug"

    def get_queryset(self):
        classroom = (
            Classroom.objects.select_related("college")
            .prefetch_related("students")
            .filter(slug=self.kwargs.get("slug"))
        )
        return classroom


class SemesterForStudentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["[student] 2. semester"]
    serializer_class = SemesterReadSerializer
    # lookup_field = 'id'
    def get_queryset(self):
        sem = Semester.objects.select_related("classroom").filter(
            classroom__slug=self.kwargs.get("classroom_slug")
        )
        return sem


class SubjectsForStudentsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    my_tags = ["[student] 3. subjects"]
    serializer_class = SubjectReadSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Subject.objects.select_related("semester")
            .select_related("semester__classroom")
            .filter(semester__id=self.kwargs.get("semester_pk"))
        )  # FIXME: This might be slow in future. Req: Optimization


class AnnouncementForStudentsViewSet(ListModelMixin, GenericViewSet):
    """
    Announcements for the particular subject will be shown in decreasing order
    """

    my_tags = ["[student] 4. announcements/subject  "]
    serializer_class = AnnouncementsReadSerializer

    def get_queryset(self):
        return Announcement.objects.select_related("subject").filter(
            subject__slug=self.kwargs.get("subject_slug")
        )


class NotesForStudentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Notes for the particular subject will be shown in decreasing order
    """

    my_tags = ["[student] 5. notes/subject"]
    serializer_class = NotesReadForStudentSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Notes.objects.select_related("subject", "posted_by", "posted_by__user")
            .prefetch_related("attached_files")
            .filter(subject__slug=self.kwargs.get("subject_slug"))
        )


# TODO: Add Assignment View
class AssignmentViewForStudentViewSet(
    ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    my_tags = ["[student] 6. assignments/subject"]
    serializer_class = AssignmentReadByStudentSerializer
    # parser_classes = [FormParser,MultiPartParser]

    def get_queryset(self):
        return Assignment.objects.select_related("subject").filter(
            subject__slug=self.kwargs.get("subject_slug")
        )


class AssignmentSubmissionByStudentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "head", "options"]
    my_tags = ["[student] 7. assignment submission"]
    serializer_class = AssignmentSubmissionWriteByStudent
    parser_classes = [
        FormParser,
        MultiPartParser,
    ]

    def get_queryset(self):
        # TODO:Dynamically find student id before submission
        student: Student = Student.objects.select_related("user").get(
            user__id=self.request.user.id
        )
        return AssignmentSubmission.objects.filter(
            assignment__id=self.kwargs.get("assignment_pk"), submitted_by=student.id
        )

    def get_serializer_context(self):
        return {
            "assignment_pk": self.kwargs.get("assignment_pk"),
            "user_id": self.request.user.id,
        }

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return AssignmentSubmissionWriteByStudent
        return AssignmentSubmissionReadByStudent
