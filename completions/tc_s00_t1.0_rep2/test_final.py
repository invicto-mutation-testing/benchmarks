

import pytest
from nds_script import correct_asserts_indent

# def test_correct_indent_single_line():
#     input_code = "assert True"
#     expected_output = "        assert True"
#     assert correct_asserts_indent(input_code) == expected_output

def test_correct_indent_multiple_lines():
    input_code = "assert True\nassert False"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_indent_with_empty_lines():
    input_code = "\nassert True\n\nassert False\n"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_indent_with_various_indentation():
    input_code = "  assert True\n    assert False"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_input_not_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_empty_string():
    assert correct_asserts_indent("") == ""

def test_input_only_whitespace():
    assert correct_asserts_indent("    \n  \t  ") == ""

def test_input_none_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_input_string_error_message():
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(123)
    assert "Input must be a string" in str(exc_info.value)



def test_correct_indent_single_char_line():
    input_code = "a"
    expected_output = "a"
    assert correct_asserts_indent(input_code) == expected_output

