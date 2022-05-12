from .routers.students_urls import stud_urlpatterns
from .routers.teacher_urls import teacher_urlpatterns

urlpatterns = []
urlpatterns += stud_urlpatterns+teacher_urlpatterns
