"""
Role tests
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_airflow_user(host):
    """
    Tests about airflow user configuration
    """
    airflow_user = host.user('airflow')

    assert airflow_user.exists is True
    assert airflow_user.group == 'airflow'
    assert airflow_user.home == '/var/lib/airflow'
    assert airflow_user.shell == '/bin/false'


def test_airflow_group(host):
    """
    Tests about airflow group configuration
    """

    assert host.group('airflow').exists is True


@pytest.mark.parametrize('name,codenames', [
    ('python3-dev', None),
    ('libpq-dev', None),
    ('libssl-dev', None),
    ('libffi-dev', None),
    ('build-essential', None),
    ('python-virtualenv', None),
    ('python-pip', None),
])
def test_prerequisites_packages(host, name, codenames):
    """
    Tests about airflow prerequisites packages
    """

    if host.system_info.distribution not in ['debian', 'ubuntu']:
        pytest.skip('{} ({}) distribution not managed'.format(
            host.system_info.distribution, host.system_info.release))

    if codenames and host.system_info.codename.lower() not in codenames:
        pytest.skip('{} package not used with {} ({})'.format(
            name, host.system_info.distribution, host.system_info.codename))

    assert host.package(name).is_installed


def test_airflow_processes(host):
    """
    Test about airflow processes
    """

    assert len(host.process.filter(user='airflow', comm='airflow')) >= 2


@pytest.mark.parametrize('name', [
    ('airflow-webserver'),
    ('airflow-scheduler'),
])
def test_airflow_services(host, name):
    """
    Test about airflow services
    """

    if host.system_info.codename == 'jessie':
        output = host.check_output('service {} status'.format(name))
        assert '{} running'.format(name) in output
    else:
        service = host.service(name)
        assert service.is_running
        assert service.is_enabled


@pytest.mark.parametrize('path,path_type,user,group,mode', [
    ('/var/run/airflow', 'directory', 'airflow', 'airflow', 0o700),
    ('/var/lib/airflow/airflow', 'directory', 'airflow', 'airflow', 0o700),
    ('/var/lib/airflow/venv', 'directory', 'airflow', 'airflow', 0o755),
    (
        '/var/lib/airflow/airflow/airflow.cfg',
        'file', 'airflow', 'airflow', 0o400
    ),
])
def test_airflow_paths(host, path, path_type, user, group, mode):
    """
    Tests Airflow paths
    """

    current_path = host.file(path)

    assert current_path.exists

    if path_type == 'directory':
        assert current_path.is_directory
    elif path_type == 'file':
        assert current_path.is_file
    assert current_path.user == user
    assert current_path.group == group
    assert current_path.mode == mode
