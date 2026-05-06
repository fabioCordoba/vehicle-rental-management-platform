import random
import re
import string
import uuid

from django.core.exceptions import ImproperlyConfigured

from alternova_351conversion.testing import is_in_testing_session
from apps.authentication.constants.permissions_constants import MethodOptions
from apps.authentication.fixtures.endpoint_fixtures import (
    update_endpoints_and_permissions,
)
from apps.authentication.models.endpoint import Endpoint
from apps.authentication.models.permission import Permission
from apps.authentication.models.permission_group import PermissionGroup
from apps.authentication.models.permission_resource import PermissionResource


def create_endpoint_permission_group(allowed_patterns_regex=None):
    """
    Create a test group with permissions for the endpoints that match the allowed patterns

    :param allowed_patterns_regex: List of regex patterns to match the endpoints
    :return: Role
    """
    if not is_in_testing_session():
        raise ImproperlyConfigured(
            "This function should only be called in the test environment"
        )

    update_endpoints_and_permissions()
    endpoints = Endpoint.objects.all()
    test_group, _ = PermissionGroup.objects.get_or_create(
        title="Test Group", code_name="test_group"
    )
    for endpoint in endpoints:
        if allowed_patterns_regex and not any(
            re.match(regex, endpoint.path) for regex in allowed_patterns_regex
        ):
            continue

        code_name = "test_" + "".join(
            random.choice(string.ascii_lowercase) for _ in range(5)
        )
        test_resource, _ = PermissionResource.objects.get_or_create(
            title="Test Resource", code_name=code_name
        )

        for method in MethodOptions.choices:
            code_name = f"view{method[0]}_{str(uuid.uuid4())}"
            permission, _ = Permission.objects.get_or_create(
                title=endpoint.path,
                code_name=code_name,
                resource=test_resource,
                action=method[1],
                method=method[0],
                endpoint=endpoint,
            )
            test_group.permissions.add(permission)

    return test_group
