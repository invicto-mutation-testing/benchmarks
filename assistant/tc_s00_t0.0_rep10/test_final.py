import pytest
from put import correct_asserts_indent

def test_correct_asserts_indent_with_valid_input():
    input_code = "assert True\nassert False"
    expected_output = "assert True\n        assert False"
    assert correct_asserts_indent(input_code) == expected_output

    input_code = "  assert x == 1\n\nassert y == 2  "
    expected_output = "assert x == 1\n        assert y == 2"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_empty_string():
    input_code = ""
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_no_asserts():
    input_code = "x = 1\ny = 2"
    expected_output = "x = 1\n        y = 2"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_asserts_indent_with_single_line():
    input_code = "assert x == 1"
    expected_output = "assert x == 1"
    assert correct_asserts_indent(input_code) == expected_output

@pytest.mark.parametrize("input_code", [
    123,  # integer
    12.34,  # float
    None,  # NoneType
    [],  # list
    {},  # dictionary
    ()   # tuple
])
def test_correct_asserts_indent_with_invalid_types(input_code):
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(input_code)
    assert str(exc_info.value) == "Input must be a string"

def test_correct_asserts_indent_with_multiline_string():
    input_code = """
    assert x == 1
    x = 2
    assert y != 3
    """
    expected_output = "assert x == 1\n        x = 2\n        assert y != 3"
    assert correct_asserts_indent(input_code) == expected_output

# New test case to catch the mutation
def test_correct_asserts_indent_with_single_character_line():
    # This test will pass with the original code but fail with the mutated code
    # because the mutated code ignores lines with exactly one character after stripping.
    input_code = "a\nb\nassert c"
    expected_output = "a\n        b\n        assert c"
    assert correct_asserts_indent(input_code) == expected_output