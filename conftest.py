"""
Main test configuration, used to fix fixture loading
"""


import pytest

from pytest_ansible_docker import AnsibleDockerTestinfraBackend


@pytest.fixture
def TestinfraBackend(request):
    """
    Entry point to boot and stop a docker image.
    """
    return AnsibleDockerTestinfraBackend(request)
