import pytest
from put import correct_asserts_indent

def test_correct_indentation_empty_string():
    input_code = ""
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output, "Empty string should return an empty string"

def test_correct_indentation_single_statement():
    input_code = "assert True"
    expected_output = "assert True"
    assert correct_asserts_indent(input_code) == expected_output, "Single-line input should not have the indentation added"

def test_correct_indentation_multiple_statements():
    input_code = """assert True
assert False
assert 1 == 1"""
    expected_output = """assert True
        assert False
        assert 1 == 1"""
    assert correct_asserts_indent(input_code) == expected_output, "Each line after the first should be indented exactly 8 spaces"

def test_correct_indentation_with_initial_spaces():
    input_code = """    assert True
        assert False
    assert 1 == 1"""
    expected_output = """assert True
        assert False
        assert 1 == 1"""
    assert correct_asserts_indent(input_code) == expected_output, "Lines after the first should be indented correctly irrespective of their original spaces"

def test_input_not_a_string():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(123)  # Passing an int

def test_input_string_representation_of_non_string():
    input_code = "123"
    expected_output = "123"
    assert correct_asserts_indent(input_code) == expected_output, "Non-code strings should maintain their original non-indented form as the first line"

@pytest.mark.parametrize("input_code, expected_exception", [
    (123, TypeError),
    (None, TypeError),
    ([1, 2, 3], TypeError),
    (True, TypeError),
])
def test_various_incorrect_input_types(input_code, expected_exception):
    with pytest.raises(expected_exception, match="Input must be a string"):
        correct_asserts_indent(input_code)

def test_typo_in_type_error_message():
    with pytest.raises(TypeError, match="Input must be a string"):
        correct_asserts_indent(123)  # Checking if correct type error message is thrown

# New test cases specifically designed to catch the mutation in the mutant code.

def test_negative_handling():
    """This test is designed to fail for the mutant version where condition `len(l) >= 0` is always true."""
    input_code = "assert True\n\n\nassert False"
    expected_output = """assert True
        assert False"""
    assert correct_asserts_indent(input_code) == expected_output, "Multiple newlines should not result in extra indented blank lines"