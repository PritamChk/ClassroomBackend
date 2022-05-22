from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.serializers import (
    ModelSerializer as ms,
    SlugField,
    FileField,
)
from classroom.model import (
    College,
    Classroom,
    Notes,
    NotesAttachmentFile,
    Semester,
    Subject,
    Announcement,
    Teacher,
)
from django.shortcuts import get_object_or_404
from classroom.models.assignment import Assignment
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


class AnnouncementsPostOrUpdateSerializer(ms):
    class Meta:
        model = Announcement
        fields = (
            "id",
            "heading",
            "body",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        subject_slug = self.context.get("subject_slug")
        teacher_pk = self.context.get("teacher_pk")
        try:
            subject = Subject.objects.get(slug=subject_slug)
        except:
            raise NotFound(
                detail=f"Subject with slug- {subject_slug} does not exists",
                code=HTTP_404_NOT_FOUND,
            )
        try:
            teacher = Teacher.objects.get(pk=teacher_pk)
        except:
            raise NotFound(
                detail=f"Teacher with id - {teacher_pk} does not exists",
                code=HTTP_404_NOT_FOUND,
            )
        try:
            self.instance = Announcement.objects.create(
                posted_by=teacher, subject=subject, **validated_data
            )
            # TODO: on announcement send mass mail to allowed students of that class
        except:
            raise NotFound(
                detail=f"Subject Creation failed",
                code=HTTP_204_NO_CONTENT,
            )

        return self.instance


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


class SubjectRetrieveForTeacherSerializer(ms):
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
        read_only_fields = ["slug", "created_at"]


class SubjectCreateByTeacherSerializer(ms):
    class Meta:
        model = Subject
        fields = fields = [
            "id",
            "slug",
            "subject_code",
            "title",
            "subject_type",
            "credit_points",
            "created_at",
        ]
        read_only_field = ["id", "created_at", "slug"]

    def create(self, validated_data):

        created_by = self.context.get("created_by")
        semester_pk = self.context.get("sem_pk")
        try:
            sem = Semester.objects.get(pk=semester_pk)
        except:
            raise NotFound(
                detail=f"Semester_Pk - {semester_pk} does not exists",
                code=HTTP_404_NOT_FOUND,
            )
        try:
            teacher = Teacher.objects.get(pk=created_by)
        except:
            raise NotFound(
                detail=f"Teacher with id - {created_by} does not exists",
                code=HTTP_404_NOT_FOUND,
            )
        try:
            self.instance = Subject.objects.create(
                created_by=teacher, semester=sem, **validated_data
            )
        except:
            raise NotFound(
                detail=f"Subject Creation failed",
                code=HTTP_204_NO_CONTENT,
            )

        return self.instance


from rest_framework import serializers as _sz


class NotesFileUploadByTeacherSerializer(ms):
    file_path = FileField(max_length=None, use_url=True, required=True)

    class Meta:
        model = NotesAttachmentFile
        fields = ["id", "title", "file_path", "created_at"]
        read_only_fields = ["id", "title", "created_at"]

    def create(self, validated_data):
        notes_slug = self.context.get("notes_slug")
        try:
            notes = Notes.objects.get(slug=notes_slug)
        except:
            raise NotFound(
                detail=f"notes with slug - {notes_slug} does not exists",
                code=HTTP_404_NOT_FOUND,
            )

        try:
            self.instance = NotesAttachmentFile.objects.create(
                notes=notes, **validated_data
            )
        except:
            raise NotFound(
                detail=f"Subject Creation failed",
                code=HTTP_204_NO_CONTENT,
            )

        return self.instance


class NotesCreateForTeacherSerializer(ms):  # Combine this with Student Notes Read
    # attached_files = NotesFileUploadByTeacherSerializer(many=True, required=False)

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
            # "attached_files",
        )
        read_only_fields = [
            "slug",
            "created_at",
            "updated_at",
            "subject",
            "posted_by",
            # "attached_files",
        ]

    def create(self, validated_data):

        created_by = self.context.get("teacher_pk")
        subject_slug = self.context.get("subject_slug")
        try:
            subject = Subject.objects.get(slug=subject_slug)
        except:
            raise NotFound(
                detail=f"subject_slug - {subject_slug} does not exists",
                code=HTTP_404_NOT_FOUND,
            )
        try:
            teacher = Teacher.objects.get(pk=created_by)
        except:
            raise NotFound(
                detail=f"Teacher with id - {created_by} does not exists",
                code=HTTP_404_NOT_FOUND,
            )
        try:
            self.instance = Notes.objects.create(
                posted_by=teacher, subject=subject, **validated_data
            )
        except:
            raise NotFound(
                detail=f"Notes Creation failed",
                code=HTTP_204_NO_CONTENT,
            )

        return self.instance


class NotesUpdateForTeacherSerializer(ms):  # Combine this with Student Notes Read
    # attached_files = NotesFileUploadByTeacherSerializer(many=True, required=False)

    class Meta:
        model = Notes
        fields = (
            "title",
            "description",
        )
        read_only_fields = [
            "slug",
            "created_at",
            "updated_at",
        ]


class AssignmentPostByTeacherSerializer(ms):
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
        read_only_fields = ["id", "created_at"]
