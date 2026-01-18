from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_valid():
    # Create a dummy valid YAML file
    with open('valid_yaml.yml', 'w') as fp:
        fp.write('key: value')
    result = validate_yaml_file('valid_yaml.yml')
    assert result == (True, f"Successfully validated {Fore.CYAN}`valid_yaml.yml`{Fore.RESET}!")

def test_validate_yaml_file_not_found():
    result = validate_yaml_file('non_existent_file.yml')
    assert result == (False, f"The file {Fore.CYAN}`non_existent_file.yml`{Fore.RESET} wasn't found")

def test_validate_yaml_file_invalid_yaml():
    # Create a dummy invalid YAML file
    with open('invalid_yaml.yml', 'w') as fp:
        fp.write(': invalid')
    result = validate_yaml_file('invalid_yaml.yml')
    assert "There was an issue while trying to read with your AI Settings file:" in result[1]

def test_validate_yaml_file_empty():
    # Create a dummy empty YAML file
    with open('empty_yaml.yml', 'w') as fp:
        fp.write('')
    result = validate_yaml_file('empty_yaml.yml')
    assert result == (True, f"Successfully validated {Fore.CYAN}`empty_yaml.yml`{Fore.RESET}!")

# def test_validate_yaml_file_with_non_str_path():
#     # Test with a non-string, non-Path object
#     result = validate_yaml_file(None)
#     assert "The file " in result[1]

def test_validate_yaml_file_with_path_object():
    # Create a Path object for valid YAML
    path_obj = Path('path_valid_yaml.yml')
    with open(path_obj, 'w') as fp:
        fp.write('key: value')
    result = validate_yaml_file(path_obj)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{path_obj}`{Fore.RESET}!")

def test_validate_yaml_file_with_empty_name():
    result = validate_yaml_file('')
    assert "The file " in result[1]

# def test_validate_yaml_file_handles_exception():
#     with open('incorrect_yaml.yml', 'w') as fp:
#         fp.write('key: value\nkey')  # Introduce a YAML syntax error
#     result = validate_yaml_file('incorrect_yaml.yml')
#     assert result == (False, f"There was an issue while trying to read with your AI Settings file:")



# def test_validate_yaml_file_error_message_changed():
#     # Create a dummy invalid YAML file
#     with open('invalid_yaml_error_msg.yml', 'w') as fp:
#         fp.write(': invalid')
#     result = validate_yaml_file('invalid_yaml_error_msg.yml')
#     assert result[1] == f"There was an issue while trying to read with your AI Settings file: could not find expected ':'"

