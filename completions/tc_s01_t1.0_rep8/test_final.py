from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file

# def test_validate_yaml_good_file():
#     result = validate_yaml_file("good_example.yaml")
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

def test_validate_yaml_nonexistent_file():
    result = validate_yaml_file("nonexistent.yaml")
    assert result[0] == False
    assert "wasn't found" in result[1]

# def test_validate_yaml_empty_file():
#     result = validate_yaml_file("empty.yaml")
#     assert result[0] == False
#     assert "AI Settings file" in result[1]

# def test_validate_yaml_with_invalid_yaml_syntax():
#     result = validate_yaml_file("invalid.yaml")
#     assert result[0] == False
#     assert "AI Settings file" in result[1]

# def test_validate_yaml_with_invalid_yaml_structure():
#     result = validate_yaml_file("invalid_structure.yaml")
#     assert result[0] == False
#     assert "AI Settings file" in result[1]

# def test_validate_yaml_with_binary_file():
#     result = validate_yaml_file("binaryfile.bin")
#     assert result[0] == False
#     assert "AI Settings file" in result[1]

def test_validate_yaml_with_none_input():
    with pytest.raises(TypeError):
        validate_yaml_file(None)

# def test_validate_yaml_with_integer_input():
#     with pytest.raises(TypeError):
#         validate_yaml_file(12345)

def test_validate_yaml_with_dict_input():
    with pytest.raises(TypeError):
        validate_yaml_file({'path': 'somefile.yaml'})

def test_validate_yaml_with_list_input():
    with pytest.raises(TypeError):
        validate_yaml_file(['somefile.yaml', 'anotherfile.yaml'])

# def test_validate_yaml_with_path_object():
#     path = Path("good_example.yaml")
#     result = validate_yaml_file(path)
#     assert result[0] == True
#     assert "Successfully validated" in result[1]

# def test_validate_yaml_valid_encoding():
#     result = validate_yaml_file("valid_example.yaml")
#     assert result[0] == True
#     assert "Successfully validated" in result[1]