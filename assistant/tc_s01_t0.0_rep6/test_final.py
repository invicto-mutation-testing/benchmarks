import pytest
from put import validate_yaml_file
from pathlib import Path
from unittest.mock import mock_open, patch
import yaml

# Setup and Teardown fixtures
@pytest.fixture
def setup_file_mock():
    # Mock open to simulate file handling
    m = mock_open(read_data="name: Test\nversion: 1.0")
    with patch("builtins.open", m):
        yield m

@pytest.fixture
def setup_pathlib_path_exists():
    # Mock Path.exists() to control file existence checks
    with patch.object(Path, "exists", return_value=True):
        yield

@pytest.fixture
def setup_pathlib_path_not_exists():
    # Mock Path.exists() to simulate non-existing file
    with patch.object(Path, "exists", return_value=False):
        yield

# Original Test cases
def test_validate_yaml_file_with_valid_yaml(setup_file_mock, setup_pathlib_path_exists):
    file_path = "valid.yaml"
    result = validate_yaml_file(file_path)
    assert result == (True, f"Successfully validated \x1b[36m`{file_path}`\x1b[39m!")

def test_validate_yaml_file_with_invalid_yaml(setup_file_mock, setup_pathlib_path_exists):
    setup_file_mock.return_value.read.return_value = "name: Test\nversion: 1.0: :"
    file_path = "invalid.yaml"
    result = validate_yaml_file(file_path)
    assert result[0] == False and "issue while trying to read" in result[1]

def test_validate_yaml_file_file_not_found(setup_pathlib_path_not_exists):
    file_path = "nonexistent.yaml"
    result = validate_yaml_file(file_path)
    assert result == (False, f"The file \x1b[36m`{file_path}`\x1b[39m wasn't found")

def test_validate_yaml_file_with_path_object(setup_file_mock, setup_pathlib_path_exists):
    file_path = Path("valid.yaml")
    result = validate_yaml_file(file_path)
    assert result == (True, f"Successfully validated \x1b[36m`{file_path}`\x1b[39m!")

def test_validate_yaml_file_with_empty_string():
    file_path = ""
    result = validate_yaml_file(file_path)
    assert result == (False, f"The file \x1b[36m`{file_path}`\x1b[39m wasn't found")

# New Test cases to catch mutation
def test_validate_yaml_file_with_invalid_yaml_mutation(setup_file_mock, setup_pathlib_path_exists):
    setup_file_mock.return_value.read.return_value = "name: Test\nversion: 1.0: :"
    file_path = "invalid.yaml"
    result = validate_yaml_file(file_path)
    assert "XX" not in result[1], "Mutation detected: Unexpected 'XX' in error message"