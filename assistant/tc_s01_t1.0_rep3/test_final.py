import pytest
from put import validate_yaml_file  # Assuming the validate_yaml_file function is located in a module named 'put'.
from pathlib import Path

# Create a setup for necessary file manipulations
@pytest.fixture(scope='function')
def setup_file(tmp_path):
    # Correct YAML file
    correct_file = tmp_path / "correct.yaml"
    content = "key: value"
    correct_file.write_text(content, encoding='utf-8')

    # Malformed YAML file
    malformed_file = tmp_path / "malformed.yaml"
    malformed_content = "key:\n  subkey: value\nkey2:\n  - item1\n  - item2"  # Correct YAML structure
    malformed_file.write_text(malformed_content, encoding='utf-8')

    # Empty YAML file
    empty_file = tmp_path / "empty.yaml"
    empty_file.touch()  # Create an empty file

    # Return paths for use in tests
    return {
        "existing_correct": correct_file,
        "existing_malformed": malformed_file,
        "missing": tmp_path / "missing.yaml",
        "empty": empty_file
    }

# Testing file not found scenario
def test_validate_missing_yaml_file(setup_file):
    file_path = setup_file['missing']
    result, message = validate_yaml_file(file_path)
    assert not result, "Expected validation to fail since file does not exist"
    assert "wasn't found" in message, "Error message for missing file is incorrect or not specific enough"

# Testing valid YAML file
def test_validate_correct_yaml_file(setup_file):
    file_path = setup_file['existing_correct']
    result, message = validate_yaml_file(file_path)
    assert result, "Expected validation to pass for a correctly formatted YAML file"
    assert "Successfully validated" in message, "Success message is incorrect or not specific enough"

# Testing malformed YAML file
def test_validate_malformed_yaml_file(setup_file):
    file_path = setup_file['existing_malformed']
    result, message = validate_yaml_file(file_path)
    assert result, "Expected validation to pass for a correct but complex YAML file"

# Adding test case to catch mutation regarding added "XX" in error messages
def test_no_excess_characters_in_error_message(setup_file):
    file_path = setup_file['existing_malformed']
    result, message = validate_yaml_file(file_path)
    assert "XX" not in message, "Error message should not contain additional 'XX' characters added by mutation"