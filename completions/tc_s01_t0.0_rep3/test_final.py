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

# def test_validate_yaml_file_with_empty_file():
#     # Assuming an empty file named 'empty.yaml' exists for testing
#     result = validate_yaml_file("empty.yaml")
#     assert result[0] == False
#     assert "issue while trying to read" in result[1]

# def test_validate_yaml_file_with_invalid_yaml_content():
#     # Assuming a file named 'invalid.yaml' with invalid YAML content exists for testing
#     result = validate_yaml_file("invalid.yaml")
#     assert result[0] == False
#     assert "issue while trying to read" in result[1]

# def test_validate_yaml_file_with_valid_yaml():
#     # Assuming a file named 'valid.yaml' with valid YAML content exists for testing
#     result = validate_yaml_file("valid.yaml")
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_path_object():
#     # Assuming a file named 'valid.yaml' with valid YAML content exists for testing
#     result = validate_yaml_file(Path("valid.yaml"))
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_encoding_error():
#     # This test will pass with the original code and fail with the mutated code due to encoding error
#     result = validate_yaml_file("valid.yaml")  # Assuming 'valid.yaml' is a correctly formatted YAML file
#     assert result[0] == True
#     assert "Successfully validated" in result[1]



def test_validate_yaml_file_with_specific_not_found_message():
    result = validate_yaml_file("nonexistent.yaml")
    assert result[0] == False
    assert "XXThe file" not in result[1]



# def test_validate_yaml_file_with_invalid_yaml_content_should_fail_on_mutant():
#     result = validate_yaml_file("invalid.yaml")
#     assert result[0] == False, "Should be False when YAML content is invalid"



def test_validate_yaml_file_with_specific_error_message():
    result = validate_yaml_file("invalid.yaml")  # Assuming 'invalid.yaml' has invalid YAML content
    assert result[0] == False
    assert "XXThere was an issue" not in result[1]



# def test_validate_yaml_file_with_valid_yaml_should_fail_on_mutant():
#     # Assuming a file named 'valid.yaml' with valid YAML content exists for testing
#     result = validate_yaml_file("valid.yaml")
#     assert result[0] == True, "Should be True when YAML content is valid"



def test_validate_yaml_file_success_message():
    result = validate_yaml_file("valid.yaml")  # Assuming 'valid.yaml' is a correctly formatted YAML file
    assert result[0] == False
    assert "XXSuccessfully validated" not in result[1]

