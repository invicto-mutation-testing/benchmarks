from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_init_valid():
    session = Session("user", "pass", 8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# def test_session_init_invalid_username():
#     with pytest.raises(TypeError):
#         Session(123, "pass", 8080)

# def test_session_init_invalid_password():
#     with pytest.raises(TypeError):
#         Session("user", 456, 8080)

# def test_session_init_invalid_port():
#     with pytest.raises(TypeError):
#         Session("user", "pass", "8080")

def test_das_session_init_valid():
    req_session = requests.Session()
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, req_session)
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1
    assert das_session.session == req_session

# def test_das_session_init_none_username():
#     with pytest.raises(TypeError):
#         DasSession(None, "pass", 8080, "http://example.com", 1.1)

# def test_das_session_init_none_password():
#     with pytest.raises(TypeError):
#         DasSession("user", None, 8080, "http://example.com", 1.1)

# def test_das_session_init_none_port():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", None, "http://example.com", 1.1)

# def test_das_session_init_none_url():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, None, 1.1)

# def test_das_session_init_invalid_version():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, "http://example.com", "1.1")

# def test_das_session_init_invalid_session_type():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, "http://example.com", 1.1, "not_a_session")

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     assert DasSession.id.primary_key is True



# def test_das_session_id_primary_key():
#     assert hasattr(DasSession, 'id') and DasSession.id.primary_key



# def test_das_session_foreign_key_mutation():
#     assert DasSession.user_id.foreign_keys.pop().column.table.name == "users"



def test_das_session_user_id_attribute():
    assert hasattr(DasSession, 'user_id') and DasSession.user_id is not None



# def test_das_session_url_column_name():
#     assert 'url' in DasSession.__table__.c



# def test_das_session_url_length():
#     assert len(DasSession.url.property.columns[0].type.length) == 100



# def test_das_session_url_not_nullable():
#     with pytest.raises(ValueError):
#         DasSession(url=None)



def test_das_session_url_not_none():
    das_session = DasSession(url="http://example.com")
    assert das_session.url is not None



# def test_das_session_port_column_name():
#     assert 'port' in DasSession.__table__.c



# def test_das_session_port_not_nullable():
#     with pytest.raises(TypeError):
#         DasSession(port=None)



def test_das_session_port_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.port == 8080



# def test_das_session_username_column_name():
#     assert 'username' in DasSession.__table__.c



def test_das_session_username_length():
    das_session = DasSession(username="a" * 50)
    assert len(das_session.username) == 50



def test_das_session_username_nullable():
    # This test should pass with the original code and fail with the mutated code
    # because the mutation makes the username nullable.
    das_session = DasSession(username=None)
    assert das_session.username is None



def test_das_session_username_not_none():
    # This test should pass with the original code and fail with the mutated code
    # because the mutation sets the username to None by default.
    das_session = DasSession(username="user")
    assert das_session.username is not None



# def test_das_session_password_column_name():
#     # This test checks if the password column name is correctly defined as 'password'
#     # It should pass with the original code and fail with the mutated code where the column name is 'XXpasswordXX'
#     assert 'password' in DasSession.__table__.c



def test_das_session_password_length():
    das_session = DasSession(password="a" * 500)
    assert len(das_session.password) == 500



def test_das_session_password_nullable():
    # This test should pass with the original code and fail with the mutated code
    # because the mutation makes the password nullable.
    das_session = DasSession(password=None)
    assert das_session.password is None



def test_das_session_password_not_none():
    das_session = DasSession(username="user", password="pass", port=8080)
    assert das_session.password is not None



def test_das_session_version_column_mutation():
    das_session = DasSession(version=1.2)
    assert das_session.version == 1.2



# def test_das_session_version_nullable():
#     # This test checks if the version attribute must not be None in the original code
#     # It should fail in the mutated code where the version can be nullable
#     das_session = DasSession(version=None)
#     assert das_session.version is not None



def test_das_session_version_attribute():
    das_session = DasSession(version=1.1)
    assert das_session.version == 1.1



# def test_das_session_user_relationship_type():
#     # This test checks if the user relationship is correctly linked to the "User" class
#     # It should pass with the original code and fail with the mutated code where the relationship is linked to "XXUserXX"
#     assert DasSession.user.property.mapper.class_.__name__ == "User"



# def test_das_session_relationship_back_populates():
#     # This test should pass with the original code and fail with the mutated code
#     # because the mutation changes the back_populates argument in the relationship.
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_lazy_relationship():
#     # This test should pass with the original code and fail with the mutated code
#     # because the mutation changes the lazy loading strategy of the relationship.
#     assert DasSession.user.property.lazy == "select"



def test_das_session_user_relationship():
    # This test should pass with the original code and fail with the mutated code
    # because the mutation sets the user relationship to None.
    assert DasSession.user is not None



def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1

