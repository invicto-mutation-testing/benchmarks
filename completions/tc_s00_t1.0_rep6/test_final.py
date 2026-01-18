

import pytest
from nds_script import correct_asserts_indent


def test_correct_normal_string():
    input_code = "assert True\nassert False"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_empty_string():
    assert correct_asserts_indent("") == ""

def test_single_line_no_assert():
    assert correct_asserts_indent("print('hello')") == "print('hello')"

def test_multiple_lines_mixed_content():
    input_code = "def test_function():\n  print('hello')\n  assert True"
    expected_output = "def test_function():\n        print('hello')\n        assert True"
    assert correct_asserts_indent(input_code) == expected_output

def test_input_non_string_raises_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_list_raises_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(["assert True", "assert False"])

def test_input_dict_raises_error():
    with pytest.raises(TypeError):
        correct_asserts_indent({"code": "assert True"})

def test_input_blank_spaces():
    input_code = "  \n  assert True \n assert False \n   "
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_input_blank_lines():
    input_code = "\n\nassert True\n\nassert False\n\n"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_incorrect_error_message_for_non_string_input():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(123)



# def test_lines_with_single_character():
#     input_code = "a\nb\nc"
#     expected_output = "a\n        b\n        c"
#     assert correct_asserts_indent(input_code) == expected_output

