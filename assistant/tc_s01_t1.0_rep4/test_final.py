import pytest
from put import validate_yaml_file
from colorama import Fore
from pathlib import Path
import tempfile
import os

def test_validate_yaml_file():
    """Test cases for the validate_yaml_file function."""

    # Setup: create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    valid_yaml_content = """
    field1: value1
    field2:
      subfield: value2
    """
    invalid_yaml_content = """
    field1: value1
    field2
      subfield: value2
    """
    non_yaml_file = "not_a_yaml_file.txt"
    valid_file_path = os.path.join(temp_dir, "valid_yaml.yaml")
    invalid_file_path = os.path.join(temp_dir, "invalid_yaml.yaml")
    non_existing_file_path = os.path.join(temp_dir, "non_existing.yaml")

    # Create a valid yaml file
    with open(valid_file_path, 'w') as valid_file:
        valid_file.write(valid_yaml_content)
    
    # Create an invalid yaml file
    with open(invalid_file_path, 'w') as invalid_file:
        invalid_file.write(invalid_yaml_content)

    # Test for successful validation
    result = validate_yaml_file(valid_file_path)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{valid_file_path}`{Fore.RESET}!"), "Test should pass for valid YAML content"

    # Test for file not found
    result = validate_yaml_file(non_existing_file_path)
    assert result == (False, f"The file {Fore.CYAN}`{non_existing_file_path}`{Fore.RESET} wasn't found"), "Test should handle file not found correctly"
    
    # Test for YAML error handling
    result = validate_yaml_file(invalid_file_path)
    assert result[0] == False and "There was an issue while trying to read with your AI Settings file: while scanning a simple key" in result[1], "Test should handle invalid YAML content correctly"

    # Test for detection of mutation in error messages
    assert "XX" not in result[1], "No mutant `XX` signs should appear in error messages."

    # Cleanup: Remove temporary directory and all its content
    os.remove(valid_file_path)
    os.remove(invalid_file_path)
    os.rmdir(temp_dir)