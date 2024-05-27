"""Module contining utility and helper functions for the efavor-automation package"""
from typing import Dict, Union
import pathlib
import platform
import subprocess
import sys
import yaml


class TableNotReadException(Exception):
    """Exception raised if a configuration table not found.

    Atrributes:
        table: name of the table or list of names of tables that are not found.
    """
    def __init__(self, table: Union[str, list]):
        if isinstance(table, str):
            self.message = f"Table: {table} could not be read."
        elif isinstance(table, list):
            self.message = f"Tables: {', '.join(table)} could not be read."
        else:
            self.message = ""
        super().__init__(self.message)


def find_os() -> str:
    """Find operating system"""
    return platform.system().lower()


def install_package(package_name: str) -> None:
    """Instally Python package on demand during program execution"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def hr_to_sec(time_hr: float, start_hr: int = 0) -> int:
    """Converts time in hours to EPANET simulation time in seconds.
    start_hr is the simulation start time in EPANET (default 0)"""
    return start_hr + time_hr * 3_600


def hr_to_min(time_hr: float) -> float:
    """Converts hours to minutes"""
    return time_hr * 60

    
def read_table(
        file_path: pathlib.Path) -> Dict:
    """Reads yaml table from the given YAML file.

    Args:
        file_path: path to the YAML file.
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

    return loaded_yaml
