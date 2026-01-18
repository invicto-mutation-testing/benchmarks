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

def test_das_session_initialization_missing_username():
    das_session = DasSession(password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.username is None

def test_das_session_initialization_missing_password():
    das_session = DasSession(username="user", port=8080, url="http://example.com", version=1.1)
    assert das_session.password is None

def test_das_session_initialization_missing_port():
    das_session = DasSession(username="user", password="pass", url="http://example.com", version=1.1)
    assert das_session.port is None

def test_das_session_initialization_missing_url():
    das_session = DasSession(username="user", password="pass", port=8080, version=1.1)
    assert das_session.url is None

def test_das_session_initialization_missing_version():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com")
    assert das_session.version == 1.1  # Default value

def test_das_session_initialization_with_requests_session():
    req_session = requests.Session()
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", session=req_session)
    assert das_session.session == req_session

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     assert DasSession.id.primary_key is True



# def test_das_session_id_primary_key():
#     assert hasattr(DasSession, 'id') and DasSession.id.primary_key



# def test_das_session_foreign_key_user_id():
#     assert DasSession.user_id.property.columns[0].foreign_keys.pop().target_fullname == "users.id"



def test_das_session_user_id_foreign_key():
    assert DasSession.user_id is not None



# def test_das_session_url_column_name():
#     assert 'url' in DasSession.__table__.c



# def test_das_session_url_length():
#     das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com" + "a" * 100, version=1.1)
#     assert len(das_session.url) == 100



# def test_das_session_url_not_nullable():
#     with pytest.raises(TypeError):
#         das_session = DasSession(username="user", password="pass", port=8080, version=1.1)



def test_das_session_url_not_none():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.url is not None



# def test_das_session_port_column_name():
#     # This test checks if the 'port' column name has been mutated.
#     assert 'port' in DasSession.__table__.c



# def test_das_session_port_not_nullable():
#     with pytest.raises(TypeError):
#         das_session = DasSession(username="user", password="pass", url="http://example.com", version=1.1)



def test_das_session_port_attribute():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.port == 8080



# def test_das_session_username_column_name():
#     # This test checks if the 'username' column name has been mutated.
#     assert 'username' in DasSession.__table__.c



def test_das_session_username_length():
    das_session = DasSession(username="a" * 50, password="pass", port=8080, url="http://example.com", version=1.1)
    assert len(das_session.username) == 50



# def test_das_session_username_not_nullable():
#     with pytest.raises(AttributeError):
#         das_session = DasSession(username=None, password="pass", port=8080, url="http://example.com", version=1.1)
#         _ = das_session.username



def test_das_session_username_not_none():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.username is not None



# def test_das_session_password_column_name():
#     # This test checks if the 'password' column name has been mutated.
#     assert 'password' in DasSession.__table__.c



# def test_das_session_password_length():
#     das_session = DasSession(username="user", password="a" * 500, port=8080, url="http://example.com", version=1.1)
#     assert len(das_session.password) == 500



# def test_das_session_password_not_nullable():
#     with pytest.raises(TypeError):
#         # This should raise an error because password should not be nullable in the original code
#         das_session = DasSession(username="user", port=8080, url="http://example.com", version=1.1)



def test_das_session_password_not_none():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.password is not None



def test_das_session_version_column_name():
    # This test checks if the 'version' column name has been mutated.
    assert hasattr(DasSession, 'version')



# def test_das_session_version_nullable():
#     # This test checks if the 'version' attribute can be set to None, which should fail in the original code
#     with pytest.raises(TypeError):
#         das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=None)



def test_das_session_version_attribute():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.version == 1.1



# def test_das_session_user_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_user_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_relationship_lazy_loading():
#     assert DasSession.user.property.lazy == "select"



def test_das_session_user_relationship():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.user is not None

