from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from classroom.views.college_dba_view import (
    AddOrDeleteOtherDBAViewSet,
    CollegeCreateViewSet,
    CollegeRetrieveForDBAViewSet,
    DBAProfileViewSet,
    ManageClassroomByDBAViewSet,
    TeacherManagementClassroomLevel,
)
from termcolor import cprint

college_create_router = DefaultRouter()
college_create_router.register(
    "college-create", CollegeCreateViewSet, basename="college"
)

dba_root_router = DefaultRouter()
dba_root_router.register("dba", DBAProfileViewSet, basename="dba")

college_for_dba_router = DefaultRouter()
college_for_dba_router.register(
    "college-dba", CollegeRetrieveForDBAViewSet, basename="college"
)

create_other_dba_router = NestedDefaultRouter(
    college_for_dba_router, "college-dba", lookup="college"
)
create_other_dba_router.register(
    "manage-dba", AddOrDeleteOtherDBAViewSet, basename="manage_dba"
)

classroom_create_router = NestedDefaultRouter(
    college_for_dba_router, "college-dba", lookup="college"
)
classroom_create_router.register(
    "classroom", ManageClassroomByDBAViewSet, basename="classroom"
)

allowed_teacher_classlevel_router = NestedDefaultRouter(
    classroom_create_router, "classroom", lookup="classroom"
)
allowed_teacher_classlevel_router.register(
    "manage-teacher",
    TeacherManagementClassroomLevel,
    basename="teacher_classroom",
)
allowed_student_classlevel_router = NestedDefaultRouter(
    classroom_create_router, "classroom", lookup="classroom"
)
allowed_student_classlevel_router.register(
    "manage-student",
    TeacherManagementClassroomLevel,
    basename="student_classroom",
)


dba_urlpatterns = []
dba_urlpatterns += (
    college_create_router.urls
    + dba_root_router.urls
    + college_for_dba_router.urls
    + create_other_dba_router.urls
    + classroom_create_router.urls
    + allowed_teacher_classlevel_router.urls
    + allowed_student_classlevel_router.urls
)

cprint("-------------------------------------------", "green")
cprint("DBA URLs -", "green")
cprint("-------------------------------------------", "green")
for url in dba_urlpatterns:
    cprint(url, "green")
