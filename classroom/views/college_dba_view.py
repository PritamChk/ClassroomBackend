from requests import request
from rest_framework import viewsets as _vset
from rest_framework import mixins as _mxn
from rest_framework.permissions import SAFE_METHODS
from rest_framework.parsers import MultiPartParser, FormParser
from classroom.models.classroom import (
    AllowedStudents,
    AllowedTeacherClassroomLevel,
    Classroom,
)
from classroom.models.college import AllowedCollegeDBA, AllowedTeacher, College, Stream
from classroom.models.college_dba import CollegeDBA
from classroom.models.imports import User
from classroom.serializers.college_dba import (
    AllowedCollegeDBACreateSerializer,
    AllowedStudentCreateSerializer,
    AllowedTeacherClassroomLevelCreateSerializer,
    AllowedTeacherCollegeLevelCreateSerializer,
    ClassroomCreateByDBASerializer,
    ClassroomReadByDBASerializer,
    CollegeCreateSerializer,
    CollegeDBAProfileSerializer,
    CollegeReadForDBASerializer,
    StreamReadWriteSerializer,
    StreamUpdateSerializer,
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


class StreamManagementViewSet(_vset.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "options", "head"]
    my_tags = ["[dba] 2. streams management"]

    def get_queryset(self):
        return Stream.objects.select_related("college", "dba", "dba__user").filter(
            college__slug=self.kwargs.get("college_slug")
        )

    def get_serializer_class(self):
        method = self.request.method
        if method == "PATCH":
            return StreamUpdateSerializer
        return StreamReadWriteSerializer

    def get_serializer_context(self):
        return {"college_slug": self.kwargs.get("college_slug")}


class DBAProfileViewSet(
    _mxn.ListModelMixin, _mxn.RetrieveModelMixin, _vset.GenericViewSet
):
    """
    # Get DBA Profile Details
    ---
        - all minimal user details will be sent along with college details
    """

    my_tags = ["[dba] 3. profile"]
    serializer_class = CollegeDBAProfileSerializer

    def get_queryset(self):
        return CollegeDBA.objects.select_related("user", "college").filter(
            pk=self.kwargs.get("pk")
        )


class CollegeRetrieveForDBAViewSet(_mxn.RetrieveModelMixin, _vset.GenericViewSet):
    swagger_schema = None
    my_tags = ["[dba] - college retrieve"]
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

    my_tags = ["[dba] 4. manage dbas by owner"]
    http_method_names = ["get", "post", "delete", "head", "options"]
    serializer_class = AllowedCollegeDBACreateSerializer

    def get_queryset(self):
        return AllowedCollegeDBA.objects.select_related("college").filter(
            college__slug=self.kwargs.get("college_slug")
        )

    def get_serializer_context(self):
        return {"college_slug": self.kwargs.get("college_slug")}


class ManageClassroomByDBAViewSet(_vset.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    my_tags = ["[dba] 5. classroom management"]
    lookup_field = "slug"
    parser_classes = [FormParser, MultiPartParser]

    def get_queryset(self):
        # TODO: filter classes w.r.t stream for a dba
        is_dba = User.objects.select_related("dba").filter(id=self.request.user.id)
        if is_dba.exists():
            dba: CollegeDBA = CollegeDBA.objects.select_related("user").get(
                user__id=self.request.user.id
            )
            if dba.is_owner:
                return (
                    Classroom.objects.prefetch_related("teachers")
                    .select_related("college")
                    .filter(college__slug=self.kwargs.get("college_slug"))
                )
            else:
                streams = (
                    Stream.objects.select_related("dba")
                    .values_list("title", flat=True)
                    .filter(dba=dba.id)
                )
                return (
                    Classroom.objects.prefetch_related("teachers")
                    .select_related("college")
                    .filter(
                        college__slug=self.kwargs.get("college_slug"),
                        stream__in=streams,
                    )
                )

    def get_serializer_class(self):
        method = self.request.method
        if method in SAFE_METHODS:
            return ClassroomReadByDBASerializer
        # elif method == "PATCH": #FIXME: NOT WORKING AS EXPECTED
        #     ClassroomUpdateByDBASerializer
        else:
            return ClassroomCreateByDBASerializer

    def get_serializer_context(self):
        return {"college_slug": self.kwargs.get("college_slug")}


class TeacherManagementCollegeLevel(
    _mxn.ListModelMixin,
    _mxn.RetrieveModelMixin,
    _mxn.CreateModelMixin,
    _mxn.DestroyModelMixin,
    _vset.GenericViewSet,
):
    """
    # This end point is to add teachers to college or remove them from that classroom
    """

    my_tags = ["[dba] 6. teacher management college level"]
    serializer_class = AllowedTeacherCollegeLevelCreateSerializer

    def get_queryset(self):
        return AllowedTeacher.objects.select_related("college").filter(
            college__slug=self.kwargs.get("college_slug")
        )

    def get_serializer_context(self):
        return {"college_slug": self.kwargs.get("college_slug")}


class TeacherManagementClassroomLevel(
    _mxn.ListModelMixin,
    _mxn.RetrieveModelMixin,
    _mxn.CreateModelMixin,
    _mxn.DestroyModelMixin,
    _vset.GenericViewSet,
):
    """
    # This end point is to add teachers to classroom or remove them from that classroom
    - Please let me know if Get method doesn't work
    """

    my_tags = ["[dba] 7. teacher/student management classroom level"]
    serializer_class = AllowedTeacherClassroomLevelCreateSerializer

    def get_queryset(self):
        return AllowedTeacherClassroomLevel.objects.select_related("classroom").filter(
            classroom__slug=self.kwargs.get("classroom_slug")
        )

    def get_serializer_context(self):
        return {"classroom_slug": self.kwargs.get("classroom_slug")}


class AllowedStudentManagementClassroomLevel(
    _mxn.ListModelMixin,
    _mxn.RetrieveModelMixin,
    _mxn.CreateModelMixin,
    _mxn.DestroyModelMixin,
    _vset.GenericViewSet,
):
    """
    # This end point is to add allowed students to classroom or remove them from that classroom
    """

    my_tags = ["[dba] 7. student management classroom level"]
    serializer_class = AllowedStudentCreateSerializer

    def get_queryset(self):
        return AllowedStudents.objects.select_related("classroom").filter(
            classroom__slug=self.kwargs.get("classroom_slug")
        )

    def get_serializer_context(self):
        return {"classroom_slug": self.kwargs.get("classroom_slug")}
