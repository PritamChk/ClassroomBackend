from rest_framework import viewsets as _vset
from rest_framework import mixins as _mxn
from rest_framework import views as _vws
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from classroom.models.college import College
from classroom.serializers.college_dba import (
    CollegeCreateSerializer,
)
from termcolor import cprint


class CollegeCreateViewSet(
    _mxn.CreateModelMixin,
    _mxn.RetrieveModelMixin,
    _mxn.UpdateModelMixin,
    _vset.GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "head", "options"]
    my_tags = ["[college dba] - create/update college"]
    parser_classes = [FormParser, MultiPartParser]
    queryset = College.objects.prefetch_related("allowed_dbas").all()
    serializer_class = CollegeCreateSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        data = request.data
        cprint(f"DATA\n-->\n {data}", "green")
        return super().create(request, *args, **kwargs)


class DBAExistsView(_mxn.RetrieveModelMixin, _vset.GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


