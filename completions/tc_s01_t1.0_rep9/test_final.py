from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_with_non_existing_path():
    result = validate_yaml_file("non_existent_file.yaml")
    assert result[0] is False
    assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_valid_yaml():
#     # Assume 'valid_yaml.yaml' contains correct YAML content
#     result = validate_yaml_file("tests/valid_yaml.yaml")
#     assert result[0] is True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_invalid_yaml():
#     # Assume 'invalid_yaml.yaml' has incorrect YAML formatting
#     result = validate_yaml_file("tests/invalid_yaml.yaml")
#     assert result[0] is False
#     assert "There was an issue while trying to read" in result[1]

def test_validate_yaml_file_with_empty_yaml():
    # Assume 'empty.yaml' is an empty file which is still valid YAML
    result = validate_yaml_file("tests/empty.yaml")
    assert result[0] is False

# def test_validate_yaml_file_using_path_object_with_valid_yaml():
#     file_path = Path("tests/valid_yaml.yaml")
#     result = validate_yaml_file(file_path)
#     assert result[0] is True 
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_file_using_path_object_with_invalid_yaml():
#     file_path = Path("tests/invalid_yaml.yaml")
#     result = validate_yaml_file(file_path)
#     assert result[0] is False
#     assert "There was an issue while trying to read" in result[1]

# def test_validate_yaml_file_with_invalid_encoding():
#     # `any_valid_yaml.yaml` assumes presence of a file that contains valid yaml content.
#     result = validate_yaml_file("tests/any_valid_yaml.yaml")
#     assert result[0] is False
#     assert "UnicodeDecodeError" in result[1]



# def test_validate_yaml_file_with_file_not_found_message():
#     result = validate_yaml_file("non_existent_file.yaml")
#     assert result[0] is False
#     assert "The file `non_existent_file.yaml` wasn't found" in result[1]



# def test_validate_yaml_file_with_yaml_error():
#     # Mockup yaml file content that triggers yaml.YAMLError
#     with open("tests/error_triggering_yaml.yaml", "w") as f:
#         f.write(": unindented key")
#     result = validate_yaml_file("tests/error_triggering_yaml.yaml")
#     assert result[0] is False
#     assert "was an issue while trying to read" in result[1]



# def test_validate_yaml_file_with_changed_error_message():
#     # Mockup yaml file content that triggers yaml.YAMLError
#     with open("tests/error_triggering_yaml.yaml", "w") as f:
#         f.write(": unindented key")
#     result = validate_yaml_file("tests/error_triggering_yaml.yaml")
#     assert "XX" not in result[1]



# def test_validate_yaml_file_success_message_correct():
#     # Given a valid YAML content file path "valid_yaml.yaml", it should return True with success message.
#     result = validate_yaml_file("tests/valid_yaml.yaml")
#     assert result[0] is True
#     assert "Successfully validated" in result[1]



# def test_validate_yaml_file_with_success_message_correct():
#     result = validate_yaml_file("tests/valid_yaml.yaml")
#     assert result[0] is True
#     assert "Successfully validated" in result[1] and "XX" not in result[1]

