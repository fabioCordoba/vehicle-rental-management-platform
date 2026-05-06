import pytest

from apps.users.models import User


def test_username_field_is_email():
    assert User.USERNAME_FIELD == "email"


@pytest.mark.django_db
def test_created_by_defaults_to_null(db):
    user = User.objects.create_user(
        email="noparent@test.com",
        username="noparent",
        password="TestPass1234!",
    )
    assert user.created_by is None
