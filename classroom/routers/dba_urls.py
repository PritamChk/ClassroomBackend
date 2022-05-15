from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from classroom.views.college_dba_view import CollegeCreateViewSet
from termcolor import cprint

college_create_router = DefaultRouter()
college_create_router.register(
    "college-create", CollegeCreateViewSet, basename="college"
)

dba_urlpatterns = []
dba_urlpatterns += college_create_router.urls

cprint("-------------------------------------------", "green")
cprint("DBA URLs -", "green")
cprint("-------------------------------------------", "green")
for url in dba_urlpatterns:
    cprint(url, "green")
