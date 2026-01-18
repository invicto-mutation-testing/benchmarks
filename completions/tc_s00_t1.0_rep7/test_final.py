

import pytest
from nds_script import correct_asserts_indent


def test_correct_asserts_indent_normal_input():
    code = "def foo():\n  assert 1 == 1\n  assert 2 == 2"
    expected = "def foo():\n        assert 1 == 1\n        assert 2 == 2"
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_with_spaces():
    code = " def foo():\n\n  assert 1 == 1\n  assert 2 == 2 \n"
    expected = "def foo():\n        assert 1 == 1\n        assert 2 == 2"
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_single_line():
    code = "def foo():"
    expected = "def foo():"
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_empty_input():
    code = ""
    expected = ""
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_input_not_string():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_correct_asserts_indent_input_int():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_correct_asserts_indent_input_list():
    with pytest.raises(TypeError):
        correct_asserts_indent(["def foo():", "  assert True"])

def test_correct_asserts_indent_input_dict():
    with pytest.raises(TypeError):
        correct_asserts_indent({"code": "def foo():\n  assert True"})

# def test_correct_asserts_indent_type_error_message():
#     with pytest.raises(TypeError, match="Input must be a string"):
#         correct_asserts_indent(None)



def test_correct_asserts_indent_single_character_line():
    code = "def foo():\n a\n  assert True"
    expected = "def foo():\n        a\n        assert True"
    assert correct_asserts_indent(code) == expected

