from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_valid():
    with open("test_valid.yaml", "w") as f:
        f.write("name: John\nage: 30")
    result = validate_yaml_file("test_valid.yaml")
    assert result == (True, f"Successfully validated {Fore.CYAN}`test_valid.yaml`{Fore.RESET}!")

def test_validate_yaml_file_not_found():
    result = validate_yaml_file("nonexistent.yaml")
    assert result == (False, f"The file {Fore.CYAN}`nonexistent.yaml`{Fore.RESET} wasn't found")

# def test_validate_yaml_file_invalid_yaml():
#     with open("test_invalid.yaml", "w") as f:
#         f.write("name: John\n:age: 30")
#     result = validate_yaml_file("test_invalid.yaml")
#     expected_message_start = "There was an issue while trying to read with your AI Settings file: while scanning for the next token"
#     assert result[0] == False and result[1].startswith(expected_message_start)

def test_validate_yaml_file_pathlib_path():
    with open("test_pathlib.yaml", "w") as f:
        f.write("name: John\nage: 30")
    path = Path("test_pathlib.yaml")
    result = validate_yaml_file(path)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{path}`{Fore.RESET}!")

# def test_validate_yaml_file_invalid_yaml_with_specific_error_message():
#     with open("test_specific_invalid.yaml", "w") as f:
#         f.write("name: John\n:age: 30")
#     result = validate_yaml_file("test_specific_invalid.yaml")
#     expected_message = "XXThere was an issue while trying to read with your AI Settings file:"
#     actual_message = result[1]
#     assert result[0] is False and expected_message not in actual_message

