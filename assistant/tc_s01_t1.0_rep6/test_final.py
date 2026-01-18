import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from put import validate_yaml_file

# Sample valid and invalid YAML content
VALID_YAML_CONTENT = """
name: Example
version: 1.0
"""
INVALID_YAML_CONTENT = """
name: Example
version: 1.0
unclosed_sequence: [
"""

def test_validate_yaml_file_valid():
    # Test the function with valid YAML content
    with patch("builtins.open", mock_open(read_data=VALID_YAML_CONTENT)):
        result, message = validate_yaml_file("valid.yaml")
    assert result == True
    assert "Successfully validated" in message

def test_validate_yaml_file_not_found():
    # Test the function with a file path that triggers FileNotFoundError
    with patch("builtins.open", side_effect=FileNotFoundError):
        result, message = validate_yaml_file("nonexistent.yaml")
    assert result == False
    assert "wasn't found" in message

def test_validate_yaml_file_invalid_yaml():
    # Test the function with invalid YAML content
    with patch("builtins.open", mock_open(read_data=INVALID_YAML_CONTENT)):
        result, message = validate_yaml_file("invalid.yaml")
    assert result == False
    assert "issue while trying to read" in message

def test_validate_yaml_file_with_path_object():
    # Test using Path object as input
    valid_path = Path("valid.yaml")
    with patch("builtins.open", mock_open(read_data=VALID_YAML_CONTENT)):
        result, message = validate_yaml_file(valid_path)
    assert result == True
    assert "Successfully validated" in message

def test_validate_yaml_file_not_found_message():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result, message = validate_yaml_file("nonexistent.yaml")
    assert "XX" not in message, "The message should not include mutation 'XX' markers"

# New test case specifically checking for mutation in the success message
def test_validate_yaml_file_success_message_mutation():
    # This test will fail if mutant code is present that includes "XX" in the success message
    with patch("builtins.open", mock_open(read_data=VALID_YAML_CONTENT)):
        result, message = validate_yaml_file("valid.yaml")
    assert "XX" not in message, "The success message should not include 'XX'. Possible code mutation detected."