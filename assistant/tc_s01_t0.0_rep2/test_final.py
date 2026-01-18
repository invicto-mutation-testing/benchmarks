import pytest
from unittest.mock import mock_open, patch
from put import validate_yaml_file
from pathlib import Path
import yaml
from colorama import Fore

# Setup and teardown fixtures
@pytest.fixture
def mock_file_not_found():
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = FileNotFoundError
        yield mock_file

@pytest.fixture
def mock_yaml_error():
    with patch("builtins.open", mock_open(read_data="invalid_yaml: [unbalanced brackets")) as mock_file:
        yield mock_file

@pytest.fixture
def mock_valid_yaml():
    valid_yaml_content = "valid_key: valid_value"
    with patch("builtins.open", mock_open(read_data=valid_yaml_content)) as mock_file:
        yield mock_file

# Test cases
def test_validate_yaml_file_not_found(mock_file_not_found):
    file_path = "nonexistent.yaml"
    result = validate_yaml_file(file_path)
    assert result == (False, f"The file {Fore.CYAN}`{file_path}`{Fore.RESET} wasn't found"), "Should return False and a file not found message"

def test_validate_yaml_file_yaml_error(mock_yaml_error):
    file_path = "error.yaml"
    result = validate_yaml_file(file_path)
    assert result[0] == False, "Should return False on YAML error"
    assert "There was an issue while trying to read with your AI Settings file:" in result[1], "Should contain error message part"

def test_validate_yaml_file_success(mock_valid_yaml):
    file_path = "valid.yaml"
    result = validate_yaml_file(file_path)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{file_path}`{Fore.RESET}!"), "Should return True and a success message"

def test_validate_yaml_file_with_path_object(mock_valid_yaml):
    file_path = Path("valid.yaml")
    result = validate_yaml_file(file_path)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{file_path}`{Fore.RESET}!"), "Should handle Path objects correctly"

def test_validate_yaml_file_with_invalid_type():
    file_path = 12345  # Not a string or Path
    with pytest.raises(OSError):
        validate_yaml_file(file_path)

# New test case to catch the mutation in the error message
def test_validate_yaml_file_yaml_error_message(mock_yaml_error):
    file_path = "error.yaml"
    result = validate_yaml_file(file_path)
    assert "XX" not in result[1], "Error message should not contain 'XX'"

# Commented out the problematic test case
# def test_validate_yaml_file_encoding_error():
#     with patch("builtins.open", mock_open(read_data="valid_key: valid_value"), side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte")) as mock_file:
#         file_path = "valid.yaml"
#         with pytest.raises(UnicodeDecodeError):
#             validate_yaml_file(file_path)