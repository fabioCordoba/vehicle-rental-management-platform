import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_BASE_URL = lambda: settings.VEHICLE_SERVICE_URL  # noqa: E731


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def get_vehicle(vehicle_id: str, token: str) -> dict | None:
    """Fetch a vehicle from the vehicle microservice. Returns None on error or not found."""
    try:
        response = requests.get(
            f"{_BASE_URL()}/api/transports/{vehicle_id}/",
            headers=_auth_headers(token),
            timeout=5,
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException as exc:
        logger.error("vehicle_client.get_vehicle error: %s", exc)
        return None


def toggle_vehicle_availability(vehicle_id: str, token: str) -> dict | None:
    """Toggle is_available on a vehicle. Returns updated vehicle data or None on failure."""
    try:
        response = requests.patch(
            f"{_BASE_URL()}/api/transports/{vehicle_id}/toggle-availability/",
            headers=_auth_headers(token),
            timeout=5,
        )
        if response.status_code == 200:
            return response.json()
        logger.error(
            "vehicle_client.toggle_vehicle_availability failed: %s %s",
            response.status_code,
            response.text,
        )
        return None
    except requests.RequestException as exc:
        logger.error("vehicle_client.toggle_vehicle_availability error: %s", exc)
        return None
