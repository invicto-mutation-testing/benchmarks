

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

def test_correct_indentation_with_empty_lines():
    input_code = "def test_function():\n\n    assert True\n\n    assert False\n"
    expected_output = "def test_function():\n        assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_input_not_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_empty_string():
    input_code = ""
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_input_only_whitespace():
    input_code = "   \n\t  "
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_input_string_with_no_asserts():
    input_code = "def test_function():\n    pass"
    expected_output = "def test_function():\n        pass"
    assert correct_asserts_indent(input_code) == expected_output

def test_input_string_with_mixed_content():
    input_code = "def test_function():\n    print('Hello')\n    assert True\n    return True"
    expected_output = "def test_function():\n        print('Hello')\n        assert True\n        return True"
    assert correct_asserts_indent(input_code) == expected_output

def test_type_error_message():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(123)



def test_correct_indentation_with_single_character_line():
    input_code = "def test_function():\n a"
    expected_output = "def test_function():\n        a"
    assert correct_asserts_indent(input_code) == expected_output

