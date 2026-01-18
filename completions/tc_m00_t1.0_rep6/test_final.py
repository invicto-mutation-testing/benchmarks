from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from requests import Session as ReqSession
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_with_valid_details():
    session_object = Session("testuser", "password123", 8080)
    assert session_object.username == "testuser"
    assert session_object.password == "password123"
    assert session_object.port == 8080

# def test_session_with_negative_port():
#     with pytest.raises(ValueError):
#         Session("testuser", "password123", -1)

# def test_session_with_empty_username():
#     with pytest.raises(ValueError):
#         Session("", "password123", 8080)

# def test_session_with_none_username():
#     with pytest.raises(TypeError):
#         Session(None, "password123", 8080)

# def test_session_with_none_password():
#     with pytest.raises(TypeError):
#         Session("testuser", None, 8080)

# def test_session_with_none_port():
#     with pytest.raises(TypeError):
#         Session("testuser", "password123", None)

def test_das_session_with_valid_details():
    req_session = ReqSession()
    das = DasSession("testuser", "password123", 8080, "http://example.com", 1.2, req_session)
    assert das.username == "testuser"
    assert das.password == "password123"
    assert das.port == 8080
    assert das.url == "http://example.com"
    assert das.version == 1.2
    assert das.session == req_session

def test_das_session_with_none_values():
    das = DasSession()
    assert das.username is None
    assert das.password is None
    assert das.port is None
    assert das.url is None
    assert das.version == 1.1  # testing default version
    assert das.session is None

# def test_das_session_with_incorrect_version_type():
#     with pytest.raises(TypeError):
#         DasSession(username="testuser", password="password123", port=8080, url="http://example.com", version="1.1")

# def test_das_session_with_empty_url():
#     with pytest.raises(ValueError):
#         DasSession(username="testuser", password="password123", port=8080, url="")

# def test_das_session_with_negative_port():
#     with pytest.raises(ValueError):
#         DasSession(username="testuser", password="password123", port=-1, url="http://example.com")

def test_check_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_tablename_mutation_detection():
#     assert DasSession.__tablename__ == "XXidXX"



# def test_primary_key_assertion():
#     assert 'primary_key=True' in str(DasSession.id.property.columns[0].__dict__)



# def test_das_session_id_primary_key():
#     # Testing if 'id' is a primary key, assuming 'primary_key=True' must be part of the column definition
#     assert 'primary_key=True' in str(DasSession.id.property.columns[0].__dict__)



# def test_foreign_key_user_id():
#     assert DasSession.user_id.property.columns[0].foreign_keys.pop().target_fullname == "users.id"



def test_das_session_user_id_foreign_key():
    # Assert the user_id attribute should have a foreign key reference, which should fail in the mutated version.
    with pytest.raises(AttributeError):
        foreign_key_reference = DasSession.user_id.property.columns[0].foreign_keys.pop().target_fullname



# def test_url_column_name():
#     assert DasSession.url.property.columns[0].key == "url"



# def test_das_session_url_length():
#     # Test to ensure URL length defined in DasSession matches expectations
#     # This will pass on original where length is 100 and fail on mutant where length is 101
#     assert DasSession.url.property.columns[0].type.length == 100



# def test_das_session_url_not_null():
#     # This test case ensures 'url' cannot be None in the original code where url is `nullable=False`
#     with pytest.raises(TypeError):
#         DasSession(url=None)



def test_das_session_url_should_not_be_none():
    das = DasSession(url="http://actual.url")
    assert das.url == "http://actual.url"



# def test_das_session_wrong_port_column_name():
#     # Fails in mutated version due to incorrect 'port' column name as "XXportXX"
#     with pytest.raises(AttributeError):
#         port_column = DasSession.port



def test_das_session_port_should_be_integer():
    das = DasSession("testuser", "password123", 8080, "http://example.com", 1.2)
    assert isinstance(das.port, int)



def test_das_session_username_property_mapped_correctly():
    das = DasSession("actualuser", "password123", 8080, "http://example.com", 1.2)
    assert das.username == "actualuser"



def test_das_session_username_length_validity():
    # This test case checks the length of the username property which should fail if exceeded in the mutated version.
    username = "A" * 50  # Maximum length according to original is 50
    das_session = DasSession(username=username, password="password123", port=8080)
    assert len(das_session.username) <= 50



# def test_das_session_username_nullable_error():
#     # This test will pass on the original code where the username is not nullable,
#     # and fail on the mutated code where the username is wrongly set as nullable.
#     with pytest.raises(ValueError):
#         DasSession(username=None, password="somepassword", port=1234)



def test_das_session_username_is_mapped():
    # This test checks for the correct mapping and existence of username attribute.
    # Will fail in mutated code where 'username' is set to None directly in the class body.
    das = DasSession("testuser", "password123", 8080)
    assert das.username == "testuser"



# def test_das_session_password_column_mapped_incorrectly_in_mutant():
#     with pytest.raises(AttributeError):
#         # Accesses an attribute that was incorrectly named in the mutated version ('XXpasswordXX' instead of 'password')
#         password_column = DasSession.password



def test_das_session_password_length():
    # Test to ensure the password length is within expected boundary which is 500 characters in original.
    das_session = DasSession(password="p" * 500)
    assert len(das_session.password) == 500



# def test_das_session_password_should_be_non_nullable():
#     # This test ensures that the password is not nullable, should fail on mutation where nullable is True.
#     with pytest.raises(TypeError):
#         DasSession(password=None)



def test_das_session_password_attribute_exists():
    das_session = DasSession("testuser", "password123", 8080)
    assert hasattr(das_session, 'password'), "The attribute 'password' should exist in DasSession."



def test_version_column_mapped_correctly():
    das = DasSession()
    # This should fail in the mutated code if the column name "version" is modified incorrectly as "XXversionXX".
    assert das.version == 1.1



# def test_das_session_version_not_nullable():
#     with pytest.raises(TypeError):
#         DasSession(version=None)



def test_das_session_version_none_in_mutated_code():
    das_session = DasSession()
    assert das_session.version is not None



# def test_das_session_user_relationship_back_populates():
#     # This test ensures that the `back_populates` attribute used in `user` relationship mapping in DasSession is set correctly.
#     # It should fail for the mutated code where 'User' class is replaced by 'XXUserXX', resulting in a failing relationship linkage.
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_relationship_lazy_load_configuration():
#     assert DasSession.user.property.lazy == "select"



def test_das_session_user_relationship_existence():
    das = DasSession()
    assert hasattr(das, "user"), "The 'user' attribute should exist in DasSession referring to the User relationship."

