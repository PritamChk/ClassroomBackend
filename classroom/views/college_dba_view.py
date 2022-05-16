from rest_framework import viewsets as _vs
from rest_framework import mixins as _mxn
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
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
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    queryset = College.objects.prefetch_related(
        "allowed_dbas", "allowed_teachers"
    ).all()
    serializer_class = CollegeCreateSerializer

    def get_serializer_context(self):
        return {"request": self.request}
