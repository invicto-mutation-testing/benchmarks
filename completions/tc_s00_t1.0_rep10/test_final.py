

import pytest
from nds_script import correct_asserts_indent


def test_input_non_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_boolean_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(True)

def test_input_list_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent([])

def test_input_dict_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent({})

def test_input_none_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_empty_string_input():
    assert correct_asserts_indent("") == ""

def test_single_line_input():
    code = "assert True"
    expected = "assert True"
    assert correct_asserts_indent(code) == expected

def test_multiple_lines_input():
    code = "def function():\n    assert x == 1\n    assert y == 2"
    expected = "def function():\n        assert x == 1\n        assert y == 2"
    assert correct_asserts_indent(code) == expected

def test_input_with_different_indentation_levels():
    code = "def function():\n  assert x == 1\n     assert y == 2\nassert z == 3"
    expected = "def function():\n        assert x == 1\n        assert y == 2\n        assert z == 3"
    assert correct_asserts_indent(code) == expected

def test_input_with_no_asserts():
    code = "def function():\n    x = 1\n    y = 2"
    expected = "def function():\n        x = 1\n        y = 2"
    assert correct_asserts_indent(code) == expected

def test_type_error_message():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(123)



# def test_input_with_empty_lines():
#     code = "def function():\n    \n  assert x == 1"
#     expected = "def function():\n\n        assert x == 1"
#     assert correct_asserts_indent(code) == expected



def test_single_letter_line_with_proper_failure():
    code = "a\n a"
    expected_original = "a\n        a"
    expected_mutant = "a\n"

