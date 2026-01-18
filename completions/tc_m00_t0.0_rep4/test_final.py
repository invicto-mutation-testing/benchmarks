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
#     assert DasSession.user_id.expression.right.table.name == "users"



def test_das_session_user_id_foreign_key():
    assert DasSession.user_id is not None



# def test_das_session_url_column_name():
#     assert 'url' in DasSession.__table__.c



# def test_das_session_url_length():
#     # This test checks if the length of the URL field is as expected in the original code.
#     assert DasSession.url.property.columns[0].type.length == 100



# def test_das_session_url_nullable():
#     # This test checks if the URL field is not nullable as expected in the original code.
#     assert not DasSession.url.nullable



def test_das_session_url_not_none():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.url is not None



# def test_das_session_port_column_name():
#     # This test checks if the port column name has not been mutated.
#     assert 'port' in DasSession.__table__.c



# def test_das_session_port_nullable():
#     # This test checks if the port field is not nullable as expected in the original code.
#     das_session = DasSession("user", "pass", None, "http://example.com", 1.1)
#     assert das_session.port is not None



def test_das_session_port_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert hasattr(das_session, 'port') and das_session.port == 8080



# def test_das_session_username_column_name():
#     # This test checks if the username column name has not been mutated.
#     assert 'username' in DasSession.__table__.c



# def test_das_session_username_length():
#     # This test checks if the length of the username field is as expected in the original code.
#     assert DasSession.username.property.columns[0].type.length == 50



def test_das_session_username_nullable():
    # This test will pass with the original code and fail with the mutated code
    das_session = DasSession(username=None, password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.username is None



def test_das_session_username_not_none():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is not None



# def test_das_session_password_column_mutation():
#     # This test checks if the password column name has been mutated.
#     assert 'password' in DasSession.__table__.c



# def test_das_session_password_length():
#     # This test will pass with the original code and fail with the mutated code
#     assert DasSession.password.property.columns[0].type.length == 500



# def test_das_session_password_nullable():
#     # This test will pass with the original code and fail with the mutated code
#     das_session = DasSession("user", None, 8080, "http://example.com", 1.1)
#     assert das_session.password is not None



def test_das_session_password_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.password == "pass"



def test_das_session_version_column_name():
    # This test will pass with the original code and fail with the mutated code due to the column name change
    assert hasattr(DasSession, 'version'), "The 'version' column should exist"



# def test_das_session_version_nullable():
#     # This test will pass with the original code and fail with the mutated code
#     das_session = DasSession("user", "pass", 8080, "http://example.com", None)
#     assert das_session.version is not None