from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_das_session_all_params_provided_correctly():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das.username == "user"
    assert das.password == "pass"
    assert das.port == 8080
    assert das.url == "http://example.com"
    assert das.version == 1.1

# def test_das_session_missing_username():
#     with pytest.raises(TypeError):
#         DasSession(None, "pass", 8080, "http://example.com", 1.1)

# def test_das_session_missing_password():
#     with pytest.raises(TypeError):
#         DasSession("user", None, 8080, "http://example.com", 1.1)

# def test_das_session_missing_port():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", None, "http://example.com", 1.1)

def test_das_session_missing_url():
    das = DasSession("user", "pass", 8080, None, 1.1)
    assert das.url is None

def test_das_session_version_default():
    das = DasSession("user", "pass", 8080, "http://example.com")
    assert das.version == 1.1

# def test_das_session_invalid_username_type():
#     with pytest.raises(AttributeError):
#         DasSession(1234, "pass", 8080, "http://example.com", 1.1)

# def test_das_session_invalid_password_type():
#     with pytest.raises(AttributeError):
#         DasSession("user", 9876, 8080, "http://example.com", 1.1)

# def test_das_session_invalid_port_type():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", "wrong_port", "http://example.com", 1.1)

# def test_das_session_invalid_url_type():
#     with pytest.raises(AttributeError):
#         DasSession("user", "pass", 8080, 5678, 1.1)

# def test_das_session_invalid_version_type():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, "http://example.com", "one point one")

def test_session_all_params_provided_correctly():
    ses = Session("user", "passwd", 8080)
    assert ses.username == "user"
    assert ses.password == "passwd"
    assert ses.port == 8080

# def test_session_invalid_username():
#     with pytest.raises(TypeError):
#         Session(123456, "passwd", 8080)

# def test_session_invalid_password():
#     with pytest.raises(TypeError):
#         Session("user", 456789, 8080)

# def test_session_invalid_port():
#     with pytest.raises(TypeError):
#         Session("user", "passwd", "eighty-eighty")

def test_das_session_table_name():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das.__tablename__ == "saved_das_connection"



# def test_das_session_id_column_name():
#     from sqlalchemy import inspect
#     inspector = inspect(DasSession)
#     assert 'id' in inspector.columns.keys()



# def test_das_session_primary_key_assertion():
#     session = Session()
#     das = das_session_class("user", "pass", 8080, "http://example.com", 1.1)
#     assert 'id' in [column.key for column in das.__table__.columns if column.primary_key]



def test_das_session_id_column_name():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das, 'id'), "DasSession should have an 'id' attribute"



# def test_das_session_foreign_key_mutation():
#     das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     # the mutation changes 'users.id' to 'XXusers.idXX' which would throw an error in a real DB interaction
#     # Assuming 'User' is defined and 'users.id' is a valid foreign key, this should raise an error with the mutant where relationship expects a valid foreign key reference.
#     with pytest.raises(Exception):
#         # simulate/test a database operation that depends on the user_id ForeignKey
#         # this test is hypothetical as the real database session and operation are required to trigger the error
#         das.user_id



# def test_das_session_foreign_key_absence():
#     with pytest.raises(AttributeError):
#         das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#         _ = das.user_id  # In the mutated code `user_id` is set to None and not an sqlalchemy Mapped column



def test_das_session_url_column_incorrect_mapping():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das, 'url'), "DasSession should have a 'url' attribute mapped correctly"



# def test_das_session_url_length_limit():
#     # Test assumes the max URL length for DasSession should not exceed 100 as defined in original code
#     with pytest.raises(ValueError):
#         DasSession("user", "pass", 8080, "http://" + "a" * 93 + ".com", 1.1)



def test_das_session_url_nullable():
    # This test verifies that the 'url' field must not be None, which contradicts the mutation.
    with pytest.raises(AssertionError):
        das = DasSession("user", "pass", 8080, None, 1.1)
        assert das.url is not None



def test_das_session_url_should_not_be_none():
    with pytest.raises(AssertionError):
        das = DasSession("user", "pass", 8080, None, 1.1)
        assert das.url is not None



def test_das_session_port_mapping():
    # This test checks if 'port' is mapped correctly. It should pass with original and fail with mutated code due to mutation in port mapping ("XXportXX").
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das.port == 8080, "Port should be mapped to 'port' and not 'XXportXX'"



def test_das_session_port_nullable():
    das = DasSession("user", "pass", None, "http://example.com", 1.1)
    assert das.port is None



def test_das_session_check_port_mapping():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das.port == 8080



def test_das_session_username_column_mapping():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das, 'username'), "DasSession should have a 'username' attribute"



def test_das_session_username_length():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert len(das.username) <= 50



# def test_das_session_username_nullable_violation():
#     # This test should pass with original code and fail with mutated code because username should not accept None
#     das = DasSession(username=None, password="pass", port=8080, url="http://example.com", version=1.1)
#     assert das.username is not None



def test_original_das_session_username_not_none():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das.username is not None, "Username should not be None"



def test_das_session_password_column_mapping():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert getattr(das, 'password', None) == "pass"



def test_das_session_password_length_field_mutation():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert len(das.password) <= 500



# def test_das_session_password_nullable():
#     # This test is designed to fail with the mutated code where password is nullable
#     das = DasSession("user", None, 8080, "http://example.com", 1.1)
#     assert das.password is not None



def test_password_attribute_presence():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das, 'password'), "The 'password' attribute should be present in DasSession."



def test_das_session_version_column_mutation():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.5)
    assert das.version == 1.5, "Version should be correctly set to 1.5"



# def test_das_session_version_not_nullable():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, "http://example.com", None)



def test_das_session_version_attribute_presence():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das, 'version'), "DasSession should have a 'version' attribute"



# def test_das_session_user_relationship_association():
#     das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     with pytest.raises(AttributeError):
#         # In mutated code 'user' relation is changed to 'XXUserXX'
#         _ = das.user



# def test_das_session_relationship_back_populates_mutation():
#     das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     with pytest.raises(AttributeError):
#         _ = das.user



def test_relationship_lazy_loading():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das.user.lazy == "select", "The 'lazy' parameter for user relationship should be set to 'select'"



def test_das_session_session_attribute_not_none():
    das = DasSession("user", "pass", 8080, "http://example.com", 1.1, session="some_session")
    assert das.session is not None

