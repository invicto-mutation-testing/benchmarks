

import pytest
from nds_script import correct_asserts_indent


def test_correct_indentation_single_line():
    initial_code = "assert True"
    expected_code = "assert True"
    assert correct_asserts_indent(initial_code) == expected_code

def test_correct_indentation_multiple_lines():
    initial_code = "def test_function():\n    assert True\n    assert False"
    expected_code = "def test_function():\n        assert True\n        assert False"
    assert correct_asserts_indent(initial_code) == expected_code

def test_correct_indentation_varied_spacing():
    initial_code = "def test_function():\n  assert True\n\tassert False"
    expected_code = "def test_function():\n        assert True\n        assert False"
    assert correct_asserts_indent(initial_code) == expected_code

def test_input_empty_string():
    initial_code = ""
    expected_code = ""
    assert correct_asserts_indent(initial_code) == expected_code

def test_input_single_newline():
    initial_code = "\n"
    expected_code = ""
    assert correct_asserts_indent(initial_code) == expected_code

def test_input_multiple_newlines_space():
    initial_code = "\n\n   \n"
    expected_code = ""
    assert correct_asserts_indent(initial_code) == expected_code

def test_input_non_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_input_integer_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_list_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(["def test_function():", "    assert True"])

def test_input_dict_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent({"code": "assert True"})

def test_input_string_type_error_message():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(None)



# def test_correct_indentation_empty_lines():
#     initial_code = "def test_function():\n    assert True\n\n    assert False"
#     expected_code = "def test_function():\n        assert True\n\n        assert False"
#     assert correct_asserts_indent(initial_code) == expected_code



def test_correct_indentation_single_character_line():
    initial_code = "assert True\na"
    expected_code = "assert True\n        a"
    assert correct_asserts_indent(initial_code) == expected_code

