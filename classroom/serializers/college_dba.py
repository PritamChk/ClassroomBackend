from django.db.transaction import atomic
from numpy import source
from rest_framework import serializers as _sz
from rest_framework.exceptions import ValidationError as _error
from rest_framework.serializers import ModelSerializer as _ms
from rest_framework.status import HTTP_409_CONFLICT, HTTP_412_PRECONDITION_FAILED

from classroom.models.college import AllowedCollegeDBA, College
from classroom.models.college_dba import CollegeDBA
from classroom.serializers.teacher import MinimalUserDetailsSerializer


class AllowedCollegeDBAReadSerializer(_ms):
    college = _sz.SlugRelatedField("college.slug", read_only=True)

    class Meta:
        model = AllowedCollegeDBA
        fields = ["id", "email", "college"]


class AllowedCollegeDBACreateSerializer(_ms):
    college_slug = _sz.SlugField(source="college.slug", read_only=True)

    class Meta:
        model = AllowedCollegeDBA
        fields = ["id", "email", "college_slug"]
        read_only_fields = ["id", "college_slug"]


class CollegeCreateSerializer(_ms):
    allowed_teacher_list = _sz.FileField(max_length=None, use_url=True, required=False)

    class Meta:
        model = College
        fields = [
            "slug",
            "name",
            "city",
            "state",
            "address",
            "allowed_teacher_list",
            "allowed_dba_list",
        ]
        read_only_fields = ["slug"]


class CollegeDBAProfile(_sz.ModelSerializer):
    user = MinimalUserDetailsSerializer()
    college = College
    class Meta:
        model = CollegeDBA
        fields = ('user', 'college')