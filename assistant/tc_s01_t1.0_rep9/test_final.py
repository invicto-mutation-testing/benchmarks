import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from colorama import Fore
import yaml

from put import validate_yaml_file

# Creating a fixture for a mock file path that does not exist for testing FileNotFoundError
@pytest.fixture
def mock_nonexistent_file():
    return "nonexistent_file.yaml"

# Creating a fixture for a valid YAML content
@pytest.fixture
def valid_yaml_content():
    return "key: value"

# Creating a fixture for invalid YAML content
@pytest.fixture
def invalid_yaml_content():
    return "{bad_yaml: true}"

# Utility fixture for patching the built-in open function
@pytest.fixture
def mock_file_open():
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        yield mock_open

@pytest.mark.parametrize("file_path", [123, None, object(), 5.5])
def test_validate_yaml_file_with_invalid_file_types(file_path):
    """
    Test that validate_yaml_file responds correctly to parameter types that are not str or Path.
    This test is expected to fail if implementation does not handle type checks.
    """
    with pytest.raises((TypeError, OSError)):
        validate_yaml_file(file_path)

def test_validate_yaml_file_file_not_found(mock_nonexistent_file):
    """
    Test validate_yaml_file handling FileNotFoundError.
    """
    result = validate_yaml_file(mock_nonexistent_file)
    expected = (
        False,
        f"The file {Fore.CYAN}`{mock_nonexistent_file}`{Fore.RESET} wasn't found"
    )
    assert result == expected, f"Expected output did not match: {result}"

def test_validate_yaml_file_valid_yaml(mock_file_open, valid_yaml_content):
    """
    Test validate_yaml_file with valid YAML content.
    """
    mock_file_open.return_value.__enter__.return_value.read.return_value = valid_yaml_content
    file_path = "valid.yaml"
    with patch("yaml.load") as mocked_yaml_load:
        mocked_yaml_load.return_value = valid_yaml_content  # Simulate yaml.load success
        result = validate_yaml_file(file_path)
        expected = (True, f"Successfully validated {Fore.CYAN}`{file_path}`{Fore.RESET}!")
        assert result == expected, f"Expected output did not match: {result}"

def test_validate_yaml_file_invalid_yaml(mock_file_open, invalid_yaml_content):
    """
    Test validate_yaml_file with invalid YAML content and catch YAMLError.
    """
    mock_file_open.return_value.__enter__.return_value.read.return_value = invalid_yaml_content
    file_path = "invalid.yaml"
    with patch("yaml.load", side_effect=yaml.YAMLError("mocked yaml error")) as mocked_yaml_load:
        result = validate_yaml_file(file_path)
        expected = (
            False,
            f"There was an issue while trying to read with your AI Settings file: mocked yaml error",
        )
        assert result == expected, f"Expected output did not match: {result}"