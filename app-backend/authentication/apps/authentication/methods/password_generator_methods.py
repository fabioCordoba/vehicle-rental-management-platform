import random
import string

ALLOWED_SYMBOLS = "~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/"


def generate_password(length=8):
    """
    Generate a random password with the given length.
    :param length: The length of the password to generate.
    :return: A random password with the given length.
    """
    if length < 8:  # pragma: no cover
        raise ValueError("Password length must be at least 8 characters.")

    two_random_uppercase = random.choices(string.ascii_uppercase, k=2)
    two_random_digits = random.choices(string.digits, k=2)
    two_random_symbols = random.choices(ALLOWED_SYMBOLS, k=2)
    random_password = (
        two_random_uppercase
        + two_random_digits
        + two_random_symbols
        + random.choices(string.ascii_lowercase, k=length - 6)
    )
    random.shuffle(random_password)
    return "".join(random_password)
