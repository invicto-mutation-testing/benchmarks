from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def test_validate_yaml_file_valid():
    # Test with a valid YAML file
    with open("valid_yaml.yaml", "w") as f:
        f.write("name: Test\nversion: 1.0")
    result = validate_yaml_file("valid_yaml.yaml")
    assert result == (True, f"Successfully validated {Fore.CYAN}`valid_yaml.yaml`{Fore.RESET}!")

def test_validate_yaml_file_not_found():
    # Test with a non-existent file
    result = validate_yaml_file("non_existent.yaml")
    assert result == (False, f"The file {Fore.CYAN}`non_existent.yaml`{Fore.RESET} wasn't found")

def test_validate_yaml_file_invalid_yaml():
    # Test with an invalid YAML content
    with open("invalid_yaml.yaml", "w") as f:
        f.write("{unclosed: 'bracket'")
    result = validate_yaml_file("invalid_yaml.yaml")
    assert "There was an issue while trying to read with your AI Settings file:" in result[1]

# def test_validate_yaml_file_empty_file():
#     # Test with an empty file
#     with open("empty_yaml.yaml", "w") as f:
#         pass
#     result = validate_yaml_file("empty_yaml.yaml")
#     assert "There was an issue while trying to read with your AI Settings file:" in result[1]

# def test_validate_yaml_file_non_string_input():
#     # Test with non-string and non-Path input
#     result = validate_yaml_file(123)
#     assert "There was an issue while trying to read with your AI Settings file:" in result[1]

def test_validate_yaml_file_path_object():
    # Test with Path object
    path = Path("valid_yaml.yaml")
    with open(path, "w") as f:
        f.write("name: Test\nversion: 1.0")
    result = validate_yaml_file(path)
    assert result == (True, f"Successfully validated {Fore.CYAN}`{path}`{Fore.RESET}!")

# def test_validate_yaml_file_invalid_yaml_should_fail():
#     # Test with an invalid YAML content that should fail in the mutated code
#     with open("invalid_yaml.yaml", "w") as f:
#         f.write("{unclosed: 'bracket'")
#     result = validate_yaml_file("invalid_yaml.yaml")
#     assert result == (False, f"There was an issue while trying to read with your AI Settings file: while parsing a block mapping\n  in \"invalid_yaml.yaml\", line 1, column 1\ndid not find expected key\n  in \"invalid_yaml.yaml\", line 1, column 15")



# def test_validate_yaml_file_error_message():
#     # Test with an invalid YAML content to check specific error message
#     with open("invalid_yaml.yaml", "w") as f:
#         f.write("{unclosed: 'bracket'")
#     result = validate_yaml_file("invalid_yaml.yaml")
#     assert result == (False, f"XXThere was an issue while trying to read with your AI Settings file: while parsing a block mapping\n  in \"invalid_yaml.yaml\", line 1, column 1\ndid not find expected key\n  in \"invalid_yaml.yaml\", line 1, column 15XX")
