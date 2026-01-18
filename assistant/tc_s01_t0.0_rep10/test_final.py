import pytest
from unittest.mock import mock_open, patch
from put import validate_yaml_file  # Importing the function from the module 'put'
import yaml
from pathlib import Path

# Setup and Teardown fixtures
@pytest.fixture
def setup_file_mock():
    # Mock open to simulate file operations
    m = mock_open(read_data="key: value")
    with patch("builtins.open", m):
        yield m

@pytest.fixture
def setup_yaml_loader_mock():
    # Mock yaml loader to simulate yaml operations
    with patch("yaml.load") as mock_loader:
        yield mock_loader

# Test cases
def test_validate_yaml_file_success(setup_file_mock, setup_yaml_loader_mock):
    """Test validate_yaml_file with a valid YAML file."""
    result = validate_yaml_file("valid.yaml")
    assert result == (True, "Successfully validated \x1b[36m`valid.yaml`\x1b[39m!")
    setup_file_mock.assert_called_once_with("valid.yaml", encoding="utf-8")
    setup_yaml_loader_mock.assert_called_once()

def test_validate_yaml_file_not_found():
    """Test validate_yaml_file with a non-existent file."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = validate_yaml_file("invalid.yaml")
        assert result == (False, "The file \x1b[36m`invalid.yaml`\x1b[39m wasn't found")

def test_validate_yaml_file_invalid_yaml(setup_file_mock):
    """Test validate_yaml_file with an invalid YAML format."""
    with patch("yaml.load", side_effect=yaml.YAMLError("error parsing YAML")):
        result = validate_yaml_file("invalid.yaml")
        assert result == (False, "There was an issue while trying to read with your AI Settings file: error parsing YAML")

def test_validate_yaml_file_with_pathlib_path(setup_file_mock, setup_yaml_loader_mock):
    """Test validate_yaml_file with a Path object instead of a string."""
    path = Path("valid.yaml")
    result = validate_yaml_file(path)
    assert result == (True, "Successfully validated \x1b[36m`valid.yaml`\x1b[39m!")
    setup_file_mock.assert_called_once_with(path, encoding="utf-8")
    setup_yaml_loader_mock.assert_called_once()

def test_validate_yaml_file_with_non_string_non_path_input():
    """Test validate_yaml_file with input that is neither a string nor a Path."""
    with pytest.raises((TypeError, OSError)):
        validate_yaml_file(123)  # Passing an integer should raise a TypeError or OSError