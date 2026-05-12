from rest_framework_simplejwt.authentication import JWTAuthentication


class RemoteUser:
    """
    Objeto de usuario ligero construido desde los claims del JWT.
    No requiere consulta a la base de datos del servicio de autenticación.
    """

    is_anonymous = False
    is_authenticated = True
    is_active = True

    def __init__(self, payload: dict):
        self.id = payload.get("user_id")
        self.pk = self.id
        self.email = payload.get("email", "")
        self.is_staff = payload.get("is_staff", False)
        self.is_superuser = payload.get("is_staff", False)
        self.role = payload.get("role", "")
        self.hierarchy_level = payload.get("hierarchy_level", "")

    def __str__(self):
        return self.email


class MicroserviceJWTAuthentication(JWTAuthentication):
    """
    Backend JWT para el vehicle service.

    Valida la firma del token (mismo SECRET_KEY que el auth service)
    y construye un RemoteUser desde los claims embebidos — sin consultar
    ninguna base de datos local.
    """

    def get_user(self, validated_token):
        return RemoteUser(validated_token)
