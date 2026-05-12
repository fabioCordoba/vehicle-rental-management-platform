import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _base_url() -> str:
    return settings.VEHICLE_SERVICE_URL.rstrip("/")


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# Sentinel values so callers can distinguish "not found" from "service down"
class VehicleNotFound(Exception):
    pass


class VehicleServiceUnavailable(Exception):
    pass


def get_vehicle(vehicle_id: str, token: str) -> dict:
    """
    Fetch a single vehicle from the vehicle microservice.

    Returns the vehicle dict on success.
    Raises VehicleNotFound (404) or VehicleServiceUnavailable (network / other error).
    """
    url = f"{_base_url()}/api/transports/{vehicle_id}/"
    try:
        response = requests.get(url, headers=_auth_headers(token), timeout=5)
    except requests.RequestException as exc:
        logger.error("vehicle_client.get_vehicle — connection error to %s: %s", url, exc)
        raise VehicleServiceUnavailable(str(exc)) from exc

    if response.status_code == 200:
        return response.json()

    logger.error(
        "vehicle_client.get_vehicle — unexpected status %s for %s: %s",
        response.status_code,
        url,
        response.text[:200],
    )
    if response.status_code == 404:
        raise VehicleNotFound(vehicle_id)
    raise VehicleServiceUnavailable(f"HTTP {response.status_code}")


def toggle_vehicle_availability(vehicle_id: str, token: str) -> dict | None:
    """Toggle is_available on a vehicle. Returns updated vehicle data or None on failure."""
    url = f"{_base_url()}/api/transports/{vehicle_id}/toggle-availability/"
    try:
        response = requests.patch(url, headers=_auth_headers(token), timeout=5)
    except requests.RequestException as exc:
        logger.error("vehicle_client.toggle_vehicle_availability — connection error: %s", exc)
        return None

    if response.status_code == 200:
        return response.json()

    logger.error(
        "vehicle_client.toggle_vehicle_availability — status %s: %s",
        response.status_code,
        response.text[:200],
    )
    return None
