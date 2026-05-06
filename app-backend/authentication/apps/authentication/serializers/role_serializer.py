from rest_framework.serializers import ModelSerializer

from apps.authentication.models.role import Role


class RoleShortSerializer(ModelSerializer):
    """
    Role short serializer

    This serializer is used to serialize the Role model in a short format.
    """

    class Meta:
        model = Role
        fields = ["id", "title", "code_name"]
