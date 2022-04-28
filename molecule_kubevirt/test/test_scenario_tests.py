"""Functional tests."""
from base64 import b64decode

import pytest
import yaml
from molecule import logger
from molecule.util import run_command, safe_load_file

LOG = logger.get_logger(__name__)


@pytest.mark.parametrize(
    ("namespace", "name", "user"),
    [
        ("kube-public", "instance-full", "notmolecule"),
        ("default", "instance-almost-default", "molecule"),
    ],
)
class TestClass:
    """Test non running VMs and compare to references yaml files."""

    @classmethod
    def setup_class(cls):
        cmd = ["molecule", "create", "-s", "tests"]
        result = run_command(cmd)
        assert result.returncode == 0

    @classmethod
    def teardown_class(cls):
        cmd = ["molecule", "destroy", "-s", "tests"]
        result = run_command(cmd)
        assert result.returncode == 0

    # Check spec result is same as tracked refs/
    def test_instance_spec(self, namespace, name, user):
        cmd = ["kubectl", "get", "-n", namespace, "VirtualMachine", name, "-o", "yaml"]
        result = run_command(cmd)
        assert result.returncode == 0

        result_yaml = yaml.safe_load(result.stdout)
        spec_test_yaml = safe_load_file("molecule_kubevirt/test/refs/%s.yml" % (name))

        assert result_yaml["spec"] == spec_test_yaml["spec"]

    # Check secret's user-data is same as tracked refs/
    def test_instance_secret(self, namespace, name, user):
        cmd = [
            "kubectl",
            "get",
            "-n",
            namespace,
            "secret",
            name,
            "-o",
            "jsonpath={.data.userdata}",
        ]
        result = run_command(cmd)
        assert result.returncode == 0

        cloud_config = b64decode(result.stdout)
        cloud_config_yaml = yaml.safe_load(cloud_config)

        # ssh key is emptied before testing against tracked definition
        for i in cloud_config_yaml["users"]:
            if i["name"] == user:
                i["ssh_authorized_keys"] = [""]

        spec_test_yaml = safe_load_file(
            "molecule_kubevirt/test/refs/user_data-%s.yml" % (name)
        )

        assert spec_test_yaml == cloud_config_yaml
