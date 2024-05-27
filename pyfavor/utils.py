"""Module contining utility and helper functions for the efavor-automation package"""
from typing import Any, Dict, List, Literal, Optional
import pathlib
import platform
import subprocess
import sys
import pandas as pd
import yaml


def find_os() -> str:
    """ """
    return platform.system().lower()


def install_package(package_name: str) -> None:
    """ """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def hr_to_sec(time_hr: float, start_hr: int = 0) -> int:
    """Converts time in hours to EPANET simulation time in seconds.
    start_hr is the simulation start time in EPANET (default 0)"""
    return start_hr + time_hr * 3_600


def hr_to_min(time_hr: float) -> float:
    """ """
    return time_hr * 60

    
def read_table(
        file_path: pathlib.Path, 
        schema_file: Optional[pathlib.Path] = None) -> Dict:
    """Reads yaml table from the given YAML file.

    Args:
        file_path: path to the YAML file.
        schema_file: path to json 'jsonschema' file
    Returns:
        Dictionary representation of the yaml file if the file exists and no
            errors occured while parsing the file.
    Raises:
        TableNotReadException.
    """
    try:
        stream = open(file_path, "r", encoding="utf-8")
        loaded_yaml = yaml.safe_load(stream)
    except FileNotFoundError as exc:
        print(f"File in {file_path} not found.")
        raise TableNotReadException(table=file_path.as_posix()) from exc
    except yaml.YAMLError as exc:
        print(f"File in {file_path} cannot be parsed.")
        raise TableNotReadException(table=file_path.as_posix()) from exc
    finally:
        stream.close()

    if schema_file:
        schema = load_json(schema_file)
        validate(loaded_yaml, schema)

    return loaded_yaml
