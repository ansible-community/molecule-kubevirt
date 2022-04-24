"""Functional tests."""
import pathlib
import shutil
import subprocess
import yaml

from molecule import logger
from molecule.test.conftest import change_dir_to
from molecule.util import run_command,safe_load_file,safe_dump,write_file

LOG = logger.get_logger(__name__)


def format_result(result: subprocess.CompletedProcess):
    """Return friendly representation of completed process run."""
    return (
        f"RC: {result.returncode}\n"
        + f"STDOUT: {result.stdout}\n"
        + f"STDERR: {result.stderr}"
    )



def test_defaults_supercharge(tmp_path: pathlib.Path, DRIVER: str) -> None:
    """Verify that supercharge scenario works."""
    shutil.rmtree(tmp_path, ignore_errors=True)
    tmp_path.mkdir(exist_ok=True)

    cmd = ["molecule", "create", "-s", "tests"]

    result = run_command(cmd)
    assert result.returncode == 0


    cmd = ["kubectl", "get", "VirtualMachine", "instance-full", "-o", "yaml"] 
    result = run_command(cmd)
    result_yaml=yaml.safe_load(result.stdout)

    cmd = ["kubectl", "get", "secret", "instance-full", "-o", "yaml"] 
    result = run_command(cmd)
    result_yaml=yaml.safe_load(result.stdout)

    cmd = ["molecule", "destroy", "-s", "tests"] 
    result = run_command(cmd)
    assert result.returncode == 0

    assert result.returncode == 99