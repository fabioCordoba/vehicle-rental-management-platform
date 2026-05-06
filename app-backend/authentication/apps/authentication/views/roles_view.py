from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models.role import HierarchyLevel, Role
from apps.users.serializers.user_serializers import RoleSerializer


class AssignableRolesView(APIView):
    """
    GET /api/authentication/roles/

    Devuelve los roles que se pueden asignar al crear usuarios.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            roles = Role.objects.filter(is_active=True)
        else:
            roles = Role.objects.filter(
                hierarchy_level=HierarchyLevel.SUPERVISOR,
                is_active=True,
            )
        return Response(RoleSerializer(roles, many=True).data)
