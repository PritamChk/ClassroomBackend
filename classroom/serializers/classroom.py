from rest_framework.serializers import (
    ModelSerializer as ms,
    SlugField,
    FilePathField,
    FileField,
)
from classroom.models import (
    College,
    Classroom,
    Notes,
    NotesAttachmentFile,
    Semester,
    Subject,
    Announcement,
    Teacher,
)
from classroom.serializers.teacher import (
    MinimalTeacherDetailsSerializer,
    MinimalUserDetailsSerializer,
    TeacherReadForSubjectSerializer,
)


class CollegeReadSerializer(ms):
    class Meta:
        model = College
        fields = ["id", "slug", "name", "city", "state", "address"]


class SemesterReadSerializer(ms):
    classroom__slug = SlugField(source="classroom.slug")

    class Meta:
        model = Semester
        fields = [
            "id",
            "classroom__slug",  # TODO:If req then open
            "sem_no",
            "is_current_sem",
        ]
        select_related_fields = ["classroom"]


class ClassroomReadForStudentSerializer(ms):
    college = CollegeReadSerializer()

    class Meta:
        model = Classroom
        fields = (
            "slug",
            "title",
            "level",
            "stream",
            "start_year",
            "end_year",
            "section",
            "no_of_semesters",
            "current_sem",
            "created_at",
            "college",
        )


class ClassroomReadForTeacherSerializer(ms):
    college = CollegeReadSerializer()
    semesters_list = SemesterReadSerializer(source="semesters", many=True)

    class Meta:
        model = Classroom
        fields = (
            "slug",
            "title",
            "level",
            "stream",
            "start_year",
            "end_year",
            "section",
            "no_of_semesters",
            "current_sem",
            "semesters_list",
            "created_at",
            "college",
        )


class SubjectReadSerializer(ms):
    created_by = TeacherReadForSubjectSerializer()

    class Meta:
        model = Subject
        fields = (
            "slug",
            "subject_code",
            "title",
            "subject_type",
            "credit_points",
            "created_at",
            "created_by",
        )


class AnnouncementsReadSerializer(ms):
    class Meta:
        model = Announcement
        fields = (
            "id",
            "heading",
            "body",
            "created_at",
            "updated_at",
        )


class NotesFileReadByStudentSerializer(ms):
    file_path = FileField(max_length=None, use_url=True, required=False)

    class Meta:
        model = NotesAttachmentFile
        fields = ["title", "file_path", "created_at"]


class NotesReadForStudentSerializer(ms):
    posted_by = MinimalTeacherDetailsSerializer()
    subject_slug = SlugField(source="subject.slug")
    attached_files = NotesFileReadByStudentSerializer(many=True)

    class Meta:
        model = Notes
        fields = (
            "slug",
            "title",
            "description",
            "created_at",
            "updated_at",
            "subject_slug",
            "posted_by",
            "attached_files",
        )
        # depth = 1


class SubjectRetriveForTeacherSerializer(ms):
    class Meta:
        model = Subject
        fields = [
            "slug",
            "subject_code",
            "title",
            "subject_type",
            "credit_points",
            "created_at",
        ]
        readonly_fields = ["slug", "created_at"]


class SubjectCreateByTeacherSerializer(ms):
    class Meta:
        model = Subject
        fields = fields = [
            "subject_code",
            "title",
            "subject_type",
            "credit_points",
            "created_at",
            "semester",
            "created_by",
        ]
