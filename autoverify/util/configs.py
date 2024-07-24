"""_summary_."""

import ast
import re
import yaml
import logging
from pathlib import Path
from typing import Any

from ConfigSpace import Configuration, ConfigurationSpace


def config_dict_from_config_str(cfg: str) -> dict[str, Any]:
    """Create a config object from a printed configuration."""
    cfg = re.sub(r"^.*?{", "{", cfg)
    dic: dict[str, Any] = ast.literal_eval(cfg[:-1])
    return dic


def config_from_str(cfg: str, cfg_space: ConfigurationSpace) -> Configuration:
    """Create a config object from a string configuration."""
    return Configuration(cfg_space, config_dict_from_config_str(cfg))


def flatten_dict_keys(data: dict[str, Any], prefix=""):
    """Flattens a nested dictionary by concatenating keys with values using a sp
    ecified prefix.
    """
    flat_list = []
    for key, value in data.items():
        # Concatenate key with prefix (if provided)
        new_key = f"{prefix}{key}" if prefix else key

        # Base case: Append value directly if it's not a dictionary
        if not isinstance(value, dict):
            flat_list.append(f"{new_key}:{value}")
        # Recursive call for nested dictionaries
        else:
            # Recursively call with updated prefix (including current key)
            flat_list.extend(flatten_dict_keys(value, f"{new_key}__"))
    return flat_list


def convert_to_data_type(string_value):
    """Converts a string to an appropriate data type using built-in functions."""
    try:
        # Attempt conversion to integer
        return int(string_value)
    except ValueError:
        pass

    try:
        # Attempt conversion to float
        return float(string_value)
    except ValueError:
        pass

    # Check for boolean values (case-insensitive)
    if string_value.lower() in ("true", "false"):
        return bool(string_value.lower() == "true")

    # String by default if not convertible to other types
    return string_value


def config_from_txt_file(
    file: Path, cfg_space: ConfigurationSpace
) -> Configuration:
    """Create a config from a config in a txt file."""
    with open(str(file), "r") as f:
        txt = f.read().rstrip()

    return config_from_str(txt, cfg_space)


def config_from_yaml_file(
    file: Path, cfg_space: ConfigurationSpace
) -> Configuration:
    """Create a config from a config in a yaml file."""
    with open(file) as stream:
        # test = stream.read()
        cfg_dict = yaml.safe_load(stream)
        try:
            # Remove unnecessary parameters
            del cfg_dict["model"]
            del cfg_dict["specification"]
        except KeyError:
            logging.debug("Could not delete model and/or specification")
        cfg_dict = flatten_dict_keys(cfg_dict)

        new_dict = {}
        for value in cfg_dict:
            parameter = value.split(":")
            new_dict[parameter[0]] = convert_to_data_type(parameter[1])

    return Configuration(cfg_space, new_dict)


def config_from_file(
    file: Path, cfg_space: ConfigurationSpace
) -> Configuration:
    """Create a config from a config in a file."""
    if file.suffix == ".txt":
        return config_from_txt_file(file, cfg_space)
    elif file.suffix == ".yaml":
        return config_from_yaml_file(file, cfg_space)
    else:
        raise ValueError(f"File type {file.suffix} not supported, use txt.")
