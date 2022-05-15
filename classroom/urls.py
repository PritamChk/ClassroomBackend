from django.urls import path
from .routers.students_urls import stud_urlpatterns
from .routers.teacher_urls import teacher_urlpatterns
from .routers.dba_urls import dba_urlpatterns
from classroom.views.usertype_view import UserTypeAPIView

urlpatterns = [
    path("user-type/<uuid:id>", UserTypeAPIView.as_view(), name="user-category")
]
urlpatterns += stud_urlpatterns + teacher_urlpatterns + dba_urlpatterns
