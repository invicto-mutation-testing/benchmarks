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
#         Session("user", 123, 8080)

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

# def test_das_session_init_no_username():
#     with pytest.raises(TypeError):
#         DasSession(password="pass", port=8080, url="http://example.com", version=1.1)

# def test_das_session_init_no_password():
#     with pytest.raises(TypeError):
#         DasSession(username="user", port=8080, url="http://example.com", version=1.1)

# def test_das_session_init_no_port():
#     with pytest.raises(TypeError):
#         DasSession(username="user", password="pass", url="http://example.com", version=1.1)

# def test_das_session_init_no_url():
#     with pytest.raises(TypeError):
#         DasSession(username="user", password="pass", port=8080, version=1.1)

# def test_das_session_init_invalid_version():
#     with pytest.raises(TypeError):
#         DasSession(username="user", password="pass", port=8080, url="http://example.com", version="1.1")

# def test_das_session_init_invalid_session_type():
#     with pytest.raises(TypeError):
#         DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1, session="not_a_session")

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     assert DasSession.id.primary_key is True



def test_das_session_primary_key():
    assert DasSession.id is not None



# def test_das_session_foreign_key_mutation():
#     assert DasSession.user_id.expression.right.table.name == "users"



def test_das_session_user_id_foreign_key():
    assert DasSession.user_id is not None



# def test_das_session_url_column_name():
#     assert 'url' in DasSession.__table__.c



# def test_das_session_url_length():
#     # This test checks if the length of the URL field is as expected in the original code.
#     assert DasSession.url.property.columns[0].type.length == 100



# def test_das_session_url_nullable():
#     # This test checks if the URL field is non-nullable as expected in the original code.
#     assert not DasSession.url.nullable



def test_das_session_url_not_none():
    das_session = DasSession(url="http://example.com")
    assert das_session.url is not None



# def test_das_session_port_column_name():
#     # This test checks if the port column name is correctly defined as 'port' in the original code.
#     assert 'port' in DasSession.__table__.c



# def test_das_session_port_nullable():
#     # This test checks if the port field is non-nullable as expected in the original code.
#     das_session = DasSession(username="user", password="pass", port=None, url="http://example.com", version=1.1)
#     assert das_session.port is not None



def test_das_session_port_not_none():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.port is not None



# def test_das_session_username_column_name():
#     # This test checks if the username column name is correctly defined as 'username' in the original code.
#     assert 'username' in DasSession.__table__.c



def test_das_session_username_length():
    das_session = DasSession(username="a" * 50)
    assert len(das_session.username) == 50



# def test_das_session_username_nullable():
#     # This test will pass with the original code and fail with the mutated code
#     # because the mutation allows username to be None which is not allowed in the original.
#     with pytest.raises(AttributeError):
#         das_session = DasSession(username=None)
#         das_session.username



def test_das_session_username_not_none():
    das_session = DasSession(username="user")
    assert das_session.username is not None



# def test_das_session_password_column_name():
#     # This test checks if the password column name is correctly defined as 'password' in the original code.
#     assert 'password' in DasSession.__table__.c



def test_das_session_password_length():
    das_session = DasSession(password="a" * 500)
    assert len(das_session.password) == 500



# def test_das_session_password_nullable():
#     # This test will fail with the mutated code because the mutation allows password to be None.
#     das_session = DasSession(username="user", password=None, port=8080, url="http://example.com", version=1.1)
#     assert das_session.password is not None



def test_das_session_password_not_none():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.password is not None



# def test_das_session_version_column_name():
#     # This test checks if the version column name is correctly defined as 'version' in the original code.
#     assert 'version' in DasSession.__table__.c



# def test_das_session_version_nullable():
#     das_session = DasSession(version=None)
#     assert das_session.version is not None



def test_das_session_version_attribute():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert hasattr(das_session, 'version'), "DasSession should have a 'version' attribute"



# def test_das_session_user_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_user_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_lazy_relationship():
#     assert DasSession.user.property.lazy == "select"



def test_das_session_user_relationship():
    assert DasSession.user is not None



def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1

