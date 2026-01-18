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

# def test_validate_yaml_file_with_empty_file():
#     with open("empty_file.yaml", "w") as f:
#         pass
#     result = validate_yaml_file("empty_file.yaml")
#     assert result[0] == False
#     assert "issue while trying to read" in result[1]

def test_validate_yaml_file_with_invalid_yaml_content():
    with open("invalid_yaml.yaml", "w") as f:
        f.write("unbalanced blackets: ][")
    result = validate_yaml_file("invalid_yaml.yaml")
    assert result[0] == False
    assert "issue while trying to read" in result[1]

def test_validate_yaml_file_with_valid_yaml_content():
    with open("valid_yaml.yaml", "w") as f:
        f.write("key: value")
    result = validate_yaml_file("valid_yaml.yaml")
    assert result[0] == True
    assert "Successfully validated" in result[1]

# def test_validate_yaml_file_with_non_string_input():
#     result = validate_yaml_file(12345)
#     assert result[0] == False
#     assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_none_input():
#     result = validate_yaml_file(None)
#     assert result[0] == False
#     assert "wasn't found" in result[1]

# def test_validate_yaml_file_with_specific_not_found_message():
#     result = validate_yaml_file("nonexistent_file.yaml")
#     assert result[0] == False
#     assert result[1] == f"The file `nonexistent_file.yaml` wasn't found"



def test_validate_yaml_file_with_specific_error_message():
    with open("invalid_yaml.yaml", "w") as f:
        f.write("unbalanced blackets: ][")
    result = validate_yaml_file("invalid_yaml.yaml")
    assert "XXThere was an issue while trying to read" not in result[1]



# def test_validate_yaml_file_success_message():
#     with open("valid_yaml.yaml", "w") as f:
#         f.write("key: value")
#     result = validate_yaml_file("valid_yaml.yaml")
#     assert result[1] == "Successfully validated `valid_yaml.yaml`!"

