import pytest
from put import validate_yaml_file
from pathlib import Path
from colorama import Fore

@pytest.fixture
def setup_file(tmp_path):
    # Create a temporary directory and a file with valid YAML format
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "testfile.yaml"
    p.write_text("name: test\nvalue: 1")
    return str(p)  # Return path as a string to match file input type expectations

def test_validate_yaml_valid_file(setup_file):
    result, message = validate_yaml_file(setup_file)
    assert result == True
    assert "Successfully validated" in message

def test_validate_yaml_non_existing_file():
    non_existing_file = "nonexistent.yaml"
    result, message = validate_yaml_file(non_existing_file)
    assert not result
    assert "wasn't found" in message

def test_validate_yaml_non_existing_file_message():
    non_existing_file = "nonexistent.yaml"
    result, message = validate_yaml_file(non_existing_file)
    expected_message = f"The file {Fore.CYAN}`{non_existing_file}`{Fore.RESET} wasn't found"
    assert expected_message in message

def test_validate_yaml_very_long_file_name(tmp_path):
    very_long_filename = "a" * 256 + ".yaml"
    path = tmp_path / very_long_filename
    try:
        path.write_text("name: test\nvalue: 1")
        result, message = validate_yaml_file(str(path))
        assert result
        assert "Successfully validated" in message
    except OSError as e:
        assert "Invalid argument" in str(e) or "No such file or directory" in str(e)

def test_validate_yaml_mutated_error_message(tmp_path):
    p = tmp_path / "invalid_syntax.yaml"
    p.write_text("{incorrectly: 'formatted, missing: 'closing'}")
    result, message = validate_yaml_file(str(p))
    normal_error_msg_intro = "There was an issue while trying to read with your AI Settings file:"
    assert not result
    assert normal_error_msg_intro in message
    assert "XX" not in message

# New test case to specifically detect mutation in success message
def test_validate_yaml_success_message_mutation(setup_file):
    result, message = validate_yaml_file(setup_file)
    assert result == True
    # Check that the mutated 'XX' tags are not present in the success message
    assert "XX" not in message
