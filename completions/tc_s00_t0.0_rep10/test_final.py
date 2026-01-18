

import pytest
from nds_script import correct_asserts_indent


def test_correct_indentation_single_line():
    input_code = "assert True"
    expected_output = "assert True"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_indentation_multiple_lines():
    input_code = "def test_function():\n    assert True\n    assert False"
    expected_output = "def test_function():\n        assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

# def test_correct_indentation_with_empty_lines():
#     input_code = "def test_function():\n\n    assert True\n\n    assert False"
#     expected_output = "def test_function():\n\n        assert True\n\n        assert False"
#     assert correct_asserts_indent(input_code) == expected_output

def test_correct_indentation_with_comments():
    input_code = "def test_function():\n    # Check condition\n    assert True"
    expected_output = "def test_function():\n        # Check condition\n        assert True"
    assert correct_asserts_indent(input_code) == expected_output

def test_input_not_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_input_integer_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_list_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(["assert True"])

def test_input_dict_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent({"code": "assert True"})

def test_empty_string():
    input_code = ""
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_string_with_only_spaces():
    input_code = "    "
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_string_with_newlines():
    input_code = "\n\n"
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

# def test_input_string_raises_custom_type_error_message():
#     with pytest.raises(TypeError) as exc_info:
#         correct_asserts_indent("Some string")
#     assert str(exc_info.value) == "Input must be a string"



# def test_correct_indentation_with_empty_line_in_between():
#     input_code = "def test_function():\n\n    assert True"
#     expected_output = "def test_function():\n\n        assert True"
#     assert correct_asserts_indent(input_code) == expected_output



def test_correct_indentation_single_character_line():
    input_code = "def test_function():\n a"
    expected_output = "def test_function():\n        a"
    assert correct_asserts_indent(input_code) == expected_output

