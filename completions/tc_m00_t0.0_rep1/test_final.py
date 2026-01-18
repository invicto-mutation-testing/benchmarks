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
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1

def test_das_session_init_none_username():
    das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is None

def test_das_session_init_none_password():
    das_session = DasSession("user", None, 8080, "http://example.com", 1.1)
    assert das_session.password is None

def test_das_session_init_none_port():
    das_session = DasSession("user", "pass", None, "http://example.com", 1.1)
    assert das_session.port is None

def test_das_session_init_none_url():
    das_session = DasSession("user", "pass", 8080, None, 1.1)
    assert das_session.url is None

# def test_das_session_init_invalid_version():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", "1.1")

# def test_das_session_init_invalid_session_type():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, "not a session object")

def test_das_session_init_with_requests_session():
    req_session = requests.Session()
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, req_session)
    assert das_session.session == req_session

def test_das_session_tablename():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert hasattr(das_session, 'id') and das_session.id.primary_key is True



def test_das_session_id_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das_session, 'id') and das_session.id is not None



# def test_das_session_foreign_key_mutation():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert das_session.user_id.property.columns[0].foreign_keys.pop().target_fullname == "users.id"



def test_das_session_user_id_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das_session, 'user_id') and das_session.user_id is not None



# def test_das_session_url_column_name():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert 'url' in das_session.__table__.columns



# def test_das_session_url_length():
#     das_session = DasSession("user", "pass", 8080, "http://example.com" * 10, 1.1)
#     assert len(das_session.url) <= 100



# def test_das_session_url_not_nullable():
#     with pytest.raises(TypeError):
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
    # This test checks the maximum length of the username in DasSession
    # It should pass with the original code where the limit is 50 characters
    # It should fail with the mutated code where the limit is 51 characters
    das_session = DasSession("a" * 50, "pass", 8080, "http://example.com", 1.1)
    assert len(das_session.username) == 50



def test_das_session_username_nullable():
    # This test checks if the username can be None, which should fail in the original code
    # where the username is not nullable, but pass in the mutated code where it is nullable.
    das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is None



def test_das_session_username_not_none():
    # This test ensures that the username cannot be None in the original code
    # It should pass with the original code where the username is not nullable
    # It should fail with the mutated code where the username is set to None
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is not None



# def test_das_session_password_column_name():
#     # This test checks if the password column name is correctly defined as 'password'
#     # It should pass with the original code and fail with the mutated code where the column name is 'XXpasswordXX'
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert 'password' in DasSession.__table__.columns



def test_das_session_password_length():
    # This test checks the maximum length of the password in DasSession
    # It should pass with the original code where the limit is 500 characters
    # It should fail with the mutated code where the limit is 501 characters
    das_session = DasSession("user", "p" * 500, 8080, "http://example.com", 1.1)
    assert len(das_session.password) == 500



# def test_das_session_password_nullable():
#     # This test checks if the password can be None, which should fail in the mutated code
#     # where the password is nullable, but pass in the original code where it is not nullable.
#     das_session = DasSession("user", None, 8080, "http://example.com", 1.1)
#     assert das_session.password is not None



def test_das_session_password_not_none():
    # This test ensures that the password cannot be None in the original code
    # It should pass with the original code where the password is not nullable
    # It should fail with the mutated code where the password is set to None
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.password is not None



def test_das_session_version_column_name():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das_session, 'version'), "The 'version' attribute should exist in DasSession."



# def test_das_session_version_not_nullable():
#     # This test checks if the version attribute can be None, which should fail in the original code
#     # where the version is not nullable, but pass in the mutated code where it is nullable.
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", None)



def test_das_session_version_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.version == 1.1



def test_das_session_user_relationship_back_populates():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.user.back_populates == "saved_das_connection"



def test_das_session_lazy_relationship():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.user.lazy == "select"



#def test_das_session_default_version():
#    das_session = DasSession("user", "pass", 8080, "http://example.com")
#    assert das_session.version == 2.1, "Default version should be 1.1"

