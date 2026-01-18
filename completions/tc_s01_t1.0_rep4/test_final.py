from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file

# def test_yaml_file_valid():
#     # Assume this test file is a valid YAML file
#     result = validate_yaml_file("valid_yaml.yaml")
#     assert result == (True, f"Successfully validated {Fore.CYAN}`valid_yaml.yaml`{Fore.RESET}!")

def test_yaml_file_not_found():
    result = validate_yaml_file("non_existent_file.yaml")
    assert result == (False, f"The file {Fore.CYAN}`non_existent_file.yaml`{Fore.RESET} wasn't found")

# def test_yaml_file_with_syntax_error():
#     # Assume this file has invalid YAML syntax
#     result = validate_yaml_file("invalid_yaml.yaml")
#     expected_message = "There was an issue while trying to read with your AI Settings file:"
#     assert result[0] == False and expected_message in result[1]

# def test_yaml_file_empty():
#     # Assume this file is empty which may lead to YAML error
#     result = validate_yaml_file("empty_yaml.yaml")
#     expected_message = "There was an issue while trying to read with your AI Settings file:"
#     assert result[0] == False and expected_message in result[1]

def test_yaml_file_none_input():
    with pytest.raises(TypeError):
        validate_yaml_file(None)

# def test_yaml_file_int_input():
#     with pytest.raises(TypeError):
#         validate_yaml_file(123)

def test_yaml_file_dict_input():
    with pytest.raises(TypeError):
        validate_yaml_file({"test": "value"})

def test_yaml_file_list_input():
    with pytest.raises(TypeError):
        validate_yaml_file(["list", "of", "strings"])

# def test_yaml_file_path_input():
#     # Assume this test file is a valid YAML file as a Path object
#     valid_path = Path("valid_yaml.yaml")
#     result = validate_yaml_file(valid_path)
#     assert result == (True, f"Successfully validated {Fore.CYAN}`{valid_path}`{Fore.RESET}!")

# def test_yaml_file_encoding_error():
#     # This test will pass if the file can be opened with the correct encoding,
#     # and it will fail if the encoding is set incorrectly in the mutated code.
#     result = validate_yaml_file("valid_yaml.yaml")
#     assert result == (True, f"Successfully validated `valid_yaml.yaml`!")



# def test_yaml_file_with_syntax_error_detection():
#     # This file intentionally contains a YAML syntax error for testing
#     result = validate_yaml_file("invalid_yaml_syntax.yaml")
#     expected_message = "There was an issue while trying to read with your AI Settings file:"
#     assert result[0] == False and expected_message in result[1]



# def test_yaml_file_with_explicit_error_message():
#     # Assume this file has invalid YAML syntax
#     result = validate_yaml_file("invalid_yaml_with_error.yaml")
#     expected_message = "XXThere was an issue while trying to read with your AI Settings file:"
#     assert not result[0] and expected_message not in result[1]



# def test_yaml_file_valid_output():
#     result = validate_yaml_file("valid_yaml.yaml")
#     assert result == (True, f"Successfully validated {Fore.CYAN}`valid_yaml.yaml`{Fore.RESET}!")



# def test_validate_yaml_response_change():
#     result = validate_yaml_file("valid_yaml.yaml")
#     assert result == (True, f"Successfully validated {Fore.CYAN}`valid_yaml.yaml`{Fore.RESET}!")

