import pytest
from put import correct_asserts_indent

@pytest.fixture
def correct_indentation_setup_correct():
    """Setup fixture to provide initial inputs and their expected correct outputs."""
    return [
        ("", ""),
        ("assert True", "        assert True"),  # Single line, needs correct indentation
        ("\n\nassert True", "        assert True"),  # Preceding whitespaces and newlines
        ("  \n \n assert True", "        assert True")  # Complex case of mixed spaces and newlines
    ]

@pytest.mark.parametrize("input_value, expected_result", [
    (123, TypeError),  # Non-string: integer
    (56.78, TypeError),  # Non-string: float
    ([], TypeError),  # Non-string: list
    ({}, TypeError),  # Non-string: dictionary
    (None, TypeError)  # Non-string: NoneType
])
def test_correct_asserts_indent_with_invalid_types(input_value, expected_result):
    """Test correct_asserts_indent with non-string inputs, expecting a TypeError."""
    with pytest.raises(expected_result):
        correct_asserts_indent(input_value)

def test_empty_string():
    """Test correct_asserts_indent with an empty string. Should return an empty string."""
    assert correct_asserts_indent("") == ""

def test_string_type_error_message():
    """Test correct_asserts_indent with non-string input to confirm correct exception message."""
    with pytest.raises(TypeError) as exc_info:
        correct_asserts_indent(100)
    assert str(exc_info.value) == "Input must be a string"

def test_special_split_mutation_case():
    """This test will pass if the split is done by '\n' and fail if a different delimiter like 'XX\nXX' is used."""
    test_input = "assert True\nassert False"
    expected_normal = "assert True\n        assert False"
    actual_output = correct_asserts_indent(test_input)
    assert actual_output == expected_normal, f"Output was: {actual_output}"

# New test specifically to detect mutation by testing length condition change
def test_single_character_line_indentation():
    """Test case with a single character on the line beneath the first which should be indented."""
    test_input = "assert True\nx"
    expected_output = "assert True\n        x"
    output = correct_asserts_indent(test_input)
    assert output == expected_output, "Single character line should still be indented; Output was: {}".format(output)