import pytest
from put import correct_asserts_indent

# Original and corrected test cases
@pytest.mark.parametrize("invalid_input", [123, 4.56, None, [], {}, (1, 2)])
def test_invalid_type_inputs(invalid_input):
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(invalid_input)

def test_correct_single_line_input():
    code = "assert True"
    expected = "assert True"
    assert correct_asserts_indent(code) == expected, "Failed to handle single line input correctly."

def test_correct_multiline_input():
    code = "assert True\n    assert False\nassert None"
    expected = "assert True\n        assert False\n        assert None"
    assert correct_asserts_indent(code) == expected, "Failed to handle multi-line input correctly."

def test_input_with_empty_lines():
    code = "assert True\n\n    assert False\n\nassert None"
    expected = "assert True\n        assert False\n        assert None"
    assert correct_asserts_indent(code) == expected, "Failed to handle input with empty lines correctly."

def test_empty_string():
    code = ""
    expected = ""
    assert correct_asserts_indent(code) == expected, "Failed to handle empty string input correctly."

def test_string_with_only_new_lines():
    code = "\n\n\n"
    expected = ""
    assert correct_asserts_indent(code) == expected, "String with only new lines should return empty string."

def test_correct_indentation_already_present():
    code = "assert True\n        assert False\n        assert None"
    expected = "assert True\n        assert False\n        assert None"
    assert correct_asserts_indent(code) == expected, "Failed to handle inputs with correct indentation already present."

def test_strip_trailing_whitespace():
    code = "assert True \n    assert False \n    assert None "
    expected = "assert True\n        assert False\n        assert None"
    assert correct_asserts_indent(code) == expected, "Failed to strip trailing whitespace correctly."

def test_mixed_indentation_styles():
    code = "assert True\n\tassert False\n  assert None"
    expected = "assert True\n        assert False\n        assert None"
    assert correct_asserts_indent(code) == expected, "Failed to normalize mixed indentation styles correctly."

# Additional test to check mutation where mutated code does not indent single character lines correctly
def test_single_character_line_input():
    code = "a\nb\nc"
    expected = "a\n        b\n        c"
    assert correct_asserts_indent(code) == expected, "Failed to properly indent single character lines."