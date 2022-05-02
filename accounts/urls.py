"""
CORE URLS
"""
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',test,name="test-url"),
]
