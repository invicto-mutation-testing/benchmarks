import pytest
from put import correct_asserts_indent

def test_correct_asserts_indent_with_valid_input():
    input_code = "assert True\nassert False"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

    input_code = "  assert True\n    assert False\nassert None"
    expected_output = "assert True\n        assert False\n        assert None"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_empty_string():
    input_code = ""
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_whitespace_input():
    input_code = "   \n\t  \n "
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_no_asserts():
    input_code = "print('Hello, world!')"
    expected_output = "print('Hello, world!')"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_non_string_input():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)
    with pytest.raises(TypeError):
        correct_asserts_indent(None)
    with pytest.raises(TypeError):
        correct_asserts_indent([1, 2, 3])

def test_correct_asserts_indent_with_mixed_content():
    input_code = "print('Start')\nassert True\nprint('End')\nassert False"
    expected_output = "print('Start')\n        assert True\n        print('End')\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_error_message():
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(123)
    assert str(exc_info.value) == "Input must be a string"

# New test case to catch the mutation in the mutant code
def test_correct_asserts_indent_single_character_line():
    input_code = "a\nassert True"
    expected_output = "a\n        assert True"
    assert correct_asserts_indent(input_code) == expected_output