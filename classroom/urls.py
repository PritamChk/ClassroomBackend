from rest_framework.routers import DefaultRouter
from .views import *

student_router = DefaultRouter()
student_router.register('student',StudentViewSet,'student')

urlpatterns = student_router.urls