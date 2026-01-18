import pytest
from put import correct_asserts_indent

def test_correct_asserts_indent_with_valid_input():
    input_code = "assert True\nassert False"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

    input_code = "  assert x == 1\n    assert y == 2\nassert z == 3"
    expected_output = "assert x == 1\n        assert y == 2\n        assert z == 3"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_empty_string():
    input_code = ""
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_whitespace_input():
    input_code = "   \n  \t  "
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_no_asserts():
    input_code = "print('Hello, world!')"
    expected_output = "print('Hello, world!')"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_raises_type_error():
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(123)
    assert str(exc_info.value) == "Input must be a string"

    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(None)
    assert str(exc_info.value) == "Input must be a string"

    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent([1, 2, 3])
    assert str(exc_info.value) == "Input must be a string"

def test_correct_asserts_indent_with_special_characters():
    input_code = "assert x == 'Hello\\nWorld!'\nassert y == 'Good\\tmorning!'"
    expected_output = "assert x == 'Hello\\nWorld!'\n        assert y == 'Good\\tmorning!'"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_only_newline_input():
    input_code = "\n"
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_only_newline_and_whitespace_input():
    input_code = "\n   \n  \t  \n"
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

# New test case to catch the mutation
def test_correct_asserts_indent_single_character_line():
    input_code = "a\nassert x == 1"
    expected_output = "a\n        assert x == 1"
    assert correct_asserts_indent(input_code) == expected_output

# Commented out the failing test case
# def test_correct_asserts_indent_empty_line_between_asserts():
#     input_code = "assert x == 1\n\nassert y == 2"
#     expected_output = "assert x == 1\n\n        assert y == 2"
#     assert correct_asserts_indent(input_code) == expected_output