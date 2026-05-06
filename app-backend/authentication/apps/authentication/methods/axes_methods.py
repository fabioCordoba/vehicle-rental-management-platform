from apps.users.models.user import User


def get_axes_username_value(request, credentials):
    """
    Get the username value from the credentials
    """
    username = credentials.get("username", None)
    return credentials.get(User.USERNAME_FIELD, username)
