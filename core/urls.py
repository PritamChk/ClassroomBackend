# CORE>URLS
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# DRF_YASG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Classroom(LMS) API",
        default_version="0.1.0",
        description="""
        ## This is the **`Classroom API`** documentation
        
        > - ### Here all the api routes are grouped by tags
        > - ### First Migration done
        """,
        contact=openapi.Contact(email="django.dev.tmsl@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
# DRF_YASG


urlpatterns = [
    # path("classroom/", include("classroom.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("login/", include("djoser.urls.jwt")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
