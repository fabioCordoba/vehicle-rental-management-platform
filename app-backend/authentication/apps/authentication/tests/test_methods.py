import string

from apps.authentication.methods.password_generator_methods import generate_password


def test_generate_password_has_correct_length():
    assert len(generate_password(10)) == 10


def test_generate_password_contains_uppercase():
    password = generate_password(10)
    assert any(c in string.ascii_uppercase for c in password)
