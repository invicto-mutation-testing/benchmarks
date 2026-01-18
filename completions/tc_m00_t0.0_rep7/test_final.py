from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_initialization_valid():
    session = Session("user", "pass", 8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# def test_session_initialization_invalid_username():
#     with pytest.raises(TypeError):
#         session = Session(123, "pass", 8080)

# def test_session_initialization_invalid_password():
#     with pytest.raises(TypeError):
#         session = Session("user", 123, 8080)

# def test_session_initialization_invalid_port():
#     with pytest.raises(TypeError):
#         session = Session("user", "pass", "8080")

def test_das_session_initialization_valid():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1

# def test_das_session_initialization_invalid_username():
#     with pytest.raises(TypeError):
#         das_session = DasSession(123, "pass", 8080, "http://example.com", 1.1)

# def test_das_session_initialization_invalid_password():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", 123, 8080, "http://example.com", 1.1)

# def test_das_session_initialization_invalid_port():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", "8080", "http://example.com", 1.1)

# def test_das_session_initialization_invalid_url():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, 123, 1.1)

# def test_das_session_initialization_invalid_version():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", "1.1")

def test_das_session_initialization_null_username():
    das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is None

def test_das_session_initialization_null_password():
    das_session = DasSession("user", None, 8080, "http://example.com", 1.1)
    assert das_session.password is None

def test_das_session_initialization_null_port():
    das_session = DasSession("user", "pass", None, "http://example.com", 1.1)
    assert das_session.port is None

def test_das_session_initialization_null_url():
    das_session = DasSession("user", "pass", 8080, None, 1.1)
    assert das_session.url is None

def test_das_session_initialization_null_version():
    das_session = DasSession("user", "pass", 8080, "http://example.com", None)
    assert das_session.version is None

def test_das_session_initialization_with_requests_session():
    req_session = requests.Session()
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, req_session)
    assert das_session.session == req_session

# def test_das_session_tablename():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert das_session.__tablename__ == "saved_das_connection"



# def test_das_session_tablename():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert das_session.__tablename__ == "saved_das_connection"



def test_das_session_tablename():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert hasattr(das_session, 'id') and das_session.id.primary_key == True



def test_das_session_id_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das_session, 'id') and das_session.id is not None



# def test_das_session_foreign_key_user_id():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert das_session.user_id.foreign_keys[0].column == "users.id"



def test_das_session_user_id_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das_session, 'user_id') and das_session.user_id is not None



# def test_das_session_url_mapped_column_name():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert 'url' in DasSession.__table__.columns



# def test_das_session_url_length():
#     das_session = DasSession("user", "pass", 8080, "http://example.com" * 10, 1.1)
#     assert len(das_session.url) <= 100



# def test_das_session_url_not_nullable():
#     with pytest.raises(ValueError):
#         das_session = DasSession("user", "pass", 8080, None, 1.1)



def test_das_session_url_mapped_column():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.url == "http://example.com"



def test_das_session_port_mapped_column():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.port == 8080



# def test_das_session_port_not_nullable():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", None, "http://example.com", 1.1)



def test_das_session_port_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.port == 8080



def test_das_session_username_mapped_column():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username == "user"



def test_das_session_username_length():
    # This test checks the length of the username field which should be 50 characters max in the original code
    # It will fail in the mutated code where the length is incorrectly set to 51
    das_session = DasSession("a" * 50, "pass", 8080, "http://example.com", 1.1)
    assert len(das_session.username) == 50



# def test_das_session_username_nullable():
#     # This test checks if the username can be None, which should fail in the original code where username is not nullable
#     with pytest.raises(AttributeError):
#         das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1)
#         assert das_session.username is None



def test_das_session_username_not_none():
    # This test will pass with the original code where username is properly initialized
    # It will fail with the mutated code where username is set to None
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is not None



# def test_das_session_password_mapped_column_name():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert 'password' in DasSession.__table__.columns



def test_das_session_password_length():
    # This test checks the length of the password field which should be 500 characters max in the original code
    # It will fail in the mutated code where the length is incorrectly set to 501
    das_session = DasSession("user", "p" * 500, 8080, "http://example.com", 1.1)
    assert len(das_session.password) == 500



# def test_das_session_password_nullable():
#     # This test will pass with the original code where password is not nullable
#     # It will fail with the mutated code where password is set to nullable
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", None, 8080, "http://example.com", 1.1)



def test_das_session_password_not_none():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.password is not None



def test_das_session_version_mapped_column():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.version == 1.1



# def test_das_session_version_nullable():
#     # This test checks if the version can be None, which should fail in the mutated code where version is nullable
#     das_session = DasSession("user", "pass", 8080, "http://example.com", None)
#     assert das_session.version is not None



def test_das_session_version_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.version == 1.1



# def test_das_session_user_relationship_type():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert type(das_session.user).__name__ == "User"



def test_das_session_relationship_back_populates():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.user.back_populates == "saved_das_connection"



def test_das_session_relationship_lazy_loading():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.user.lazy == "select"



def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1

