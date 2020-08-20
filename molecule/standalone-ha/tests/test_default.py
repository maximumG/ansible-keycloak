import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('keycloak*')


def test_keycloak_directories(host):
    """
    Check that Keycloak directory structure is present and ownned by keycloak/keycloak
    """
    assert host.file('/opt/keycloak').is_directory
    assert host.file('/opt/keycloak/common').is_directory
    assert host.file('/opt/keycloak/tools').is_directory
    assert host.file('/opt/keycloak').user == 'keycloak' and host.file('/opt/keycloak').group == 'keycloak'
    assert host.file('/opt/keycloak/common').user == 'keycloak' and host.file('/opt/keycloak').group == 'keycloak'
    assert host.file('/opt/keycloak/tools').user == 'keycloak' and host.file('/opt/keycloak').group == 'keycloak'


def test_keycloak_user(host):
    """
    Check that keycloak user exists
    """
    assert host.user('keycloak').exists
    assert host.user('keycloak').shell == '/sbin/nologin'
    assert host.user('keycloak').home == '/opt/keycloak'


def test_keycloak_service_running(host):
    """
    Check that the keycloak service is enabled and running on the host
    """
    assert host.service('keycloak').is_enabled
    assert host.service('keycloak').is_running


def test_keycloak_infinispan_cluster(host):
    """
    Check that keycloak is running within an Infinispan Cluster and found its peer

    ex: [org.infinispan.CLUSTER] (MSC service thread 1-2) ISPN000094: Received new cluster view for channel ejb:
    [keycloak-centos8|1] (2) [keycloak-centos8, keycloak-debian10]
    """
    assert host.run_test('journalctl -u keycloak | '
                         'grep -i "org.infinispan.CLUSTER" | '
                         'grep -i "Received new cluster view" |'
                         'grep -i "(2)"')
