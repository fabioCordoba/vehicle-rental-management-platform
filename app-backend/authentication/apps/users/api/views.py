from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models.role import HierarchyLevel
from apps.core.utils.send_mail import send_email
from apps.users.models import User
from apps.users.serializers.user_serializers import (
    UserCreateByOrgAdminSerializer,
    UserCreateByPlatformAdminSerializer,
    UserSerializer,
)


class SendEmailTest(APIView):

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        subject = 'Actualización de tu préstamo TEST'
        message = (
            f'Hola {user.first_name},\n\n'
            f'Se ha aplicado un interés mensual de ${0:,.2f} '
            f'a tu préstamo con codigo XXX.\n\n'
            f'Tu nuevo saldo de intereses es: ${0:,.2f}.\n'
            f'Tu saldo de capital es: ${0:,.2f}.\n\n'
            'Por favor mantente al día con tus pagos.'
        )
        try:
            response = send_email(user.email, subject, message)
            print(response)
        except Exception as e:
            print(f'Error enviando correo a {user.email}: {e}')
        return Response('Send Email Test')


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    CRUD de usuarios con visibilidad y permisos según jerarquía:

    - platform_admin (is_staff): ve y gestiona todos los usuarios de la plataforma.
    - org_admin: ve y gestiona usuarios (excluye a sí mismo).
      Puede crear usuarios con roles supervisor, employee o custom.
    - supervisor: solo puede listar empleados.
    - employee/custom: sin acceso.
    """

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return (
                User.objects.filter(is_active=True)
                .prefetch_related('roles')
                .distinct()
            )

        if user.roles.filter(hierarchy_level=HierarchyLevel.SUPERVISOR).exists():
            return (
                User.objects.filter(
                    roles__hierarchy_level=HierarchyLevel.SUPERVISOR,
                    is_active=True,
                )
                .exclude(id=user.id)
                .prefetch_related('roles')
                .distinct()
            )

        return User.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            if self.request.user.is_staff:
                return UserCreateByPlatformAdminSerializer
            return UserCreateByOrgAdminSerializer
        return UserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response(
            {'detail': f'El usuario {user.username} ha sido desactivado.'},
            status=status.HTTP_200_OK,
        )


class UserSearchView(generics.ListAPIView):
    """
    Búsqueda de usuarios con visibilidad jerárquica.
    Filtra por field=<campo>&value=<valor>.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    ALLOWED_FIELDS = ['username', 'email', 'first_name', 'last_name', 'created_at']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = User.objects.filter(is_active=True).prefetch_related('roles')
        elif user.roles.filter(hierarchy_level=HierarchyLevel.SUPERVISOR).exists():
            queryset = User.objects.filter(
                roles__hierarchy_level=HierarchyLevel.SUPERVISOR,
                is_active=True,
            ).exclude(id=user.id).prefetch_related('roles')
        else:
            return User.objects.none()

        field = self.request.query_params.get('field')
        value = self.request.query_params.get('value')
        if field in self.ALLOWED_FIELDS and value:
            queryset = queryset.filter(**{f'{field}__icontains': value})

        return queryset.distinct()
