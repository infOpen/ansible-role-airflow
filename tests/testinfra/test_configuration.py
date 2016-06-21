"""
Role tests
"""
import pytest

pytestmark = pytest.mark.docker_images('infopen/ubuntu-trusty-ssh')


def test_airflow_config_file(File):
    """
    Tests about airflow configuration
    """
    config_file = File('/var/lib/airflow/airflow/airflow.cfg')

    assert config_file.exists is True
    assert config_file.is_file is True
    assert config_file.user == 'airflow'
    assert config_file.group == 'airflow'
    assert config_file.mode == 0o400
