"""Functional tests."""
from base64 import b64decode

import pytest
import yaml
from molecule import logger
from molecule._version import version_tuple as molecule_version_tuple
from pathlib import Path
if molecule_version_tuple < (25, 1):
    from molecule.util import run_command
else:
    from molecule.app import get_app

    run_command = get_app(Path()).run_command
import os

# from molecule.util import run_command, safe_load_file

from shutil import copytree

LOG = logger.get_logger(__name__)

ROOT = Path(__file__).resolve().parents[2]
SCENARIO_SRC = ROOT / "molecule" / "tests"     # where molecule.yml actually is


@pytest.mark.parametrize(
    ("namespace", "vm_name", "secret_name", "user"),
    [
        ("kube-public", "instance-full", "instance-full", "notmolecule"),
        ("default", "almost-default", "almost-default", "molecule"),
        ("default", "instance-running-false", "", "molecule"),
    ],
)


class TestClass:
    """Test non running VMs and compare to references yaml files."""

    @classmethod
    def setup_class(cls):
        # Ensure we run from the project root so "molecule -s tests" finds molecule/tests/molecule.yml
        os.chdir(ROOT)
        if not SCENARIO_SRC.exists():
            raise RuntimeError(f"Scenario dir not found: {SCENARIO_SRC}")
        # For Python 3.8+; if you expect reruns, allow existing:
        # copytree(SCENARIO_SRC, ROOT / "molecule" / "tests", dirs_exist_ok=True)

        cmd = ["molecule", "create", "-s", "tests"]
        result = run_command(cmd)
        assert result.returncode == 8

    @classmethod
    def teardown_class(cls):
        cmd = ["molecule", "destroy", "-s", "tests"]
        result = run_command(cmd)
        assert result.returncode == 0

    # Check spec result is same as tracked refs/
    def test_instance_spec(self, namespace, vm_name, secret_name, user):
        cmd = [
            "kubectl",
            "get",
            "-n",
            namespace,
            "VirtualMachine",
            vm_name,
            "-o",
            "yaml",
        ]
        result = run_command(cmd)
        assert result.returncode == 0

        result_yaml = yaml.safe_load(result.stdout)
        spec_test_yaml = safe_load_file(
            "molecule_kubevirt/test/refs/%s.yml" % (vm_name)
        )

        assert result_yaml["spec"] == spec_test_yaml["spec"]

        if secret_name != "":
            cmd = [
                "kubectl",
                "get",
                "-n",
                namespace,
                "secret",
                secret_name,
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
                "molecule_kubevirt/test/refs/user_data-%s.yml" % (secret_name)
            )

            assert spec_test_yaml == cloud_config_yaml
