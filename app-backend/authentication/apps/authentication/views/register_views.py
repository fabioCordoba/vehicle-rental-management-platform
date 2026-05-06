from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.serializers.register_serializer import OrgAdminRegisterSerializer
from apps.users.serializers.user_serializers import UserSerializer


class RegisterView(APIView):
    """
    Registro público de Administrador cliente (org_admin).

    - Cualquier persona puede registrarse: no requiere autenticación.
    - El rol org_admin se asigna automáticamente (si existe en BD).
    - Retorna tokens JWT listos para usar, igual que el endpoint de login.
    - Para crear org_admins desde el panel técnico usar POST /api/users/.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Registro de Administrador cliente',
        operation_description=(
            'Crea una cuenta de tipo org_admin (administrador de organización). '
            'El campo `roles` no es aceptado; el rol se asigna automáticamente.'
        ),
        request_body=OrgAdminRegisterSerializer,
        responses={
            201: openapi.Response('Usuario creado', OrgAdminRegisterSerializer),
            400: 'Datos inválidos.',
        },
    )
    def post(self, request):
        serializer = OrgAdminRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )
