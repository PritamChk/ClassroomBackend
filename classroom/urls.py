from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views.student_view import user_category

from .views.student_view import StudentViewSet

# from .views.student_view import DynamicRetriveUser

student_router = DefaultRouter()
student_router.register("student", StudentViewSet, "student")

urlpatterns = [
    path("user-type/<uuid:id>", user_category, name="user-category")
    # path("user-type/<uuid:id>", DynamicRetriveUser.as_view())
]

urlpatterns += student_router.urls
