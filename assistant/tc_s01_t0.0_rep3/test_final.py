import pytest
from unittest.mock import mock_open, patch
from put import validate_yaml_file
from pathlib import Path
import yaml
from colorama import Fore

# Test cases
class TestValidateYamlFile:
    def test_validate_yaml_file_valid(self):
        # Test with valid YAML content
        with patch("builtins.open", mock_open(read_data="name: Test"), create=True) as mocked_file:
            result = validate_yaml_file("valid.yaml")
            assert result == (True, f"Successfully validated {Fore.CYAN}`valid.yaml`{Fore.RESET}!")

    def test_validate_yaml_file_not_found(self):
        # Test file not found scenario
        with patch("builtins.open", mock_open(), create=True) as mocked_file:
            mocked_file.side_effect = FileNotFoundError
            result = validate_yaml_file("nonexistent.yaml")
            assert result == (False, f"The file {Fore.CYAN}`nonexistent.yaml`{Fore.RESET} wasn't found")

    def test_validate_yaml_file_invalid_yaml(self):
        # Test with invalid YAML content
        with patch("builtins.open", mock_open(read_data=": invalid_yaml"), create=True):
            result = validate_yaml_file("invalid.yaml")
            assert result[0] == False
            assert "There was an issue while trying to read with your AI Settings file:" in result[1]

    def test_validate_yaml_file_with_path_object(self):
        # Test with Path object as input
        path_input = Path("valid.yaml")
        with patch("builtins.open", mock_open(read_data="name: Test"), create=True):
            result = validate_yaml_file(path_input)
            assert result == (True, f"Successfully validated {Fore.CYAN}`{path_input}`{Fore.RESET}!")

    def test_validate_yaml_file_non_string_path_input(self):
        # Test with non-string and non-Path input
        with pytest.raises(OSError):
            validate_yaml_file(12345)  # Input is an integer

    def test_validate_yaml_file_encoding_error(self):
        # Test to ensure the file is opened with the correct encoding
        with patch("builtins.open") as mocked_open:
            mocked_open.side_effect = lambda *args, **kwargs: mock_open(read_data="name: Test")(*args, **kwargs) if kwargs.get('encoding') == 'utf-8' else None
            result = validate_yaml_file("valid.yaml")
            mocked_open.assert_called_with("valid.yaml", encoding="utf-8")
            assert result == (True, f"Successfully validated {Fore.CYAN}`valid.yaml`{Fore.RESET}!")

    # New test case to catch the mutation in the error message
    def test_validate_yaml_file_invalid_yaml_error_message(self):
        # Test to ensure the error message does not contain the mutation
        with patch("builtins.open", mock_open(read_data=": invalid_yaml"), create=True):
            result = validate_yaml_file("invalid.yaml")
            assert "XXThere was an issue while trying to read with your AI Settings file:" not in result[1]
            assert "There was an issue while trying to read with your AI Settings file:" in result[1]