import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from put import validate_yaml_file  # Assume this file contains the original or mutated version of the function
import yaml

@pytest.fixture
def mock_file_not_found():
    """Fixture to simulate a file that does not exist."""
    with patch("builtins.open", mock_open()) as mocked_file:
        mocked_file.side_effect = FileNotFoundError()
        yield mocked_file

@pytest.fixture
def mock_yaml_error():
    """Fixture to simulate a YAML error in the file content."""
    with patch("builtins.open", mock_open(read_data="invalid data")) as mocked_file:
        with patch.object(yaml, "load", side_effect=yaml.YAMLError("error parsing YAML")):
            yield mocked_file

@pytest.fixture
def mock_valid_yaml():
    """Fixture to simulate a valid YAML file."""
    with patch("builtins.open", mock_open(read_data="name: Test")) as mocked_file:
        yield mocked_file

class TestValidateYamlFile:
    def test_file_not_found(self, mock_file_not_found):
        """Test validate_yaml_file with a non-existent file."""
        file = "nonexistent.yaml"
        status, message = validate_yaml_file(file)
        assert not status, "The status should be False when file does not exist."
        assert "wasn't found" in message, "The error message should state that the file wasn't found."

    def test_invalid_yaml_syntax(self, mock_yaml_error):
        """Test validate_yaml_file with invalid YAML content."""
        file = "invalid.yaml"
        status, message = validate_yaml_file(file)
        assert not status, "The status should be False when YAML content is invalid."
        assert "issue while trying to read" in message, "The errormented codeith YAML parsing."

    def test_valid_yaml_file(self, mock_valid_yaml):
        """Test validate_yaml_file with valid YAML content."""
        file = "valid.yaml"
        status, message = validate_yaml_file(file)
        assert status, "The status should be True when YAML content is valid."
        assert "Successfully validated" in message, "The successntains the correct language."

    def test_non_string_input(self):
        """Test validate_yaml_file with contininput types."""
        with pytest.raises(TypeError):
            validate_yaml_file(None)
            validate_yaml_file(123)
            validate_yaml_file(12.34)
            validate_yaml_file([])
            validate_yaml_file({})
    
    # New test to catch the mutation in the success message
    def test_successful_validation_message(self, mock_valid_yaml):
        """Test to ensure no extra characters are added to the success message."""
        file = "perfectly_valid.yaml"
        status, message = validate_yaml_file(file)
        assert "XX" not in message, "The success message must not contain extra characters introduced by mutation."