from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file

# def test_validate_yaml_valid_file():
#     # Create a temporary valid YAML file
#     test_file = Path("temp_valid.yaml")
#     test_file.write_text("test: valid")
#     assert validate_yaml_file(test_file) == (True, f"Successfully validated `{test_file}`!")
#     # Cleanup
#     test_file.unlink()

def test_validate_yaml_invalid_yaml():
    # Create a temporary invalid YAML file
    test_file = Path("temp_invalid.yaml")
    test_file.write_text("test: [invalid: yaml")
    result = validate_yaml_file(test_file)
    assert result[0] == False and "There was an issue while trying to read with your AI Settings file:" in result[1]
    # Cleanup
    test_file.unlink()

# def test_validate_yaml_non_existent_file():
#     # Non-existent file path
#     test_file = Path("non_existent.yaml")
#     result = validate_yaml_file(test_file)
#     assert result == (False, f"The file `{test_file}` wasn't found")

# def test_validate_yaml_with_directory_input():
#     # Path to a directory instead of a file
#     test_path = Path(".")
#     result = validate_yaml_file(test_path)
#     assert not result[0] and "is not a file" in result[1]

def test_validate_yaml_with_none_input():
    # None as file path
    with pytest.raises(TypeError):
        validate_yaml_file(None)

# def test_validate_yaml_with_integer_input():
#     # Integer as file path
#     with pytest.raises(TypeError):
#         validate_yaml_file(12345)

# def test_validate_yaml_non_existent_file_check_return_false():
#     # Test to ensure FileNotFoundError handling returns False as the first part of the tuple
#     non_existent_file = Path("does_not_exist.yaml")
#     assert validate_yaml_file(non_existent_file) == (False, f"The file `does_not_exist.yaml` wasn't found")



# def test_validate_yaml_file_not_found_message():
#     # Test to specifically check the error message for a non-existent file
#     test_file = Path("definitely_non_existent.yaml")
#     result = validate_yaml_file(test_file)
#     assert result == (False, f"The file `definitely_non_existent.yaml` wasn't found")

