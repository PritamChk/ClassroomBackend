from rest_framework.serializers import ModelSerializer as ms
from classroom.model import Student, User
from classroom.models.assignment import Assignment, AssignmentSubmission
from .classroom import ClassroomReadForStudentSerializer
from accounts.serializers import CurrentUserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status as code


class StudentUserReadSerializer(ms):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "contact_no", "email")


class StudentReadSerializer(ms):
    """
    Returns Student ID & User Profile along with Classroom Details
    """

    user = StudentUserReadSerializer()
    classroom = ClassroomReadForStudentSerializer()

    class Meta:
        model = Student
        fields = ("university_roll", "user", "classroom")
        # read_only_fields = "__all__"
        # depth = 1


# ---------------assignment read by student --------------------
class AssignmentReadByStudentSerializer(ms):
    """
    # Student can only view assignment and download the file
    """

    class Meta:
        model = Assignment
        fields = (
            "id",
            "title",
            "description",
            "alloted_marks",
            "attached_pdf",
            "due_date",
            "due_time",
            "created_at",
        )


# ---------------Assignment Submission Serializers ---------------
class AssignmentSubmissionReadByStudent(ms):
    class Meta:
        model = AssignmentSubmission
        fields = (
            "id",
            "answer_section",
            "submitted_file",
            "is_submitted",
            "submission_date",
            "submission_time",
            "score",
            "has_scored",
            "remarks",
            # "assignment",
            # "submitted_by",
            # "scored_by",
        )


class AssignmentSubmissionWriteByStudent(ms):
    class Meta:
        model = AssignmentSubmission
        fields = (
            "id",
            "answer_section",
            "submitted_file",
            "is_submitted",
            "submission_date",
            "submission_time",
            "has_scored",
            "submitted_by",
            # "score",
            # "assignment",
            # "remarks",
            # "scored_by",
        )
        read_only_fields = ["id", "submission_date", "submission_time", "has_scored"]

    def create(self, validated_data):
        assignment_pk = self.context.get("assignment_pk")
        try:
            assignment = Assignment.objects.get(id=assignment_pk)
        except:
            raise ValidationError("Assignment Not Found", code=code.HTTP_404_NOT_FOUND)
        try:
            self.instance = AssignmentSubmission.objects.create(
                assignment=assignment, **validated_data
            )
        except:
            raise ValidationError(
                "Assignment Submission Failed", code=code.HTTP_304_NOT_MODIFIED
            )
        return self.instance
