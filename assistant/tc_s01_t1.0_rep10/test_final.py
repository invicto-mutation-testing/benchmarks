import pytest
from put import validate_yaml_file
from pathlib import Path
import yaml  # Importing yaml for handling YAML operations in mocked tests

@pytest.mark.parametrize("invalid_file_input", [123, None, 3.14, [], {}])
def test_invalid_file_input_type_exception(invalid_file_input):
    """
    Test various non-string and non-Path types to check if they lead to an exception,
    focusing on testing improper input types which should logically not be processed by
    the file reading function without causing some type of error.
    """
    with pytest.raises(Exception):
        validate_yaml_file(invalid_file_input)

@pytest.fixture(scope="module")
def create_valid_yaml_file(tmp_path_factory):
    """
    Fixture to create a valid YAML file for testing.
    """
    file_path = tmp_path_factory.mktemp("data") / "valid_yaml.yml"
    content = "name: OpenAI\nversion: 1.0"
    with open(file_path, "w", encoding="utf-8") as yaml_file:
        yaml_file.write(content)
    return file_path

@pytest.mark.parametrize("valid_file_input,expected", [
    ("tests/data/valid_yaml.yml", True),
    (Path("tests/data/valid_yaml.yml"), True)
])
def test_valid_file_input_encoding(valid_file_input, expected, create_valid_yaml_file):
    """
    Test that valid YAML files are handled correctly.
    """
    result, message = validate_yaml_file(create_valid_yaml_file)
    assert result == expected, "The validation function should return True for valid YAML files with correct encoding."

@pytest.mark.parametrize("valid_file_input", [
    ("tests/data/valid_yaml.yml"),
    Path("tests/data/valid_yaml.yml")
])
def test_invalid_encoding_exception(valid_file_input, monkeypatch):
    """
    Test invalid encoding handling.
    """
    def mock_open(*args, **kwargs):
        assert 'encoding' not in kwargs or kwargs['encoding'] == 'utf-8', "Encoding should be 'utf-8'"
        original_open(*args, **kwargs)

    original_open = open
    monkeypatch.setattr("builtins.open", mock_open)
    try:
        validate_yaml_file(valid_file_input)
    finally:
        monkeypatch.undo()

@pytest.mark.parametrize("file_not_found_input", [
    "non_existent_file.yml",
    Path("non_existent_file.yml")
])
def test_file_not_found(file_not_found_input):
    """
    Test FileNotFoundException handling.
    """
    result, message = validate_yaml_file(file_not_found_input)
    assert not result, "Expected result to be False when the file does not exist."
    assert "wasn't found" in message, "Expected error message to state that the file wasn't found."

@pytest.mark.parametrize("yaml_error_input", [
    "tests/data/invalid_yaml.yml",
    Path("tests/data/invalid_yaml.yml")
])
def test_yaml_error_message_correctness(yaml_error_input, monkeypatch):
    """
    Ensure the correct error message is provided when a YAMLError occurs.
    This test should pass on the original code and fail on the mutant due to the mutated error message.
    """
    def mock_load(*args, **kwargs):
        raise yaml.YAMLError("Error parsing YAML")

    monkeypatch.setattr(yaml, "load", mock_load)
    result, message = validate_yaml_file(yaml_error_input)
    assert not result, "Expected result to be False on YAMLError."
    assert "XXThere was an issue" not in message, "Error message should not contain mutated 'XX' prefixes."

# New test case to catch specific mutation in the success message
@pytest.mark.parametrize("valid_file_input", [
    ("tests/data/valid_yaml.yml"),
    Path("tests/data/valid_yaml.yml")
])
def test_validate_message_for_unwanted_characters(valid_file_input, create_valid_yaml_file):
    """
    Test to check for unwanted characters in the success validation message that
    were inserted during code mutation.
    """
    result, message = validate_yaml_file(create_valid_yaml_file)
    assert result, "Expected successful YAML validation."
    assert "XX" not in message, "Success message should not contain 'XX' if not mutated."