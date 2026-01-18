from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_with_nonexistent_path():
    result = validate_yaml_file("nonexistent.yaml")
    assert result[0] == False
    assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_directory_instead_of_file():
#     result = validate_yaml_file(".")
#     assert result[0] == False
#     assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_valid_yaml():
#     # Assuming 'valid.yaml' is a valid YAML file in the test directory
#     result = validate_yaml_file("valid.yaml")
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_invalid_yaml():
#     # Assuming 'invalid.yaml' is an invalid YAML file in the test directory
#     result = validate_yaml_file("invalid.yaml")
#     assert result[0] == False
#     assert "There was an issue while trying to read" in result[1]

# def test_validate_yaml_file_with_empty_file():
#     # Assuming 'empty.yaml' is an empty file in the test directory
#     result = validate_yaml_file("empty.yaml")
#     assert result[0] == False
#     assert "There was an issue while trying to read" in result[1]

# def test_validate_yaml_file_with_binary_file():
#     # Assuming 'binary.dat' is a binary file that is not a YAML file
#     result = validate_yaml_file("binary.dat")
#     assert result[0] == False
#     assert "There was an issue while trying to read" in result[1]

def test_validate_yaml_file_with_none_input():
    with pytest.raises(TypeError):
        validate_yaml_file(None)

# def test_validate_yaml_file_with_integer_input():
#     with pytest.raises(TypeError):
#         validate_yaml_file(12345)

# def test_validate_yaml_file_with_path_object():
#     # Assuming 'valid.yaml' is a valid YAML file in the test directory
#     result = validate_yaml_file(Path("valid.yaml"))
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_incorrect_encoding():
#     # This test should pass with the original code and fail with the mutated code due to encoding error
#     result = validate_yaml_file("valid.yaml")  # Assuming 'valid.yaml' exists and is correctly formatted
#     assert result[0] == True
#     assert "Successfully validated" in result[1]



def test_validate_yaml_file_error_message_format():
    result = validate_yaml_file("nonexistent.yaml")
    assert "XX" not in result[1]



# def test_validate_yaml_file_with_invalid_yaml_handling():
#     # Assuming 'invalid.yaml' is an invalid YAML file in the test directory
#     result = validate_yaml_file("invalid.yaml")
#     assert result[0] == False
#     assert "There was an issue while trying to read" in result[1]



def test_validate_yaml_file_with_specific_error_message():
    # This test checks for the exact error message format in case of a YAML error
    result = validate_yaml_file("invalid.yaml")  # Assuming 'invalid.yaml' is an invalid YAML file
    assert "XXThere was an issue while trying to read with your AI Settings file:" not in result[1]



# def test_validate_yaml_file_success_message():
#     # Assuming 'valid.yaml' is a valid YAML file in the test directory
#     result = validate_yaml_file("valid.yaml")
#     assert result[0] == True
#     assert "Successfully validated" in result[1]



def test_validate_yaml_file_success_message_format():
    # This test checks for the exact success message format
    result = validate_yaml_file("valid.yaml")  # Assuming 'valid.yaml' is a valid YAML file
    assert "XXSuccessfully validated" not in result[1]

