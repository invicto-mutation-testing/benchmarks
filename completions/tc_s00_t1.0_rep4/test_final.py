

import pytest
from nds_script import correct_asserts_indent


def test_correct_indentation_single_line_code():
    code = "assert True"
    expected = "assert True"
    assert correct_asserts_indent(code) == expected

def test_correct_indentation_multiple_lines_code():
    code = "def test_function():\n  assert True\n  assert False"
    expected = "def test_function():\n        assert True\n        assert False"
    assert correct_asserts_indent(code) == expected

def test_correct_indentation_with_empty_lines():
    code = "def test_function():\n\n  assert True\n\n  assert False\n"
    expected = "def test_function():\n        assert True\n        assert False"
    assert correct_asserts_indent(code) == expected

def test_input_is_not_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_input_is_integer_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_is_list_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(["assert True"])

def test_input_is_dict_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent({"code": "assert True"})

def test_input_is_tuple_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(("assert True",))

def test_empty_string_input():
    code = ""
    expected = ""
    assert correct_asserts_indent(code) == expected

def test_whitespace_only_string_input():
    code = "     "
    expected = ""
    assert correct_asserts_indent(code) == expected

def test_correct_indentation_with_comments():
    code = "def test_function():\n  # Check true\n  assert True\n  # Done"
    expected = "def test_function():\n        # Check true\n        assert True\n        # Done"
    assert correct_asserts_indent(code) == expected

def test_string_type_error_message():
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(123)
    assert str(exc_info.value) == "Input must be a string"



# def test_handle_single_character_line():
#     code = "def test_function():\n a\n b"
#     expected = "def test_function():\n        a\n        b"
#     assert correct_asserts_indent(code) == expected

