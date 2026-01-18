from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_valid_file():
    # create a temporary YAML valid file
    with open('valid_yaml.yml', 'w') as file:
        file.write("hello: world\n")
    assert validate_yaml_file('valid_yaml.yml') == (True, f"Successfully validated {Fore.CYAN}`valid_yaml.yml`{Fore.RESET}!")

def test_validate_yaml_invalid_file():
    # create a temporary YAML invalid file
    with open('invalid_yaml.yml', 'w') as file:
        file.write("{unclosed: dict\n")
    assert validate_yaml_file('invalid_yaml.yml')[0] == False

def test_validate_yaml_nonexistent_file():
    assert validate_yaml_file('nonexistent.yml')[0] == False

# def test_validate_yaml_none_input():
#     assert validate_yaml_file(None)[0] == False

# def test_validate_yaml_integer_input():
#     assert validate_yaml_file(12345)[0] == False

# def test_validate_yaml_list_input():
#     assert validate_yaml_file(['not', 'a', 'path'])[0] == False

def test_validate_yaml_empty_string():
    assert validate_yaml_file('')[0] == False

# def test_validate_yaml_directory_input(tmp_path):
#     dir_path = str(tmp_path / "a_directory")
#     Path(dir_path).mkdir()
#     assert validate_yaml_file(dir_path)[0] == False

def test_validate_yaml_file_not_found_message():
    assert validate_yaml_file('nonexistent.yml') == (False, f"The file {Fore.CYAN}`nonexistent.yml`{Fore.RESET} wasn't found")

