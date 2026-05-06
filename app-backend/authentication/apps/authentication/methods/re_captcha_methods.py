import requests
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_recaptcha(request):
    """
    Validate the recaptcha token

    Args:
        request (Request): The request object

    Returns:
        bool: True if the recaptcha token is valid, False otherwise
    """
    secret_key = settings.DRF_RECAPTCHA_SECRET_KEY
    data = {"response": request.data.get("g-recaptcha-response"), "secret": secret_key}
    resp = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=data, timeout=10
    )
    result_json = resp.json()

    if not result_json.get("success"):
        raise ValidationError({"error": "reCAPTCHA verification failed"})

    return True
