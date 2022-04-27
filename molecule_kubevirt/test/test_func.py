"""Functional tests."""
import pathlib
import shutil
import subprocess
from base64 import b64decode

import yaml
from molecule import logger
from molecule.test.conftest import change_dir_to
from molecule.util import run_command, safe_load_file

LOG = logger.get_logger(__name__)


def format_result(result: subprocess.CompletedProcess):
    """Return friendly representation of completed process run."""
    return (
        f"RC: {result.returncode}\n"
        + f"STDOUT: {result.stdout}\n"
        + f"STDERR: {result.stderr}"
    )


def test_command_init_and_test_scenario(tmp_path: pathlib.Path, DRIVER: str) -> None:
    """Verify that init scenario works."""
    shutil.rmtree(tmp_path, ignore_errors=True)
    tmp_path.mkdir(exist_ok=True)

    scenario_name = "default"

    with change_dir_to(tmp_path):

        scenario_directory = tmp_path / "molecule" / scenario_name
        cmd = [
            "molecule",
            "init",
            "scenario",
            "--driver-name",
            DRIVER,
        ]
        result = run_command(cmd)
        assert result.returncode == 0

        assert scenario_directory.exists()

        # run molecule reset as this may clean some leftovers from other
        # test runs and also ensure that reset works.
        result = run_command(["molecule", "reset"])  # default sceanario
        assert result.returncode == 0

        result = run_command(["molecule", "reset", "-s", scenario_name])
        assert result.returncode == 0

        cmd = ["molecule", "--debug", "test", "-s", scenario_name]
        result = run_command(cmd)
        assert result.returncode == 0


def test_instance_full(tmp_path: pathlib.Path, DRIVER: str) -> None:
    """Verify that supercharge scenario works."""
    shutil.rmtree(tmp_path, ignore_errors=True)
    tmp_path.mkdir(exist_ok=True)

    # Create non running tests VMs
    cmd = ["molecule", "create", "-s", "tests"]

    result = run_command(cmd)
    assert result.returncode == 0

    # Check spec result is same as tracked defintion in git
    cmd = ["kubectl", "get", "VirtualMachine", "instance-full", "-o", "yaml"]
    result = run_command(cmd)
    assert result.returncode == 0

    result_yaml = yaml.safe_load(result.stdout)
    spec_test_yaml = safe_load_file(
        "molecule_kubevirt/test/refs/spec_instance_full.yml"
    )

    assert result_yaml["spec"] == spec_test_yaml["spec"]

    # Check secret use data result is same as tracked in git
    cmd = [
        "kubectl",
        "get",
        "secret",
        "instance-full",
        "-o",
        "jsonpath={.data.userdata}",
    ]
    result = run_command(cmd)
    assert result.returncode == 0

    cloud_config = b64decode(result.stdout)
    cloud_config_yaml = yaml.safe_load(cloud_config)

    # ssh key is emptied before testing against tracked definition
    for i in cloud_config_yaml["users"]:
        if i["name"] == "molecule":
            i["ssh_authorized_keys"] = [""]

    spec_test_yaml = safe_load_file(
        "molecule_kubevirt/test/refs/user_data_instance_full.yml"
    )

    assert spec_test_yaml == cloud_config_yaml

    # Destroy
    cmd = ["molecule", "destroy", "-s", "tests"]
    result = run_command(cmd)

    assert result.returncode == 0
