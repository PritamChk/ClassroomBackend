from rest_framework.serializers import ModelSerializer as ms
from classroom.models import College, Classroom, Semester, Subject, Announcement, Teacher
from classroom.serializers.teacher import TeacherReadForSubjectSerializer


class CollegeReadSerializer(ms):
    class Meta:
        model = College
        fields = ["id", "slug", "name", "city", "state", "address"]


class SemesterReadSerializer(ms):
    class Meta:
        model = Semester
        fields = "__all__"


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
        # depth=2
        # select_related_fields = ["college"] #FIXME: This won't work
        # prefetch_related_fields = ["semesters"] #FIXME: This won't work


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
