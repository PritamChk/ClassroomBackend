from djoser.serializers import (
    UserSerializer as usz,
    UsernameResetConfirmSerializer as uname_reset,
)

class UseranmeResetConfirmSerializer(uname_reset):
    class Meta(uname_reset.Meta):
        fields = ('uid','token','email')

class CurrentUserSerializer(usz):
    """
    description: This will be returned after login authentication
    """

    class Meta(usz.Meta):
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "contact_no",
            "is_active",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("id", "email", "is_active", "date_joined", "last_login")
