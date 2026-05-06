from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.authentication.models.email_device import EmailDevice
from apps.common.methods.send_email import send_email


def send_otp_email(user, token):
    """
    Sends an email with the OTP token to the user
    """
    subject = "351 Conversion - Verification Code"
    html_message = render_to_string(
        "frontend/authentication/email/two_factor_code.html",
        {
            "user": user,
            "token": token,
        },
    )
    plain_message = strip_tags(html_message)
    return send_email(
        subject,
        plain_message,
        [user.email],
        "frontend/authentication/email/two_factor_code.html",
        settings.DEFAULT_FROM_EMAIL,
    )


def get_or_create_email_device(user, confirmed=False):
    """
    Gets or creates an email device for the user
    """
    device, created = EmailDevice.objects.get_or_create(
        user=user, name="email", defaults={"confirmed": confirmed}
    )
    return device


def verify_token(user, token):
    """
    Verifies if the provided token is valid for the user
    """
    try:
        device = EmailDevice.objects.get(user=user, name="email", confirmed=True)
        return device.verify_token(token)
    except EmailDevice.DoesNotExist:
        return False
