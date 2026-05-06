from typing import Any, cast, Dict

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.authentication.models.role import HierarchyLevel, Role
from apps.users.models import User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "title", "code_name", "hierarchy_level"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer de lectura — incluye info de roles y organización."""

    roles = RoleSerializer(many=True, read_only=True)
    hierarchy_level = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "roles",
            "hierarchy_level",
            "image",
            "is_active",
        ]

    def get_hierarchy_level(self, obj):
        role = obj.roles.first()
        return role.hierarchy_level if role else None


class UserCreateByOrgAdminSerializer(serializers.ModelSerializer):
    """
    Serializer para que un org_admin cree usuarios subordinados
    (supervisor, employee, custom) dentro de su organización.
    """

    password = serializers.CharField(write_only=True, min_length=5)
    password_confirmation = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(
            hierarchy_level=HierarchyLevel.SUPERVISOR,
        ),
        write_only=True,
        help_text="UUID del rol (supervisor) a asignar.",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password_confirmation",
            "role",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Las contraseñas no coinciden."}
            )
        attrs.pop("password_confirmation")
        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.roles.add(role)
        return user


class UserCreateByPlatformAdminSerializer(serializers.ModelSerializer):
    """
    Serializer para que un platform_admin cree usuarios (org_admin u otros)
    en cualquier organización de la plataforma.
    """

    password = serializers.CharField(write_only=True, min_length=5)
    password_confirmation = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        write_only=True,
        help_text="UUID del rol a asignar.",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password_confirmation",
            "role",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Las contraseñas no coinciden."}
            )
        attrs.pop("password_confirmation")
        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.roles.add(role)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs) -> Dict[str, Any]:
        data = cast(Dict[str, Any], super().validate(attrs))
        user = self.user
        data["user"] = UserSerializer(user).data
        return data
