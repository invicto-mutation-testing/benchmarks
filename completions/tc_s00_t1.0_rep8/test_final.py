

import pytest
from nds_script import correct_asserts_indent


def test_correct_indent_single_line():
    input_code = "assert True"
    expected = "assert True"
    assert correct_asserts_indent(input_code) == expected

def test_correct_indent_multi_line():
    input_code = "def test_func():\n    assert True\n    assert False"
    expected = "def test_func():\n        assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected

def test_correct_indent_with_empty_lines():
    input_code = "def test_func():\n\n    assert True\n\n    assert False\n"
    expected = "def test_func():\n        assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected

def test_correct_indent_no_indent_needed():
    input_code = "def test_func():\n        assert True\n        assert False"
    expected = "def test_func():\n        assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected

def test_input_non_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_list_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(["assert True", "assert False"])

def test_input_none_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_input_empty_string():
    input_code = ""
    expected = ""
    assert correct_asserts_indent(input_code) == expected

def test_input_whitespace_only_string():
    input_code = "    "
    expected = ""
    assert correct_asserts_indent(input_code) == expected

def test_indent_inside_block():
    input_code = "if condition:\n    assert x == 1\n    assert y == 2"
    expected = "if condition:\n        assert x == 1\n        assert y == 2"
    assert correct_asserts_indent(input_code) == expected

def test_correct_indent_with_tabs():
    input_code = "def test_func():\n\tassert True\n\tassert False"
    expected = "def test_func():\n        assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected

def test_correct_indent_with_mixed_whitespace():
    input_code = "def test_func():\n  \t  assert True\n    \tassert False"
    expected = "def test_func():\n        assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected

def test_input_exact_type_error_message():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(123)

