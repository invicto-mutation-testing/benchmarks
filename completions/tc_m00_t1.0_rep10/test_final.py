from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_init_valid():
    session = Session("user", "password123", 8080)
    assert session.username == "user"
    assert session.password == "password123"
    assert session.port == 8080

def test_das_session_init_all_none():
    das_session = DasSession()
    assert das_session.username is None
    assert das_session.password is None
    assert das_session.port is None
    assert das_session.url is None
    assert das_session.version == 1.1

def test_das_session_init_valid():
    req_session = requests.Session()
    das_session = DasSession("user", "pass", 8080, "http://example.com", 2.0, req_session)
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 2.0
    assert das_session.session == req_session

# def test_das_session_init_invalid_username():
#     with pytest.raises(TypeError):
#         DasSession(username=123)

# def test_das_session_init_invalid_password():
#     with pytest.raises(TypeError):
#         DasSession(password=123)

# def test_das_session_init_invalid_port():
#     with pytest.raises(TypeError):
#         DasSession(port="eighty")

# def test_das_session_init_invalid_url():
#     with pytest.raises(TypeError):
#         DasSession(url=123)

# def test_das_session_init_invalid_version():
#     with pytest.raises(TypeError):
#         DasSession(version="latest")

# def test_das_session_init_invalid_session():
#     with pytest.raises(TypeError):
#         DasSession(session="not a session object")

def test_session_init_invalid_username():
    with pytest.raises(TypeError):
        Session(username=123)

def test_session_init_invalid_password():
    with pytest.raises(TypeError):
        Session(password=123)

def test_session_init_invalid_port():
    with pytest.raises(TypeError):
        Session(port="eighty")

def test_das_session_table_name():
    das_session = DasSession()
    assert das_session.__tablename__ == "saved_das_connection"



# def test_das_session_column_id_name():
#     assert DasSession.id.key == "id"



# def test_das_session_primary_key():
#     assert DasSession.id.primary_key is True



def test_das_session_column_id_is_none():
    das_session = DasSession()
    assert das_session.id is not None



def test_das_session_foreign_key_typo():
    with pytest.raises(AttributeError):
        DasSession.user_id.property.columns[0].foreign_keys



# def test_das_session_missing_user_id_attr():
#     with pytest.raises(AttributeError):
#         assert DasSession().user_id



# def test_das_session_url_column_name():
#     import sqlalchemy
#     assert isinstance(getattr(DasSession, 'url').property.columns[0], sqlalchemy.Column)



def test_das_session_url_length():
    das_session = DasSession(url="a" * 100)
    assert len(das_session.url) == 100



# def test_das_session_url_should_not_be_none():
#     das_session = DasSession(url=None)
#     assert das_session.url is not None



# def test_das_session_url_none_failure():
#     das_session = DasSession(url=None)
#     assert das_session.url is not None



# def test_das_session_port_mapped_column_name():
#     # This test checks if the 'port' column in DasSession is set with the correct attribute name
#     # Expected to pass on original and fail on mutated code due to a change in the attribute name from 'port' to 'XXportXX'
#     with pytest.raises(AttributeError):
#         assert DasSession.port



def test_das_session_port_nullable_status():
    # This test verifies if the 'port' is not None when initialized properly in DasSession
    das_session = DasSession(port=8080)
    assert das_session.port == 8080



# def test_das_session_port_none_in_mutant_code():
#     das_session = DasSession(port=8080)
#     assert das_session.port is not None



def test_das_session_username_mapped_column_name():
    das_session = DasSession(username="user")
    assert das_session.username == "user"



def test_das_session_username_length():
    das_session = DasSession(username="a" * 50)
    assert len(das_session.username) == 50



# def test_das_session_username_non_nullable():
#     with pytest.raises(AttributeError):
#         # Expect an AttributeError because username should not be set to None in the original code but can be in the mutant
#         DasSession(username=None)



# def test_das_session_username_is_none_in_mutant():
#     das_session = DasSession()
#     assert das_session.username is not None



def test_das_session_password_mapped_column_mutation():
    das_session = DasSession(password="securepassword")
    assert das_session.password == "securepassword"



def test_das_session_password_length():
    # This test checks if the length of a password exactly at the mutated limit fails
    # Expected to pass in original and fail in mutated because the original length is 500 and mutated is 501
    das_session = DasSession(password="a" * 500)
    assert len(das_session.password) == 500



# def test_das_session_password_nullable_validation():
#     with pytest.raises(TypeError):
#         DasSession(password=None)



def test_das_session_password_is_none():
    das_session = DasSession()
    assert das_session.password is None



def test_das_session_version_column_name():
    das_session = DasSession()
    # This test ensures the attribute for storing version is named 'version' not 'XXversionXX'
    # Expect to pass on the original and fail on the mutated where column name is changed
    assert hasattr(das_session, 'version'), "Attribute 'version' should exist"



# def test_das_session_version_nullable():
#     # This test checks the 'version' attribute's nullability in DasSession.
#     # Should pass with the original where version is non-nullable, fail with the mutated where it's nullable.
#     das_session = DasSession()
#     das_session.version = None
#     assert das_session.version is not None



def test_das_session_version_column_existence():
    das_session = DasSession()
    # The test fails in the mutant where version is set to None and hence isn't an attribute of the instance
    assert hasattr(das_session, 'version'), "DasSession should have an attribute 'version'"



# def test_das_session_user_relationship_class_name():
#     assert DasSession.user.property.mapper.class_.__name__ == 'User'



# def test_das_session_user_back_populates_attribute():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_laziness_of_relationship():
#     das_session = DasSession()
#     assert das_session.user.property.lazy == "select"



def test_das_session_user_relationship_is_none():
    das_session = DasSession()
    assert das_session.user is not None, "User relationship should not be None"

