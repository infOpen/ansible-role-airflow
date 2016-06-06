"""
Role tests
"""
import pytest

# To mark all the tests as destructive:
# pytestmark = pytest.mark.destructive

# To run all the tests on given docker images:
pytestmark = pytest.mark.docker_images('infopen/ubuntu-trusty-ssh')
#pytestmark = pytest.mark.docker_images('infopen/ubuntu-trusty-ssh',
#                                       'infopen/ubuntu-xenial-ssh')

# Both
# pytestmark = [
#     pytest.mark.destructive,
#     pytest.mark.docker_images("debian:jessie", "centos:7")
# ]


def test_foo_a(User):
    assert User().name == 'root'

def test_foo_b(User):
    assert User().name == 'root'
