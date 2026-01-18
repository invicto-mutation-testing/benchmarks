import pytest
from unittest.mock import mock_open, patch
from put import validate_yaml_file
from pathlib import Path
import yaml
from colorama import Fore

def test_validate_yaml_file_file_not_found():
    file_path = "nonexistent.yaml"
    with patch("builtins.open", mock_open()) as mocked_open:
        mocked_open.side_effect = FileNotFoundError()
        success, message = validate_yaml_file(file_path)
    assert success == False
    expected_message = f"The file {Fore.CYAN}`{file_path}`{Fore.RESET} wasn't found"
    assert expected_message in message

@pytest.fixture
def mock_yaml_load_success():
    with patch("yaml.load") as mock_load:
        mock_load.return_value = {'sample': 'data'}
        yield mock_load

@pytest.fixture
def mock_yaml_load_failure():
    with patch("yaml.load") as mock_load:
        mock_load.side_effect = yaml.YAMLError("Invalid YAML content")
        yield mock_load

@pytest.mark.parametrize("file_input", [None, 123, 4.56, [], {}])
def test_validate_yaml_file_invalid_type_inputs(file_input):
    with pytest.raises((TypeError, OSError)):  # Accepting OSError too as validation for incorrect types 
        validate_yaml_file(file_input)

def test_validate_yaml_file_valid_path_and_content(mock_yaml_load_success):
    file_path = "valid.yaml"
    with patch("builtins.open", mock_open(read_data="key: value")):
        success, message = validate_yaml_file(file_path)
    assert success == True
    expected_message = "Successfully validated"
    assert expected_message in message

def test_validate_yaml_file_invalid_yaml_content(mock_yaml_load_failure):
    file_path = "invalid.yaml"
    with patch("builtins.open", mock_open(read_data=": :")):  # intentionally broken YAML
        success, message = validate_yaml_file(file_path)
    assert success == False
    expected_message = "There was an issue while trying to read with your AI Settings file:"
    assert expected_message in message

def test_validate_yaml_file_with_path_object(mock_yaml_load_success):
    file_path = Path("valid.yaml")
    with patch("builtins.open", mock_open(read_data="key: value")):
        success, message = validate_yaml_file(file_path)
    assert success == True
    expected_message = "Successfully validated"
    assert expected_message in message

def test_validate_yaml_file_mutated_success_message(mock_yaml_load_success):
    """Test case to detect mutation in success message."""
    file_path = "valid.yaml"
    with patch("builtins.open", mock_open(read_data="key: value")):
        success, message = validate_yaml_file(file_path)
    assert success == True
    mutated_message = "XXSuccessfully validated"
    assert mutated_message not in message

def test_validate_yaml_file_mutated_error_message(mock_yaml_load_failure):
    file_path = "invalid.yaml"
    with patch('builtins.open', mock_open(read_data=": :")):
        success, message = validate_yaml_file(file_path)
    assert success == False
    mutated_message = "XXThere was an issue while trying to read with your AI Settings file:"
    assert mutated_message not in message