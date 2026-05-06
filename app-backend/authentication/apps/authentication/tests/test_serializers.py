import pytest
from unittest.mock import MagicMock

from apps.authentication.serializers.change_password_serializer import ChangePasswordSerializer
from apps.authentication.serializers.forgot_password_serializer import ForgotPasswordSerializer
from apps.authentication.serializers.register_serializer import OrgAdminRegisterSerializer


def _change_password_serializer(data, check_password_result=True):
    user = MagicMock()
    user.check_password.return_value = check_password_result
    request = MagicMock()
    request.user = user
    return ChangePasswordSerializer(data=data, context={"request": request})


def test_change_password_wrong_old_password_is_invalid():
    serializer = _change_password_serializer(
        data={
            "old_password": "WrongOld1!",
            "new_password": "NewPass1234!",
            "new_password_confirmation": "NewPass1234!",
        },
        check_password_result=False,
    )
    assert serializer.is_valid() is False


def test_change_password_new_passwords_mismatch_is_invalid():
    serializer = _change_password_serializer(
        data={
            "old_password": "OldPass1234!",
            "new_password": "NewPass1234!",
            "new_password_confirmation": "DifferentPass1234!",
        },
        check_password_result=True,
    )
    assert serializer.is_valid() is False


@pytest.mark.django_db
def test_forgot_password_nonexistent_email_is_invalid(db):
    serializer = ForgotPasswordSerializer(data={"email": "ghost@nowhere.com"})
    assert serializer.is_valid() is False


@pytest.mark.django_db
def test_register_password_mismatch_is_invalid():
    serializer = OrgAdminRegisterSerializer(
        data={
            "email": "org@test.com",
            "username": "orguser",
            "password": "Pass1234!",
            "password_confirmation": "OtherPass1234!",
        }
    )
    assert serializer.is_valid() is False
