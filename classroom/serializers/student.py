from rest_framework.serializers import ModelSerializer as ms, FileField
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
    submitted_file = FileField(max_length=None, use_url=True, required=False)

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
            "assignment",
            # "submitted_by",
            # "scored_by",
        )
        read_only_fields = [
            "id",
            "submission_date",
            "submission_time",
            "score",
            "has_scored",
            "remarks",
            "assignment",
        ]


class AssignmentSubmissionWriteByStudent(ms):
    submitted_file = FileField(max_length=None, use_url=True, required=False)

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
        read_only_fields = [
            "id",
            "submission_date",
            "submission_time",
            "has_scored",
            "submitted_by",
        ]

    def create(self, validated_data):
        assignment_pk = self.context.get("assignment_pk")
        submitted_by = self.context.get("user_id")
        try:
            assignment = Assignment.objects.get(id=assignment_pk)
        except:
            raise ValidationError("Assignment Not Found", code=code.HTTP_404_NOT_FOUND)
        try:
            student: Student = Student.objects.select_related("user").get(
                user__id=submitted_by
            )
        except:
            raise ValidationError(
                "Student Profile Not Found", code=code.HTTP_404_NOT_FOUND
            )
        if AssignmentSubmission.objects.filter(
            assignment=assignment, submitted_by=student
        ).exists():
            raise ValidationError(
                "1 Submission Allowed Per Student", code=code.HTTP_400_BAD_REQUEST
            )

        try:
            self.instance = AssignmentSubmission.objects.create(
                assignment=assignment, submitted_by=student, **validated_data
            )
        except:
            raise ValidationError(
                "Assignment Submission Failed", code=code.HTTP_304_NOT_MODIFIED
            )
        return self.instance
