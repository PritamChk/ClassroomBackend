from rest_framework import serializers


class UserTypeSerializer(serializers.Serializer):
    # user_type = serializers.CharField(trim_whitespace=True)
    user_type = serializers.ChoiceField(
        choices=[
            ("student", "student"),
            ("teacher", "teacher"),
            ("college_dba", "college_dba"),
        ]
    )
    usertype_id = serializers.IntegerField()
