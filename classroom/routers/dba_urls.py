from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from classroom.views.college_dba_view import CollegeCreateViewSet, DBAProfileViewSet
from termcolor import cprint

college_create_router = DefaultRouter()
college_create_router.register(
    "college-create", CollegeCreateViewSet, basename="college"
)

dba_root_router = DefaultRouter()
dba_root_router.register("dba", DBAProfileViewSet, basename="dba")

dba_urlpatterns = []
dba_urlpatterns += college_create_router.urls + dba_root_router.urls

cprint("-------------------------------------------", "green")
cprint("DBA URLs -", "green")
cprint("-------------------------------------------", "green")
for url in dba_urlpatterns:
    cprint(url, "green")
