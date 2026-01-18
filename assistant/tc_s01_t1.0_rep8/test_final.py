import pytest
from unittest.mock import patch, mock_open
from put import validate_yaml_file  # Importing all necessary functions from module `put`

def test_valid_yaml_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "valid.yaml"
    p.write_text("a: 1\nb: 2")

    result, msg = validate_yaml_file(p)
    assert result
    assert "Successfully validated" in msg

def test_file_not_found():
    non_existing_file = 'non_existent.yaml'
    result, msg = validate_yaml_file(non_existing_file)
    assert not result
    assert "wasn't found" in msg

def test_invalid_yaml_content():
    with patch("builtins.open", mock_open(read_data=": :")):
        result, msg = validate_yaml_file("invalid.yaml")
        assert not result
        assert "issue while trying to read with your AI Settings file" in msg

def test_file_path_object_with_valid_content(tmp_path):
    p = tmp_path / "valid.yaml"
    p.write_text("a: 1\nb: 2\n")

    result, msg = validate_yaml_file(p)
    assert result
    assert "Successfully validated" in msg

@pytest.fixture(scope="module")
def create_fake_yaml_file(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    temp_file = temp_dir / "temp.yaml"
    temp_file.write_text("a: 1\nb: 2")
    yield temp_file
    temp_file.unlink()

def test_with_fixture_valid_yaml(create_fake_yaml_file):
    result, msg = validate_yaml_file(create_fake_yaml_file)
    assert result
    assert "Successfully validated" in msg

def test_error_message_consistency_for_not_found():
    non_existing_file = 'definitely_non_existent.yaml'
    result, msg = validate_yaml_file(non_existing_file)
    assert "The file " in msg and "wasn't found" in msg and "XX" not in msg

def test_error_message_integrity_for_yaml_parsing_failures():
    with patch("builtins.open", mock_open(read_data=": :")):
        result, msg = validate_yaml_file("corrupted.yaml")
        assert "XXThere was an issue" not in msg and "XX" not in msg and "There was an issue while trying to read with your AI Settings file:" in msg

# New test cases that will fail against the mutated code

def test_success_message_no_extra_characters(tmp_path):
    """Test to ensure no extra 'XX' characters are in the success message."""
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "valid.yaml"
    p.write_text("a: 1\nb: 2")

    result, msg = validate_yaml_file(p)
    assert result
    assert "XX" not in msg  # this will fail in the mutant version
    assert "Successfully validated" in msg