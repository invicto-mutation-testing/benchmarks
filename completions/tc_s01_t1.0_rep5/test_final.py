from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_with_valid_file():
    # Simulate valid YAML content
    test_file_path = 'valid_yaml.yml'
    with open(test_file_path, 'w') as file:
        file.write("name: pytest\nversion: 1.0")
    result = validate_yaml_file(test_file_path)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{test_file_path}`{Fore.RESET}!")

def test_validate_yaml_file_with_invalid_yaml():
    # Simulate broken YAML content
    test_file_path = 'invalid_yaml.yml'
    with open(test_file_path, 'w') as file:
        file.write("name: pytest\nversion: 1.0:\n")
    result = validate_yaml_file(test_file_path)
    assert "There was an issue while trying to read with your AI Settings file" in result[1]

def test_validate_yaml_file_with_non_existent_file():
    # Non-existent file path
    test_file_path = 'non_existent_file.yml'
    result = validate_yaml_file(test_file_path)
    assert result == (False, f"The file {Fore.CYAN}`{test_file_path}`{Fore.RESET} wasn't found")

# def test_validate_yaml_file_with_directory_input():
#     # Input is a directory, not a file
#     test_directory_path = '/tmp'
#     result = validate_yaml_file(test_directory_path)
#     assert "There was an issue while trying to read with your AI Settings file" in result[1]

# def test_validate_yaml_file_with_yaml_error():
#     # Simulate a YAML syntax issue in a file-like object
#     mock_file = StringIO("name: Test\nitems:\n- item1:\n- item2:")  # Deliberately malformed YAML
#     with patch("builtins.open", mock_open(read_data=mock_file.getvalue())):
#         result = validate_yaml_file("fakefile.yml")
#         assert "There was an issue while trying to read with your AI Settings file" in result[1]



# def test_validate_yaml_file_error_message_mutation():
#     # Specific test case to fail the mutated code and pass the original code based on the error message content
#     test_file_path = 'invalid_yaml_with_error_message.yml'
#     with open(test_file_path, 'w') as file:
#         file.write("name: pytest\nversion: 1.0:\n")
#     result = validate_yaml_file(test_file_path)
#     assert result[1] == f"XXThere was an issue while trying to read with your AI Settings file: {e}XX"

