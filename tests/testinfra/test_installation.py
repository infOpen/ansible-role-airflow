"""
Role tests
"""
import pytest

# To mark all the tests as destructive:
# pytestmark = pytest.mark.destructive

# To run all the tests on given docker images:
pytestmark = pytest.mark.docker_images('infopen/ubuntu-trusty-ssh')
# pytestmark = pytest.mark.docker_images('infopen/ubuntu-trusty-ssh',
#                                       'infopen/ubuntu-xenial-ssh')

# Both
# pytestmark = [
#     pytest.mark.destructive,
#     pytest.mark.docker_images("debian:jessie", "centos:7")
# ]


def test_airflow_user(User):
    """
    Tests about airflow user configuration
    """
    airflow_user = User('airflow')

    assert airflow_user.exists is True
    assert airflow_user.group == 'airflow'
    assert airflow_user.home == '/var/lib/airflow'
    assert airflow_user.shell == '/bin/false'


def test_airflow_group(Group):
    """
    Tests about airflow group configuration
    """

    assert Group('airflow').exists is True


def test_prerequisites_packages(Package):
    """
    Tests about airflow prerequisites packages
    """

    prerequisites = [
        'python3.4-dev', 'libpq-dev', 'libssl-dev', 'libffi-dev',
        'build-essential', 'python-virtualenv', 'python-pip'
    ]

    for prerequisite in prerequisites:
        assert Package(prerequisite).is_installed is True


def test_airflow_processes(Process):
    """
    Test about airflow processes
    """

    assert len(Process.get(user='airflow', comm='airflow')) >= 2


def test_airflow_services(Service):
    """
    Test about airflow services
    """

    for service in ['airflow-webserver', 'airflow-scheduler']:
        service = Service(service)

        assert service.is_running
        assert service.is_enabled
