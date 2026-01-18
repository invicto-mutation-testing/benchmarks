from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_with_nonexistent_path():
    result = validate_yaml_file("nonexistent_file.yaml")
    assert result[0] == False
    assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_directory_instead_of_file():
#     result = validate_yaml_file(Path("."))
#     assert result[0] == False
#     assert "wasn't found" in result[1]

def test_validate_yaml_file_with_invalid_yaml_content(tmp_path):
    p = tmp_path / "invalid.yaml"
    p.write_text("unbalanced brackets: [}")
    result = validate_yaml_file(p)
    assert result[0] == False
    assert "issue while trying to read" in result[1]

def test_validate_yaml_file_with_valid_yaml_content(tmp_path):
    p = tmp_path / "valid.yaml"
    p.write_text("key: value")
    result = validate_yaml_file(p)
    assert result[0] == True
    assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_empty_file(tmp_path):
#     p = tmp_path / "empty.yaml"
#     p.write_text("")
#     result = validate_yaml_file(p)
#     assert result[0] == False
#     assert "issue while trying to read" in result[1]

def test_validate_yaml_file_with_binary_file(tmp_path):
    p = tmp_path / "binary.dat"
    p.write_bytes(b'\x00\x01\x02')
    result = validate_yaml_file(p)
    assert result[0] == False
    assert "issue while trying to read" in result[1]

# def test_validate_yaml_file_with_specific_not_found_message():
#     result = validate_yaml_file("nonexistent_file.yaml")
#     assert result[0] == False
#     assert "XXThe file" not in result[1]



# def test_validate_yaml_file_with_specific_error_message(tmp_path):
#     p = tmp_path / "invalid.yaml"
#     p.write_text("unbalanced brackets: [}")
#     result = validate_yaml_file(p)
#     assert "XX" not in result[1]



# def test_validate_yaml_file_success_message(tmp_path):
#     p = tmp_path / "valid.yaml"
#     p.write_text("key: value")
#     result = validate_yaml_file(p)
#     assert result[0] == True
#     assert "XXSuccessfully validated" not in result[1]

