import pytest
from unittest.mock import mock_open, patch
from put import validate_yaml_file
from pathlib import Path
import yaml
from colorama import Fore

# Setup and teardown fixtures
@pytest.fixture
def setup_file_mock():
    # Mock open to simulate file handling
    m = mock_open(read_data="key: value")
    with patch("builtins.open", m):
        yield m

@pytest.fixture
def setup_pathlib_path():
    # Create a Path object for testing
    return Path("/fake/path/to/file.yaml")

# Test cases
def test_validate_yaml_file_valid_yaml(setup_file_mock):
    result = validate_yaml_file("/fake/path/to/file.yaml")
    assert result == (True, f"Successfully validated {Fore.CYAN}`/fake/path/to/file.yaml`{Fore.RESET}!"), "Should return success for valid YAML"

def test_validate_yaml_file_nonexistent_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = validate_yaml_file("/non/existent/file.yaml")
        assert result == (False, f"The file {Fore.CYAN}`/non/existent/file.yaml`{Fore.RESET} wasn't found"), "Should handle file not found error"

def test_validate_yaml_file_invalid_yaml(setup_file_mock):
    # Modify the mock to return invalid YAML content
    setup_file_mock.return_value.read.return_value = ":\n"
    with patch("builtins.open", setup_file_mock):
        result = validate_yaml_file("/fake/path/to/invalid.yaml")
        assert "There was an issue while trying to read with your AI Settings file:" in result[1], "Should return error for invalid YAML"

def test_validate_yaml_file_with_path_object(setup_pathlib_path, setup_file_mock):
    result = validate_yaml_file(setup_pathlib_path)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{setup_pathlib_path}`{Fore.RESET}!"), "Should handle Path objects correctly"

def test_validate_yaml_file_raises_unexpected_error(setup_file_mock):
    # Simulate an unexpected error type
    setup_file_mock.side_effect = Exception("Unexpected error")
    with pytest.raises(Exception, match="Unexpected error"):
        validate_yaml_file("/fake/path/to/file.yaml")

# Fixed test case to catch the mutation
def test_validate_yaml_file_invalid_yaml_should_fail(setup_file_mock):
    # Modify the mock to return invalid YAML content
    setup_file_mock.return_value.read.return_value = ":\n"
    with patch("builtins.open", setup_file_mock):
        result = validate_yaml_file("/fake/path/to/invalid.yaml")
        expected_error_msg = "There was an issue while trying to read with your AI Settings file:"
        assert result[0] == False and expected_error_msg in result[1], "Should return False for invalid YAML, catching the mutation"

# New test case to catch the mutation
def test_validate_yaml_file_invalid_yaml_mutation(setup_file_mock):
    # Modify the mock to return invalid YAML content
    setup_file_mock.return_value.read.return_value = ":\n"
    with patch("builtins.open", setup_file_mock):
        result = validate_yaml_file("/fake/path/to/invalid.yaml")
        assert "XX" not in result[1], "Mutation should not introduce 'XX' in the error message"