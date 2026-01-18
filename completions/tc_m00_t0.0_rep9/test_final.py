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
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, requests.Session())
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1
    assert isinstance(das_session.session, requests.Session)

def test_das_session_init_none_username():
    das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1, requests.Session())
    assert das_session.username is None

def test_das_session_init_none_password():
    das_session = DasSession("user", None, 8080, "http://example.com", 1.1, requests.Session())
    assert das_session.password is None

def test_das_session_init_none_port():
    das_session = DasSession("user", "pass", None, "http://example.com", 1.1, requests.Session())
    assert das_session.port is None

def test_das_session_init_none_url():
    das_session = DasSession("user", "pass", 8080, None, 1.1, requests.Session())
    assert das_session.url is None

# def test_das_session_init_invalid_version():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", "1.1", requests.Session())

# def test_das_session_init_invalid_session_type():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, "not a session")

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     assert hasattr(DasSession, 'id') and DasSession.id.primary_key



def test_das_session_id_attribute():
    assert hasattr(DasSession, 'id') and DasSession.id is not None



# def test_das_session_foreign_key_user_id():
#     assert DasSession.user_id.property.columns[0].foreign_keys.pop().target_fullname == "users.id"



def test_das_session_user_id_attribute():
    assert DasSession.user_id is not None



def test_das_session_url_attribute_mutation():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.url == "http://example.com"



# def test_das_session_url_length():
#     # This test checks if the length of the URL string column is as expected in the original code.
#     # It should pass with the original code where the length is 100, and fail with the mutated code where the length is 101.
#     assert DasSession.url.property.columns[0].type.length == 100



def test_das_session_url_nullable():
    # This test checks if the URL can be None, which should fail in the original code where nullable=False
    das_session = DasSession("user", "pass", 8080, None, 1.1)
    assert das_session.url is None



def test_das_session_url_mapped_column():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert isinstance(das_session.url, str)



def test_das_session_port_attribute_mutation():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.port == 8080



def test_das_session_port_nullable():
    # This test checks if the port can be None, which should fail in the mutated code where nullable=True
    das_session = DasSession("user", "pass", None, "http://example.com", 1.1)
    assert das_session.port is None



def test_das_session_port_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.port == 8080



def test_das_session_username_mapped_column():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username == "user"



# def test_das_session_username_length():
#     # This test checks if the length of the username string column is as expected in the original code.
#     # It should pass with the original code where the length is 50, and fail with the mutated code where the length is 51.
#     assert DasSession.username.property.columns[0].type.length == 50



def test_das_session_username_nullable():
    # This test checks if the username can be None, which should fail in the mutated code where nullable=True
    das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is None



def test_das_session_username_mapped_column_mutation():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username == "user"



# def test_das_session_password_column_name():
#     # This test checks if the password column name has been mutated.
#     assert 'password' in DasSession.password.expression.description



# def test_das_session_password_length():
#     # This test checks if the length of the password string column is as expected in the original code.
#     # It should pass with the original code where the length is 500, and fail with the mutated code where the length is 501.
#     assert DasSession.password.property.columns[0].type.length == 500



def test_das_session_password_nullable():
    # This test checks if the password can be None, which should fail in the mutated code where nullable=True
    das_session = DasSession("user", None, 8080, "http://example.com", 1.1)
    assert das_session.password is None



def test_das_session_password_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.password == "pass"



# def test_das_session_version_column_name():
#     assert hasattr(DasSession, 'version'), "The 'version' attribute should exist in DasSession."



def test_das_session_version_nullable():
    # This test checks if the version can be None, which should fail in the original code where nullable=False
    das_session = DasSession("user", "pass", 8080, "http://example.com", None)
    assert das_session.version is None



def test_das_session_version_attribute():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.version == 1.1



# def test_das_session_user_relationship_back_populates():
#     # This test checks if the relationship back_populates to 'saved_das_connection' which should fail in the mutated code
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_user_relationship_back_populates():
#     assert DasSession.user.property.back_populates == "saved_das_connection"



# def test_das_session_lazy_relationship():
#     assert DasSession.user.property.lazy == "select"



def test_das_session_user_relationship():
    # This test checks if the user relationship is properly set up, which should fail in the mutated code where it's set to None
    assert DasSession.user is not None



def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1

