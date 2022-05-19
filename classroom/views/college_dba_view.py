from rest_framework import viewsets as _vset
from rest_framework import mixins as _mxn
from rest_framework import views as _vws
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from classroom.models.college import AllowedCollegeDBA, College
from classroom.models.college_dba import CollegeDBA
from classroom.serializers.college_dba import (
    AllowedCollegeDBACreateSerializer,
    AllowedCollegeDBAReadSerializer,
    CollegeCreateSerializer,
    CollegeDBAProfileSerializer,
    CollegeReadForDBASerializer,
)
from termcolor import cprint


class CollegeCreateViewSet(
    _mxn.CreateModelMixin,
    _mxn.RetrieveModelMixin,
    _mxn.UpdateModelMixin,
    _vset.GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "head", "options"]
    my_tags = ["[dba] 1. create/update college"]
    parser_classes = [FormParser, MultiPartParser]
    queryset = College.objects.prefetch_related("allowed_dbas").all()
    serializer_class = CollegeCreateSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        data = request.data
        cprint(f"DATA\n-->\n {data}", "green")
        return super().create(request, *args, **kwargs)


class DBAProfileViewSet(_mxn.RetrieveModelMixin, _vset.GenericViewSet):
    """
    # Get DBA Profile Details
    ---
        - all minimal user details will be sent along with college details
    """

    my_tags = ["[dba] 2. profile"]
    serializer_class = CollegeDBAProfileSerializer

    def get_queryset(self):
        return CollegeDBA.objects.select_related("user", "college").filter(
            pk=self.kwargs.get("pk")
        )


class CollegeRetrieveForDBAViewSet(_mxn.RetrieveModelMixin, _vset.GenericViewSet):
    swagger_schema = None
    serializer_class = CollegeReadForDBASerializer
    lookup_field = "slug"

    def get_queryset(self):
        return College.objects.all()


class AddOrDeleteOtherDBAViewSet(_vset.ModelViewSet):
    """
    # Only owner admin will be able to add/delete other DBAs for classroom management
    ---
    > permissions will be checked initially in frontend
    """

    my_tags = ["[dba] 3. manage dbas by owner"]
    http_method_names = ["get", "post", "delete", "head", "options"]
    serializer_class = AllowedCollegeDBACreateSerializer

    def get_queryset(self):
        return AllowedCollegeDBA.objects.select_related("college").filter(
            college__slug=self.kwargs.get("college_slug")
        )

    def get_serializer_context(self):
        return {"college_slug": self.kwargs.get("college_slug")}
