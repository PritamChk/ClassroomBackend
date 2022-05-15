from rest_framework import viewsets as _vs
from rest_framework import mixins as _mxn

from classroom.models.college import College
from classroom.serializers.college_dba import CollegeCreateSerializer


class CollegeCreateViewSet(
    _mxn.CreateModelMixin,
    _mxn.RetrieveModelMixin,
    _mxn.UpdateModelMixin,
    _vs.GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "head", "options"]
    my_tags = ["[college dba] - create/update college"]
    queryset = College.objects.prefetch_related("allowed_dbas", "allowed_teachers")
    serializer_class = CollegeCreateSerializer
