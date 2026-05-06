from rest_framework import serializers

from apps.authentication.models.role import HierarchyLevel, Role
from apps.users.models import User


class OrgAdminRegisterSerializer(serializers.ModelSerializer):
    """
    Registro público de Administrador cliente (org_admin).

    Cualquier persona puede registrarse como administrador de su propia
    organización. El rol org_admin se asigna automáticamente.
    No expone el campo `roles` para evitar escalada de privilegios.
    """

    password = serializers.CharField(write_only=True, min_length=5)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'password_confirmation',
        ]
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError(
                {'password_confirmation': 'Las contraseñas no coinciden.'}
            )
        attrs.pop('password_confirmation')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        try:
            supervisor_role = Role.objects.get(hierarchy_level=HierarchyLevel.SUPERVISOR)
            user.roles.add(supervisor_role)
        except Role.DoesNotExist:
            pass

        return user


# Alias para no romper imports existentes
UserRegisterSerializer = OrgAdminRegisterSerializer
