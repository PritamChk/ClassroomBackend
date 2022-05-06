from rest_framework.serializers import ModelSerializer as ms
from classroom.models import College, Classroom,Semester


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
    semesters = SemesterReadSerializer(many=True)
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
            "semesters"
            "created_at",
            "college",
        )
        select_related_fields = ["college"] #FIXME: This won't work
        prefetch_related_fields = ["semesters"] #FIXME: This won't work
