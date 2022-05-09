# # -*- coding: utf-8 -*-
# from django.contrib import admin

# from .models import (
#     Announcement,
#     College,
#     Classroom,
#     Notes,
#     NotesAttachmentFile,
#     Student,
#     AllowedTeacher,
#     AllowedStudents,
#     Semester,
#     Subject,
#     Teacher,
# )


# @admin.register(College)
# class CollegeAdmin(admin.ModelAdmin):
#     list_display = ("name", "id", "city", "state", "address")
#     search_fields = ("name", "address", "city", "state")
#     list_filter = ["city", "state"]
#     readonly_fields = ["slug"]

#     # @admin.display() #FIXME: Show no of classrooms per college
#     # def no_of_classes(self, obj: College):
#     #     return (
#     #         College.objects.prefetch_related("classrooms")
#     #         .filter(id=obj.id)
#     #         .annotate(count=Count("classrooms"))
#     #         .get("count")
#     #     )


# @admin.register(Classroom)
# class ClassroomAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "id",
#         "level",
#         "stream",
#         "start_year",
#         "end_year",
#         "section",
#         "no_of_semesters",
#         "current_sem",
#         "created_at",
#         "college",
#     )
#     readonly_fields = ["slug"]
#     list_filter = (
#         "created_at",
#         "college",
#         "level",
#         "stream",
#         "start_year",
#         "end_year",
#         "section",
#         "no_of_semesters",
#         "current_sem",
#     )
#     search_fields = [
#         "title__icontains",
#         "title__istartswith",
#         "level__icontains",
#         "level__iexact",
#         "stream__icontains",
#         "stream__istartswith",
#         "section__iexact",
#     ]
#     list_select_related = ["college"]
#     autocomplete_fields = ["college"]
#     date_hierarchy = "created_at"


# @admin.register(Semester)
# class SemesterAdmin(admin.ModelAdmin):
#     list_display = ("id", "classroom", "sem_no", "is_current_sem")
#     list_filter = ("classroom", "is_current_sem", "classroom__college")
#     list_editable = ["is_current_sem"]
#     autocomplete_fields = ["classroom"]
#     list_select_related = ["classroom", "classroom__college"]
#     search_fields = [
#         "classroom__title__icontains",
#         "classroom__level__icontains",
#         "classroom__stream__icontains",
#     ]


# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "university_roll",
#         "id",
#         "first_name",
#         "last_name",
#         "college_name",
#         "classroom",
#     )
#     search_fields = [
#         "user__first_name__istartswith",
#         "user__last_name__istartswith",
#         "user__email__contains",
#         "classroom__stream__icontains",
#         "university_roll",
#         "classroom__level__iexact",
#     ]
#     list_filter = (
#         "classroom",
#         "classroom__college__name",
#         "classroom__level",
#         "classroom__stream",
#         "classroom__start_year",
#         "classroom__end_year",
#     )
#     autocomplete_fields = ["classroom", "user"]
#     list_select_related = ["user", "classroom", "classroom__college"]
#     readonly_fields = ["university_roll"]


# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ("id", "user")
#     list_filter = ("user", "classroom")
#     list_prefetch_related = ["classroom"]
#     list_select_related = ["user"]
#     autocomplete_fields = ["user", "classroom"]
#     raw_id_fields = ("classroom",)
#     search_fields = [
#         # "user",
#         "user__first_name__istartswith",
#         "user__last_name__istartswith",
#     ]


# @admin.register(AllowedTeacher)
# class AllowedTeacherAdmin(admin.ModelAdmin):
#     list_display = ("email", "id")
#     raw_id_fields = ("classrooms",)
#     list_prefetch_related = ["classrooms"]
#     autocomplete_fields = ["classrooms"]
#     list_filter = ["classrooms"]
#     search_fields = [
#         "email",
#         "classrooms__title__icontains",
#         "classrooms__stream__icontains",
#         "classrooms__level__icontains",
#         # "classrooms__college__name__istartswith", #FIXME:search in allowed teacher
#     ]


# @admin.register(AllowedStudents)
# class AllowedStudentsAdmin(admin.ModelAdmin):
#     list_display = ("email", "id", "university_roll", "classroom")
#     # list_editable = ["classroom"] #TODO: Open Later if needed
#     list_filter = ["classroom"]
#     raw_id_fields = ("classroom",)
#     list_select_related = ["classroom"]
#     autocomplete_fields = ["classroom"]
#     search_fields = ["university_roll", "email"]


# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = (
#         "slug",
#         "id",
#         "subject_code",
#         "title",
#         "subject_type",
#         "credit_points",
#         "semester",
#         "created_at",
#         "created_by",
#     )
#     list_filter = (
#         "semester",
#         "created_by",
#         "semester__classroom__title",
#         "credit_points",
#     )
#     search_fields = (
#         "slug",
#         "subject_code__istartswith",
#         "title__icontains",
#         "title__istartswith",
#     )
#     autocomplete_fields = ["semester", "created_by"]
#     list_select_related = ["semester", "created_by", "semester__classroom"]
#     date_hierarchy = "created_at"


# @admin.register(Announcement)
# class AnnouncementAdmin(admin.ModelAdmin):
#     list_display = (
#         "heading_short",
#         "id",
#         "body",
#         "created_at",
#         "updated_at",
#         "subject",
#         "posted_by",
#     )
#     list_filter = ("created_at", "updated_at", "subject", "posted_by")
#     list_select_related = ["subject", "posted_by"]
#     date_hierarchy = "created_at"
#     autocomplete_fields = ["subject", "posted_by"]
#     search_fields = ["heading__icontains", "heading__istartswith", "body__icontains"]


# class NotesAttachmentFileAdminInline(admin.TabularInline):
#     model = NotesAttachmentFile
#     min_num = 0
#     extra = 0


# @admin.register(Notes)
# class NotesAdmin(admin.ModelAdmin):
#     inlines = [NotesAttachmentFileAdminInline]
#     list_display = (
#         "id",
#         "slug",
#         "title",
#         "description",
#         "created_at",
#         "updated_at",
#         "subject",
#         "posted_by",
#     )
#     list_filter = ("created_at", "updated_at", "subject", "posted_by")
#     search_fields = ("slug",)
#     date_hierarchy = "created_at"


# @admin.register(NotesAttachmentFile)
# class NotesAttachmentFileAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "file_path", "created_at", "notes")
#     list_filter = ("created_at", "notes")
#     date_hierarchy = "created_at"
