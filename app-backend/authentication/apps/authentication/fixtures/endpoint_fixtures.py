import logging

from django.db.models import Q
from drf_yasg.generators import EndpointEnumerator

from apps.authentication.constants.permissions_constants import IGNORED_ENDPOINTS
from apps.authentication.models.endpoint import Endpoint


def update_endpoints_and_permissions():
    """
    Create the endpoints and update the permissions with the new endpoints
    For endpoints removed it will delete the permissions
    """
    generator = EndpointEnumerator()
    endpoints = list(map(lambda url: url[0], generator.get_api_endpoints()))
    endpoints = list(
        filter(
            lambda filtered_endpoint: not filtered_endpoint.startswith(
                tuple(IGNORED_ENDPOINTS)
            ),
            endpoints,
        )
    )
    Endpoint.objects.filter(~Q(path__in=endpoints)).delete()
    for endpoint in endpoints:
        Endpoint.objects.get_or_create(path=endpoint)

    logging.info("Endpoints updated successfully!")
