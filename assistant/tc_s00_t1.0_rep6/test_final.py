import pytest
from put import correct_asserts_indent

# Original test cases.
def test_correct_asserts_indent_normal_input():
    code = "assert True\nassert False\nassert x == y"
    expected = "assert True\n        assert False\n        assert x == y"
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_empty_string():
    assert correct_asserts_indent("") == ""

def test_correct_asserts_indent_no_inner_content():
    code = "assert True"
    expected = "assert True"
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_multiple_lines():
    code = "assert True\n\n\nassert False"
    expected = "assert True\n        assert False"
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_whitespace_input():
    code = "   assert True   \n   assert False   "
    expected = "assert True\n        assert" + " False"
    assert correct_asserts_indent(code) == expected

@pytest.mark.parametrize("invalid_input", [123, None, 3.14, [], {}, lambda x: x])
def test_correct_asserts_indent_non_string_input(invalid_input):
    with pytest.raises(TypeError):
        correct_asserts_indent(invalid_input)

def test_correct_asserts_indent_strip_unnecessary_newlines():
    code = "assert True\n\n\n\nassert False\n\n"
    expected = "assert True\n        assert False"
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_type_error_message():
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(123)
    assert str(exc_info.value) == "Input must be a string"

# New test cases to catch the specific mutation in the mutant code.
def test_correct_asserts_indent_single_char_line():
    code = "assert True\na\nassert False"
    expected = "assert True\n        a\n        assert False"
    # Original code: passes as it does not change single 'a' line indentation
    # Mutant code: fails because it loses 'a' line due to `if len(l) > 1` condition in the mutant
    assert correct_asserts_indent(code) == expected

def test_correct_asserts_indent_two_char_line():
    code = "assert True\nab\nassert False"
    expected = "assert True\n        ab\n        assert False"
    # Original code: sees 'ab' and indents it
    # Mutant code: the same as original in this case, but keeps consistency in designing test coverage
    assert correct_asserts_indent(code) == expected