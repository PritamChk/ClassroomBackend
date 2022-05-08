from django.urls import include, path
from termcolor import cprint

from .routers.students_urls import stud_urlpatterns

urlpatterns = []
urlpatterns += stud_urlpatterns
