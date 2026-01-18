

import pytest
from nds_script import correct_asserts_indent


def test_correct_asserts_indent_normal_case():
    input_code = "def example():\n    assert x == 1"
    expected_output = "def example():\n        assert x == 1"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_multiple_lines():
    input_code = "def example():\n    assert x == 1\n    assert y == 2"
    expected_output = "def example():\n        assert x == 1\n        assert y == 2"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_empty_string():
    assert correct_asserts_indent("") == ""

def test_correct_asserts_indent_single_line_no_assert():
    input_code = "def example(): pass"
    expected_output = "def example(): pass"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_mixed_content():
    input_code = "def example():\n    if x == 1:\n        assert x == 1\n    print('done')"
    expected_output = "def example():\n        if x == 1:\n        assert x == 1\n        print('done')"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_tabs_instead_of_spaces():
    input_code = "def example():\n\tassert x == 1"
    expected_output = "def example():\n        assert x == 1"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_leading_and_trailing_whitespace():
    input_code = "\n    def example():\n    assert x == 1  \n"
    expected_output = "def example():\n        assert x == 1"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_non_string_input():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_correct_asserts_indent_integer_input():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_correct_asserts_indent_list_input():
    with pytest.raises(TypeError):
        correct_asserts_indent(['def example():', '    assert x == 1'])

def test_correct_asserts_indent_type_error_message():
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(None)
    assert str(exc_info.value) == "Input must be a string"



def test_correct_asserts_indent_incorrect_line_handle():
    input_code = "def example():\n    \n    assert x == 1"
    expected_output = "def example():\n        assert x == 1"
    assert correct_asserts_indent(input_code) == expected_output



# def test_correct_asserts_indent_single_character_line():
#     input_code = "def example():\n    \n    a"
#     expected_output = "def example():\n        a"
#     assert correct_asserts_indent(input_code) == expected_output

