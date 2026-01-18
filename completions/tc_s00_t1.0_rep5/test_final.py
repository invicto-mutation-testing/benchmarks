

import pytest
from nds_script import correct_asserts_indent


def test_correct_asserts_indent_basic_indentation():
    input_code = (
        "def test_function():\n"
        "assert True\n"
        "assert False"
    )
    expected_output = (
        "def test_function():\n"
        "        assert True\n"
        "        assert False"
    )
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_empty_line():
    input_code = (
        "def test_function():\n"
        "assert True\n"
        "\n"
        "assert False"
    )
    expected_output = (
        "def test_function():\n"
        "        assert True\n"
        "        assert False"
    )
    assert correct_asserts_indent(input_code) == expected_output

# def test_correct_asserts_indent_with_comments():
#     input_code = (
#         "def test_function():\n"
#         "# This is a test\n"
#         "    assert True\n"
#         "    # Another comment\n"
#         "assert False"
#     )
#     expected_output = (
#         "def test_function():\n"
#         "        assert True\n"
#         "        assert False"
#     )
#     assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_mixed_indentation():
    input_code = (
        "def test_function():\n"
        "    assert True\n"
        "        assert False\n"
        " assert None"
    )
    expected_output = (
        "def test_function():\n"
        "        assert True\n"
        "        assert False\n"
        "        assert None"
    )
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_no_indents_needed():
    input_code = (
        "def test_function():\n"
        "    assert True\n"
        "    assert False"
    )
    expected_output = (
        "def test_function():\n"
        "        assert True\n"
        "        assert False"
    )
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_input_not_string():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_correct_asserts_indent_input_integer():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_correct_asserts_indent_input_list():
    with pytest.raises(TypeError):
        correct_asserts_indent(["assert True", "assert False"])

def test_correct_asserts_indent_input_dict():
    with pytest.raises(TypeError):
        correct_asserts_indent({"code": "assert True\nassert False"})

def test_correct_asserts_indent_invalid_string_error_message():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(123)



def test_correct_asserts_indent_single_char_line():
    input_code = (
        "def test_function():\n"
        "x\n"
        "assert True"
    )
    expected_output = (
        "def test_function():\n"
        "        x\n"
        "        assert True"
    )
    assert correct_asserts_indent(input_code) == expected_output

