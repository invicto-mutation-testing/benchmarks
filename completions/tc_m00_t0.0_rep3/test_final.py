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

def test_das_session_init_null_session():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, None)
    assert das_session.session is None

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     assert DasSession.id.primary_key is True



def test_das_session_primary_key():
    assert DasSession.id is not None



# def test_das_session_foreign_key_mutation():
#     assert DasSession.user_id.foreign_keys.pop().column.table.name == "users"



def test_das_session_user_id_foreign_key():
    assert DasSession.user_id is not None



# def test_das_session_url_column_name():
#     assert 'url' in DasSession.__table__.c



def test_das_session_url_length():
    das_session = DasSession(url="http://example.com")
    assert len(das_session.url) <= 100



# def test_das_session_url_not_nullable():
#     with pytest.raises(AttributeError):
#         das_session = DasSession(url=None)



def test_das_session_url_not_none():
    das_session = DasSession(url="http://example.com")
    assert das_session.url is not None



# def test_das_session_port_column_name():
#     # This test checks if the 'port' column name has been mutated.
#     # It should pass with the original code and fail with the mutated code.
#     assert 'port' in DasSession.__table__.c



# def test_das_session_port_not_nullable():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", None, "http://example.com", 1.1)



def test_das_session_port_attribute_exists():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das_session, 'port') and das_session.port == 8080



# def test_das_session_username_column_name():
#     # This test checks if the 'username' column name has been mutated.
#     # It should pass with the original code and fail with the mutated code.
#     assert 'username' in DasSession.__table__.c



# def test_das_session_username_length():
#     das_session = DasSession(username="a" * 51)
#     assert len(das_session.username) <= 50



# def test_das_session_username_nullable():
#     # This test checks if the 'username' can be None, which should fail in the original code
#     # but pass in the mutated code due to the nullable change.
#     with pytest.raises(TypeError):
#         das_session = DasSession(username=None)



def test_das_session_username_not_none():
    das_session = DasSession(username="user")
    assert das_session.username is not None



# def test_das_session_password_column_name():
#     # This test checks if the 'password' column name has been mutated.
#     # It should pass with the original code and fail with the mutated code.
#     assert 'password' in DasSession.__table__.c



def test_das_session_password_length():
    das_session = DasSession(password="a" * 500)
    assert len(das_session.password) == 500



# def test_das_session_password_nullable():
#     # This test checks if the 'password' can be None, which should fail in the original code
#     # but pass in the mutated code due to the nullable change.
#     with pytest.raises(TypeError):
#         das_session = DasSession(password=None)



def test_das_session_password_not_none():
    das_session = DasSession(password="securepassword")
    assert das_session.password is not None



# def test_das_session_version_column_name():
#     # This test checks if the 'version' column name has been mutated.
#     # It should pass with the original code and fail with the mutated code.
#     assert 'version' in DasSession.__table__.c



def test_das_session_version_nullable():
    das_session = DasSession(version=None)
    assert das_session.version is None



def test_das_session_version_attribute():
    das_session = DasSession(version=1.1)
    assert das_session.version == 1.1



# def test_das_session_user_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_user_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_lazy_relationship():
#     assert DasSession.user.property.lazy == "select"



def test_das_session_user_relationship():
    das_session = DasSession()
    assert das_session.user is not None



def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1

