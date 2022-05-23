# CORE>URLS
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# DRF_YASG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Classroom(LMS) API",
        default_version="1.0.0",
        description="""
        ## This is the **`Classroom API`** documentation
        
        > - ### Here all the api routes are grouped by tags
        > - ### Classroom, Teachers, DBA, Students, Routers configured
        """,
        contact=openapi.Contact(email="django.dev.tmsl@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
# DRF_YASG


urlpatterns = [
    path("classroom-app/", include("classroom.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("login/", include("djoser.urls.jwt")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

    # from termcolor import cprint
    # for url in urlpatterns:
    #     cprint(url,'blue')
    #     cprint('-------------------------------','blue')
