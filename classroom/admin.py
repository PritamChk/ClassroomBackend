# -*- coding: utf-8 -*-
from django.contrib import admin

from classroom.models.college_dba import CollegeDBA

from .model import (
    AllowedTeacherClassroomLevel,
    Announcement,
    College,
    Classroom,
    Notes,
    NotesAttachmentFile,
    Student,
    AllowedTeacher,
    AllowedStudents,
    Semester,
    Subject,
    Teacher,
)


class AllowedTeacherInline(admin.StackedInline):
    model = AllowedTeacher
    min_num = 0
    extra = 0


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "name",
        "id",
        "city",
        "state",
        "address",
        "allowed_teacher_list",
    )
    search_fields = (
        "name",
        "address__icontains",
        "city",
        "state",
    )
    inlines = [AllowedTeacherInline]
    list_display_links = ["slug", "name"]
    list_filter = ["city", "state"]
    readonly_fields = ["slug"]


@admin.register(AllowedTeacher)
class AllowedTeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "college")
    list_display_links = ["id", "email"]
    list_select_related = ["college"]
    autocomplete_fields = ["college"]
    list_filter = ["college"]
    search_fields = [
        "email",
        "college__name__icontains",
        "college__name__istartswith",
        "college__city__istartswith",
        "college__state__icontains",
    ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["id", "get_first_name", "get_last_name", "user", "college"]
    list_display_links = ["id", "get_first_name", "user"]
    list_filter = ("user", "college", "classrooms__title")
    list_prefetch_related = ["classrooms"]
    list_select_related = ["user", "college"]
    autocomplete_fields = [
        "user",
        "classrooms",
        "college",
    ]
    search_fields = [
        "user__first_name__istartswith",
        "user__last_name__istartswith",
        "college",
        "classrooms",
    ]


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "title",
        "level",
        "stream",
        "start_year",
        "end_year",
        "section",
        "no_of_semesters",
        "current_sem",
        "college",
        "get_teachers",
        "id",
    )
    list_display_links = ["slug", "title", "id"]
    readonly_fields = ["slug"]
    list_filter = (
        "created_at",
        "college",
        "teachers",
        "level",
        "stream",
        "start_year",
        "end_year",
        "section",
        "no_of_semesters",
        "current_sem",
    )
    search_fields = [
        "title__icontains",
        # "title",
        "level__icontains",
        # "level",
        "stream__icontains",
        # "stream",
        "section",
    ]
    list_select_related = ["college"]
    list_prefetch_related = ["teachers__id"]
    autocomplete_fields = ["college", "teachers"]
    date_hierarchy = "created_at"

    def get_teachers(self, obj):
        return "\n".join([t.user.email for t in obj.teachers.all()])


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("id", "classroom", "sem_no", "is_current_sem")
    list_filter = ("classroom", "is_current_sem", "classroom__college")
    list_editable = ["is_current_sem"]
    autocomplete_fields = ["classroom"]
    list_select_related = ["classroom", "classroom__college"]
    search_fields = [
        "classroom__title__icontains",
        "classroom__level__icontains",
        "classroom__stream__icontains",
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "university_roll",
        "id",
        "first_name",
        "last_name",
        "college_name",
        "classroom",
    )
    search_fields = [
        "user__first_name__istartswith",
        "user__last_name__istartswith",
        "user__email__contains",
        "classroom__stream__icontains",
        "university_roll",
        "classroom__level__iexact",
    ]
    list_filter = (
        "classroom",
        "classroom__college__name",
        "classroom__level",
        "classroom__stream",
        "classroom__start_year",
        "classroom__end_year",
    )
    autocomplete_fields = ["classroom", "user"]
    list_select_related = ["user", "classroom", "classroom__college"]
    list_display_links = ["user", "first_name"]
    readonly_fields = ["university_roll"]


@admin.register(AllowedStudents)
class AllowedStudentsAdmin(admin.ModelAdmin):
    list_display = ("email", "id", "university_roll", "classroom")
    # list_editable = ["classroom"] #TODO: Open Later if needed
    list_filter = ["classroom"]
    raw_id_fields = ("classroom",)
    list_select_related = ["classroom"]
    autocomplete_fields = ["classroom"]
    search_fields = ["university_roll", "email"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "id",
        "subject_code",
        "title",
        "subject_type",
        "credit_points",
        "semester",
        "created_at",
        "created_by",
    )
    list_filter = (
        "semester",
        "created_by",
        "semester__classroom__title",
        "credit_points",
    )
    search_fields = (
        "slug",
        "subject_code__istartswith",
        "title__icontains",
        "title__istartswith",
    )
    autocomplete_fields = ["semester", "created_by"]
    list_select_related = ["semester", "created_by", "semester__classroom"]
    date_hierarchy = "created_at"


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "heading_short",
        "id",
        "body",
        "created_at",
        "updated_at",
        "subject",
        "posted_by",
    )
    list_filter = ("created_at", "updated_at", "subject", "posted_by")
    list_select_related = ["subject", "posted_by"]
    date_hierarchy = "created_at"
    autocomplete_fields = ["subject", "posted_by"]
    search_fields = ["heading__icontains", "heading__istartswith", "body__icontains"]


class NotesAttachmentFileAdminInline(admin.TabularInline):
    model = NotesAttachmentFile
    min_num = 0
    extra = 0


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    inlines = [NotesAttachmentFileAdminInline]
    list_display = (
        "id",
        "slug",
        "title",
        "short_description",
        "created_at",
        "updated_at",
        "subject",
        "posted_by",
    )
    list_display_links = ["slug", "title"]
    list_filter = ("created_at", "updated_at", "subject", "posted_by")
    search_fields = ("slug",)
    date_hierarchy = "created_at"


@admin.register(NotesAttachmentFile)
class NotesAttachmentFileAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "file_path", "created_at", "notes")
    list_display_links = ["title"]
    list_filter = ("created_at", "notes")
    date_hierarchy = "created_at"


@admin.register(AllowedTeacherClassroomLevel)
class AllowedTeacherClassroomLevelAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "classroom")
    list_display_links = ["email"]
    search_fields = ["email", "classroom"]
    list_filter = ("classroom",)

@admin.register(CollegeDBA)
class CollegeDBAAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'college')
    list_filter = ('user', 'college')