

import pytest
from nds_script import correct_asserts_indent


def test_correct_indentation_single_line():
    input_code = "assert True"
    expected_output = "assert True"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_indentation_multiple_lines():
    input_code = "if a == b:\n    assert a == b\n    assert b == a"
    expected_output = "if a == b:\n        assert a == b\n        assert b == a"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_indentation_with_empty_lines():
    input_code = "if a == b:\n    assert a == b\n\n    assert b == a"
    expected_output = "if a == b:\n        assert a == b\n        assert b == a"
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_indentation_with_varied_indentation():
    input_code = "if a == b:\n  assert a == b\n        assert b == a"
    expected_output = "if a == b:\n        assert a == b\n        assert b == a"
    assert correct_asserts_indent(input_code) == expected_output

def test_input_non_string_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(123)

def test_input_boolean_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(True)

def test_input_none_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(None)

def test_input_list_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent(['assert True'])

def test_input_dictionary_raises_type_error():
    with pytest.raises(TypeError):
        correct_asserts_indent({'key': 'assert True'})

def test_correct_indentation_code_is_empty_string():
    input_code = ""
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

def test_correct_indentation_code_is_blank_space():
    input_code = "  "
    expected_output = ""
    assert correct_asserts_indent(input_code) == expected_output

# def test_correct_indentation_multiple_lines_with_initial_empty_lines():
#     input_code = "\n\nif a == b:\n  assert a == b\n        assert b == a"
#     expected_output = "\nif a == b:\n        assert a == b\n        assert b == a"
#     assert correct_asserts_indent(input_code) == expected_output

# def test_type_error_message():
#     with pytest.raises(TypeError) as exc_info:
#         correct_asserts_indent(123)
#     # Now checks specifically for the original message
#     assert str(exc_info.value) == "Input must be a string"



# def test_correct_indentation_edge_case_with_single_char_lines():
#     input_code = "if a == b:\n a\n b\n c"
#     expected_output = "if a == b:\n        a\n        b\n        c"
#     assert correct_asserts_indent(input_code) == expected_output

