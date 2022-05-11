from rest_framework.serializers import ModelSerializer as ms, SlugField
from classroom.models import (
    College,
    Classroom,
    Notes,
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
        fields = ["classroom__slug", "sem_no", "is_current_sem"]
        select_related_fields = ["classroom"]


class ClassroomReadSerializer(ms):
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


class NotesReadForStudentSerializer(ms):
    posted_by = MinimalTeacherDetailsSerializer()
    subject = SlugField(source="subject.slug")

    class Meta:
        model = Notes
        fields = (
            "slug",
            "title",
            "description",
            "created_at",
            "updated_at",
            "subject",
            "posted_by",
        )
