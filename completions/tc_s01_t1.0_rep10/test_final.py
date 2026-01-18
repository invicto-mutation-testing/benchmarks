from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_valid_content():
    mock_content = "name: TestApp\nversion: '1.0'"
    with patch("builtins.open", mock_open(read_data=mock_content)), patch("yaml.load") as mock_load:
        mock_load.return_value = {"name": "TestApp", "version": "1.0"}  # simulate YAML content
        success, message = validate_yaml_file("valid.yaml")
        assert success is True
        assert "Successfully validated" in message

# def test_validate_yaml_file_nonexistent_file():
#     with pytest.raises(FileNotFoundError):
#         validate_yaml_file("nonexistent.yaml")

def test_validate_yaml_file_invalid_yaml_format():
    mock_content = "name: TestApp\nversion '1.0'"  # Incorrect YAML format
    with patch("builtins.open", mock_open(read_data=mock_content)), \
         patch("yaml.load", side_effect=yaml.YAMLError("error parsing YAML")):
        success, message = validate_yaml_file("invalid.yaml")
        assert success is False
        assert "There was an issue while trying to read with your AI Settings file" in message

def test_validate_yaml_file_with_path_object():
    mock_content = "name: TestApp\nversion: '1.0'"
    with patch("builtins.open", mock_open(read_data=mock_content)), patch("yaml.load") as mock_load:
        mock_load.return_value = {"name": "TestApp", "version": "1.0"}  # simulate YAML content
        success, message = validate_yaml_file(Path("valid.yaml"))
        assert success is True
        assert "Successfully validated" in message

def test_validate_yaml_file_empty_content():
    mock_content = ""
    with patch("builtins.open", mock_open(read_data=mock_content)), \
         patch("yaml.load", side_effect=yaml.YAMLError("empty document")):
        success, message = validate_yaml_file("empty.yaml")
        assert success is False
        assert "There was an issue while trying to read with your AI Settings file" in message

def test_validate_yaml_file_exception_propagation():
    # Ensure exceptions not specifically handled are propagated outward
    with patch("builtins.open", side_effect=PermissionError("No permission to read file")):
        with pytest.raises(PermissionError) as excinfo:
            validate_yaml_file("restricted.yaml")
        assert "No permission to read file" in str(excinfo.value)

# def test_validate_yaml_file_incorrect_encoding():
#     with pytest.raises(UnicodeDecodeError):
#         validate_yaml_file("test.yaml")



# def test_validate_yaml_file_file_not_found():
#     success, message = validate_yaml_file("nonexistent.yaml")
#     assert success is False
#     assert "The file `nonexistent.yaml` wasn't found" in message



# def test_validate_yaml_file_file_not_found_message_mutation():
#     success, message = validate_yaml_file("nonexistent.yaml")
#     assert success is False
#     assert "The file `nonexistent.yaml` wasn't found" in message



def test_error_message_mutated():
    # This test checks specific text in the error message that differs between original and mutant
    mock_content = "name: TestApp\nversion '1.0'"
    with patch("builtins.open", mock_open(read_data=mock_content)), \
         patch("yaml.load", side_effect=yaml.YAMLError("error parsing YAML")):
        success, message = validate_yaml_file("invalid.yaml")
        assert success is False
        assert "XXThere was an issue while trying to read with your AI Settings file: error parsing YAMLXX" not in message



# def test_validate_yaml_file_message_exact_match():
#     mock_content = "name: TestApp"
#     with patch("builtins.open", mock_open(read_data=mock_content)), patch("yaml.load"):
#         success, message = validate_yaml_file("valid.yaml")
#         expected_message = f"Successfully validated {Fore.CYAN}`valid.yaml`{Fore.RESET}!"
#         assert success is True
#         assert message == expected_message

