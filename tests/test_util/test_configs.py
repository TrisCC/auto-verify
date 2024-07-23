from pathlib import Path

import pytest
from ConfigSpace import ConfigurationSpace

from autoverify.util.configs import (
    config_dict_from_config_str,
    config_from_file,
    config_from_str,
)


@pytest.fixture
def config_txt() -> str:
    return """Configuration(values={
    'A': 500,
    'B': 5.0,
    'C': True,
    })"""


@pytest.fixture
def config_yaml() -> str:
    return """A: 500\nB: 5.0\nC: true\n"""


def test_config_dict_from_config_str(config_txt: str):
    assert config_dict_from_config_str(config_txt) == {
        "A": 500,
        "B": 5.0,
        "C": True,
    }


def test_config_from_str(
    config_txt: str, simple_configspace: ConfigurationSpace
):
    assert (
        config_from_str(config_txt, simple_configspace)
        == simple_configspace.get_default_configuration()
    )


def test_config_from_file(
    tmp_path: Path,
    config_txt: str,
    config_yaml: str,
    simple_configspace: ConfigurationSpace,
):
    tmp_file = tmp_path / "tmp_cfg.txt"
    tmp_file.write_text(config_txt)

    assert (
        config_from_file(tmp_file, simple_configspace)
        == simple_configspace.get_default_configuration()
    )

    tmp_file = tmp_path / "tmp_cfg.yaml"
    tmp_file.write_text(config_yaml)

    assert (
        config_from_file(tmp_file, simple_configspace)
        == simple_configspace.get_default_configuration()
    )
