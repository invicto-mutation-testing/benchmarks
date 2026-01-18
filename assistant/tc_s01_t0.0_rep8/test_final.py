import pytest
from put import validate_yaml_file
from pathlib import Path
from unittest.mock import mock_open, patch
import yaml
from colorama import Fore

# Setup a fixture for creating a temporary file path
@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "temp.yaml"

# Test cases for the function validate_yaml_file
class TestValidateYamlFile:
    # Test with a valid YAML file
    def test_validate_yaml_file_valid(self, temp_file):
        # Prepare a valid YAML content
        content = "key: value"
        temp_file.write_text(content, encoding="utf-8")
        
        # Test the function
        result = validate_yaml_file(temp_file)
        assert result == (True, f"Successfully validated {Fore.CYAN}`{temp_file}`{Fore.RESET}!"), "Should return success message for valid YAML"

    # Test with a non-existent file
    def test_validate_yaml_file_non_existent(self, temp_file):
        # Prepare a non-existent file path
        non_existent_file = temp_file.with_name("non_existent.yaml")
        
        # Test the function
        result = validate_yaml_file(non_existent_file)
        assert result == (False, f"The file {Fore.CYAN}`{non_existent_file}`{Fore.RESET} wasn't found"), "Should return file not found message"

    # Test with a file containing invalid YAML
    def test_validate_yaml_file_invalid_yaml(self, temp_file):
        # Prepare an invalid YAML content
        content = "{unclosed: dict"
        temp_file.write_text(content, encoding="utf-8")
        
        # Test the function
        result = validate_yaml_file(temp_file)
        assert "There was an issue while trying to read with your AI Settings file:" in result[1], "Should return YAML error message"

    # Test with a file path as a string
    def test_validate_yaml_file_path_as_string(self, temp_file):
        # Prepare a valid YAML content
        content = "key: value"
        temp_file.write_text(content, encoding="utf-8")
        
        # Test the function using the file path as a string
        result = validate_yaml_file(str(temp_file))
        assert result == (True, f"Successfully validated {Fore.CYAN}`{str(temp_file)}`{Fore.RESET}!"), "Should handle string paths correctly"

    # Test with incorrect file type input
    def test_validate_yaml_file_incorrect_input_type(self):
        # Test the function with incorrect input type
        with pytest.raises(OSError):
            validate_yaml_file(123)  # Passing an integer instead of a string or Path

    # Test with None as input
    def test_validate_yaml_file_none_input(self):
        # Test the function with None as input
        with pytest.raises(TypeError):
            validate_yaml_file(None)  # Passing None

    # Test with an empty string as file path
    def test_validate_yaml_file_empty_string(self):
        # Test the function with an empty string
        result = validate_yaml_file("")
        assert result == (False, f"The file {Fore.CYAN}`{''}`{Fore.RESET} wasn't found"), "Should handle empty string paths correctly"

    # New test case to catch the mutation in the error message
    def test_validate_yaml_file_error_message_format(self, temp_file):
        # Prepare an invalid YAML content
        content = "{unclosed: dict"
        temp_file.write_text(content, encoding="utf-8")
        
        # Test the function
        result = validate_yaml_file(temp_file)
        assert "XX" not in result[1], "Error message should not contain 'XX'"