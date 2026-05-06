from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.authentication.models.role import HierarchyLevel, Role

User = get_user_model()

SYSTEM_ROLES = [
    {
        "title": "Platform Admin",
        "code_name": "platform_admin",
        "hierarchy_level": HierarchyLevel.PLATFORM_ADMIN,
    },
    {
        "title": "Supervisor",
        "code_name": "supervisor",
        "hierarchy_level": HierarchyLevel.SUPERVISOR,
    },
]

TEST_USERS = [
    {
        "username": "platform_admin",
        "email": "platform@bull.test",
        "password": "Bull2024!",
        "first_name": "Platform",
        "last_name": "Admin",
        "is_staff": True,
        "is_superuser": True,
        "role_code": "platform_admin",
    },
    {
        "username": "supervisor",
        "email": "supervisor@bull.test",
        "password": "Bull2024!",
        "first_name": "María",
        "last_name": "López",
        "is_staff": False,
        "is_superuser": False,
        "role_code": "supervisor",
    },
]


class Command(BaseCommand):

    help = (
        "Crea los roles del sistema (jerarquía completa) y usuarios "
        "de prueba para cada nivel. Seguro de ejecutar varias veces (idempotente)."
    )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Seed inicial ===\n"))

        roles = self._create_roles()
        self._create_users(roles)

        self.stdout.write(self.style.SUCCESS("\n✔  Seed completado.\n"))

    def _create_roles(self) -> dict:
        self.stdout.write(self.style.MIGRATE_HEADING("[ Roles ]"))
        role_map = {}

        for data in SYSTEM_ROLES:
            obj, created = Role.objects.get_or_create(
                code_name=data["code_name"],
                defaults={
                    "title": data["title"],
                    "hierarchy_level": data["hierarchy_level"],
                },
            )

            if not created and obj.hierarchy_level != data["hierarchy_level"]:
                obj.hierarchy_level = data["hierarchy_level"]
                obj.save(update_fields=["hierarchy_level"])
                self.stdout.write(
                    self.style.WARNING(
                        f"  ↻  {obj.title} — hierarchy_level actualizado"
                    )
                )
            elif created:
                self.stdout.write(self.style.SUCCESS(f"  ✔  {obj.title} creado"))
            else:
                self.stdout.write(f"  –  {obj.title} ya existe")

            role_map[obj.code_name] = obj

        return role_map

    def _create_users(self, role_map: dict) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("\n[ Usuarios de prueba ]"))

        for data in TEST_USERS:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "username": data["username"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_staff": data["is_staff"],
                    "is_superuser": data["is_superuser"],
                },
            )

            if not created:
                self.stdout.write(f"  –  {data['email']} ya existe")
                continue

            user.set_password(data["password"])
            user.save(update_fields=["password"])

            role = role_map.get(data["role_code"])
            if role:
                user.roles.add(role)

            level_label = role.get_hierarchy_level_display() if role else "sin rol"
            self.stdout.write(
                self.style.SUCCESS(f"  ✔  {data['email']} — {level_label}")
            )

        self.stdout.write(self.style.MIGRATE_HEADING("\n[ Credenciales de prueba ]"))
