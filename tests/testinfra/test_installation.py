"""
Role tests
"""
import pytest

pytestmark = pytest.mark.docker_images('infopen/ubuntu-trusty-ssh')


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


def test_airflow_pid_folder(File):
    """
    PID folder should exists
    """

    pid_folder = File('/var/run/airflow')

    assert pid_folder.exists is True
    assert pid_folder.is_directory is True
    assert pid_folder.user == 'airflow'
    assert pid_folder.group == 'airflow'
    assert pid_folder.mode == 0o700


def test_airflow_home_folder(File):
    """
    Airflow home folder should exists
    """

    home_folder = File('/var/lib/airflow/airflow')

    assert home_folder.exists is True
    assert home_folder.is_directory is True
    assert home_folder.user == 'airflow'
    assert home_folder.group == 'airflow'
    assert home_folder.mode == 0o700


def test_airflow_virtual_env_folder(File):
    """
    Virtualenv folder should exists
    """

    venv_folder = File('/var/lib/airflow/venv')

    assert venv_folder.exists is True
    assert venv_folder.is_directory is True
    assert venv_folder.user == 'airflow'
    assert venv_folder.group == 'airflow'
    assert venv_folder.mode == 0o755
