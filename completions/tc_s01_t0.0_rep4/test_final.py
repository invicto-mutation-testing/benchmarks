from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_with_nonexistent_path():
    result = validate_yaml_file("nonexistent_file.yaml")
    assert result[0] == False
    assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_directory_instead_of_file():
#     result = validate_yaml_file(".")
#     assert result[0] == False
#     assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_empty_file():
#     # Assuming an empty file named 'empty_file.yaml' exists for testing
#     result = validate_yaml_file("empty_file.yaml")
#     assert result[0] == False
#     assert "issue while trying to read" in result[1]

# def test_validate_yaml_file_with_invalid_yaml_content():
#     # Assuming a file named 'invalid_yaml.yaml' exists with invalid YAML content
#     result = validate_yaml_file("invalid_yaml.yaml")
#     assert result[0] == False
#     assert "issue while trying to read" in result[1]

# def test_validate_yaml_file_with_valid_yaml():
#     # Assuming a file named 'valid_yaml.yaml' exists with valid YAML content
#     result = validate_yaml_file("valid_yaml.yaml")
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_path_object():
#     # Assuming a file named 'valid_yaml.yaml' exists with valid YAML content
#     path = Path("valid_yaml.yaml")
#     result = validate_yaml_file(path)
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_encoding_error():
#     # This test case checks for encoding errors which should not occur in the original code
#     result = validate_yaml_file("valid_yaml.yaml")  # Assuming 'valid_yaml.yaml' is a valid YAML file
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_specific_not_found_message():
#     result = validate_yaml_file("nonexistent_file.yaml")
#     expected_message = "The file `nonexistent_file.yaml` wasn't found"
#     assert result[0] == False
#     assert expected_message in result[1]