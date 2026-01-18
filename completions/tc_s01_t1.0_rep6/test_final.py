import tempfile
from pathlib import Path

import pytest
import yaml
from colorama import Fore
from nds_script import validate_yaml_file


def setup_yaml_files():
    valid_yaml_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    invalid_yaml_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    empty_yaml_file = tempfile.NamedTemporaryFile(delete=False, mode='w')

# def test_valid_yaml():
#     assert validate_yaml_file(VALID_YAML) == (True, f"Successfully validated `{VALID_YAML}`!")

# def test_invalid_yaml_syntax():
#     response = validate_yaml_file(INVALID_YAML)
#     assert response[0] == False and "There was an issue while trying to read with your AI Settings file:" in response[1]

# def test_nonexistent_file():
#     response = validate_yaml_file("nonexistent_file.yaml")
#     assert response[0] == False and "`nonexistent_file.yaml` wasn't found" in response[1]

# def test_empty_file():
#     response = validate_yaml_file(EMPTY_YAML)
#     assert response[0] == False and "There was an issue while trying to read with your AI Settings file:" in response[1]

def test_with_null_input():
    with pytest.raises(TypeError):
        validate_yaml_file(None)

# def test_with_integer_input():
#     with pytest.raises(TypeError):
#         validate_yaml_file(12345)

def test_with_list_input():
    with pytest.raises(TypeError):
        validate_yaml_file([])

def test_with_dict_input():
    with pytest.raises(TypeError):
        validate_yaml_file({})

# def test_encoding_error_in_mutant():
#     # Prepare a real temporary valid YAML file
#     f = Path("tempfile.yaml")
#     with open(f, "w") as file:
#         file.writelines([
#             "example:\n",
#             "  key: value\n"
#         ])
#     # Using the original function, it should validate properly
#     assert validate_yaml_file(f)[0] == True
#     # Cleanup created file
#     f.unlink()



# def test_nonexistent_file_should_fail_in_mutant():
#     # This test should pass with the original, failing with the mutant which incorrectly reports missing files found
#     response = validate_yaml_file("nonexistent_file.yaml")
#     assert response == (False, f"The file `nonexistent_file.yaml` wasn't found")



# def test_missing_file_error_message():
#     # This test checks the error message for a nonexistent YAML file
#     # It should pass with the original code but fail with the mutant code due to changed error message format
#     response = validate_yaml_file("nonexistent_file.yaml")
#     expected_message = "The file `nonexistent_file.yaml` wasn't found"
#     assert response == (False, expected_message)



def test_structurally_invalid_yaml():
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
        tmp.write("invalid_yaml: {unbalanced_brackets: [}")
        tmp_path = Path(tmp.name)
    response = validate_yaml_file(tmp_path)
    assert response[0] == False and "There was an issue while trying to read with your AI Settings file:" in response[1]
    tmp_path.unlink()  # Clean up



# def test_explicit_detection_of_mutant_error_message():
#     expected_message = (False, f"XXThere was an issue while trying to read with your AI Settings file: could not find expected ':'XX")
#     with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
#         tmp.write("invalid_yaml: \n  unbalanced_bracket: [")
#         tmp_path = Path(tmp.name)
#     response = validate_yaml_file(tmp_path)
#     assert response != expected_message
#     tmp_path.unlink()



# def test_mutated_success_message():
#     f = tempfile.NamedTemporaryFile(delete=False, mode='w')
#     try:
#         f.write("example:\n  key: value\n")
#         f.flush()  # Ensure data is written to disk
#         f.close()
#         result = validate_yaml_file(f.name)
#         assert result == (True, f"Successfully validated `{f.name}`!")
#     finally:
#         Path(f.name).unlink()

