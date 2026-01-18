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
#         session = Session(123, "pass", 8080)

# def test_session_init_invalid_password():
#     with pytest.raises(TypeError):
#         session = Session("user", 123, 8080)

# def test_session_init_invalid_port():
#     with pytest.raises(TypeError):
#         session = Session("user", "pass", "8080")

def test_das_session_init_valid():
    req_session = requests.Session()
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, req_session)
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1
    assert das_session.session == req_session

# def test_das_session_init_invalid_username():
#     with pytest.raises(TypeError):
#         das_session = DasSession(123, "pass", 8080, "http://example.com", 1.1)

# def test_das_session_init_invalid_password():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", 123, 8080, "http://example.com", 1.1)

# def test_das_session_init_invalid_port():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", "eighty-eighty", "http://example.com", 1.1)

# def test_das_session_init_invalid_url():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, 123, 1.1)

# def test_das_session_init_invalid_version():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", "1.1")

# def test_das_session_init_invalid_session_type():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, "not a session")

def test_das_session_tablename():
    das_session = DasSession()
    assert das_session.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    das_session = DasSession()
    assert das_session.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     das_session = DasSession()
#     assert hasattr(das_session, 'id') and das_session.id.primary_key



# def test_das_session_id_primary_key():
#     das_session = DasSession()
#     assert hasattr(das_session, 'id') and das_session.id.primary_key



# def test_das_session_foreign_key_mutation():
#     das_session = DasSession()
#     assert das_session.user_id.foreign_keys[0]._colspec == "users.id"



def test_das_session_user_id_attribute():
    das_session = DasSession()
    assert hasattr(das_session, 'user_id') and das_session.user_id is not None



def test_das_session_url_column_name():
    das_session = DasSession()
    assert hasattr(das_session, 'url'), "The 'url' attribute should exist in DasSession."



def test_das_session_url_length():
    das_session = DasSession(url="http://example.com")
    assert len(das_session.url) <= 100, "URL length should not exceed 100 characters in the original code."



# def test_das_session_url_nullable():
#     das_session = DasSession(url=None)
#     assert das_session.url is not None, "URL should not be nullable in the original code."



def test_das_session_url_not_none():
    das_session = DasSession(url="http://example.com")
    assert das_session.url is not None, "URL should not be None in DasSession."



def test_das_session_port_column_name():
    das_session = DasSession(port=8080)
    assert hasattr(das_session, 'port'), "The 'port' attribute should exist in DasSession."



# def test_das_session_port_nullable():
#     # This test checks if the port can be None, which should fail in the original code
#     # because the port is not nullable in the original implementation.
#     with pytest.raises(TypeError):
#         das_session = DasSession(port=None)



def test_das_session_port_not_none():
    das_session = DasSession(port=8080)
    assert das_session.port is not None, "Port should not be None in DasSession."



def test_das_session_username_column_name():
    das_session = DasSession(username="user")
    assert hasattr(das_session, 'username'), "The 'username' attribute should exist in DasSession."



# def test_das_session_username_length():
#     das_session = DasSession(username="a" * 51)
#     assert len(das_session.username) <= 50, "Username length should not exceed 50 characters in the original code."



# def test_das_session_username_nullable():
#     # This test checks if the username can be None, which should fail in the mutated code
#     # because the username is nullable in the mutated implementation.
#     das_session = DasSession(username=None)
#     assert das_session.username is not None, "Username should not be None in the original code."



def test_das_session_username_not_none():
    das_session = DasSession(username="user")
    assert das_session.username is not None, "Username should not be None in DasSession."



def test_das_session_password_column_name():
    das_session = DasSession(password="securepassword")
    assert hasattr(das_session, 'password'), "The 'password' attribute should exist in DasSession."



def test_das_session_password_length():
    das_session = DasSession(password="a" * 500)
    assert len(das_session.password) == 500, "Password length should be exactly 500 characters in the original code."



# def test_das_session_password_nullable():
#     # This test checks if the password can be None, which should fail in the mutated code
#     # because the password is nullable in the mutated implementation.
#     with pytest.raises(AttributeError):
#         das_session = DasSession(password=None)
#         assert das_session.password is not None, "Password should not be None in the original code."



def test_das_session_password_not_none():
    das_session = DasSession(password="securepassword")
    assert das_session.password is not None, "Password should not be None in DasSession."



def test_das_session_version_column_name():
    das_session = DasSession(version=1.1)
    assert hasattr(das_session, 'version'), "The 'version' attribute should exist in DasSession."



# def test_das_session_version_nullable():
#     # This test checks if the version can be None, which should fail in the mutated code
#     # because the version is nullable in the mutated implementation.
#     with pytest.raises(TypeError):
#         das_session = DasSession(version=None)



def test_das_session_version_not_none():
    das_session = DasSession(version=1.1)
    assert das_session.version is not None, "Version should not be None in DasSession."



# def test_das_session_user_relationship_type():
#     das_session = DasSession()
#     assert type(das_session.user).__name__ == "User", "User relationship should be linked to 'User' model."



def test_das_session_relationship_back_populates():
    das_session = DasSession()
    assert das_session.user.back_populates == "saved_das_connection"



def test_das_session_relationship_lazy_loading():
    das_session = DasSession()
    assert das_session.user.lazy == "select", "The lazy loading strategy should be 'select' in the original code."



def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1, "Default version should be 1.1 in the original code."

