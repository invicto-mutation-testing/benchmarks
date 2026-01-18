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

# def test_das_session_init_none_username():
#     with pytest.raises(TypeError):
#         das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1)

# def test_das_session_init_none_password():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", None, 8080, "http://example.com", 1.1)

# def test_das_session_init_none_port():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", None, "http://example.com", 1.1)

# def test_das_session_init_none_url():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, None, 1.1)

# def test_das_session_init_invalid_version():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", "1.1")

# def test_das_session_init_invalid_session_type():
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1, "not a session")

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     assert DasSession.id.primary_key is True



# def test_das_session_id_primary_key():
#     assert hasattr(DasSession, 'id') and DasSession.id.primary_key



# def test_das_session_foreign_key_mutation():
#     with pytest.raises(ArgumentError):
#         # This test checks if the foreign key reference is valid
#         # It should pass with the correct foreign key in the original code
#         # and fail with the incorrect foreign key in the mutated code
#         DasSession.user_id



def test_das_session_user_id_foreign_key():
    assert DasSession.user_id is not None



# def test_das_session_url_column_name():
#     assert 'url' in DasSession.__table__.c



# def test_das_session_url_length():
#     # This test checks if the length of the URL string column is as expected
#     assert DasSession.url.property.columns[0].type.length == 100



# def test_das_session_url_not_nullable():
#     # This test checks if the URL field is not nullable as per the original code
#     with pytest.raises(TypeError):
#         das_session = DasSession("user", "pass", 8080, None, 1.1)



def test_das_session_url_not_none():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.url is not None



# def test_das_session_port_column_name():
#     assert hasattr(DasSession, 'port')



# def test_das_session_port_nullable():
#     # This test checks if the port field is not nullable as per the original code
#     das_session = DasSession("user", "pass", None, "http://example.com", 1.1)
#     assert das_session.port is not None



def test_das_session_port_not_none():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.port is not None



def test_das_session_username_column_name():
    assert hasattr(DasSession, 'username')



# def test_das_session_username_length():
#     das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
#     assert len(das_session.username) <= 50



# def test_das_session_username_nullable():
#     # This test checks if the username field is not nullable as per the original code
#     with pytest.raises(TypeError):
#         das_session = DasSession(None, "pass", 8080, "http://example.com", 1.1)



def test_das_session_username_not_none():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.username is not None



# def test_das_session_password_column_name():
#     # This test checks if the password column name is as expected in the original code
#     assert 'password' in DasSession.__table__.c



# def test_das_session_password_length():
#     das_session = DasSession("user", "pass" * 100, 8080, "http://example.com", 1.1)
#     assert len(das_session.password) == 500



# def test_das_session_password_nullable():
#     # This test checks if the password field is not nullable as per the original code
#     das_session = DasSession("user", None, 8080, "http://example.com", 1.1)
#     assert das_session.password is not None



def test_das_session_password_not_none():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert das_session.password is not None



def test_das_session_version_column_name():
    assert hasattr(DasSession, 'version')



def test_das_session_version_nullable():
    das_session = DasSession("user", "pass", 8080, "http://example.com", None)
    assert das_session.version is None



def test_das_session_version_type():
    das_session = DasSession("user", "pass", 8080, "http://example.com", 1.1)
    assert isinstance(das_session.version, float)



def test_das_session_relationship_back_populates():
    assert DasSession.user.back_populates == "saved_das_connection"



# def test_das_session_relationship_lazy_loading():
#     assert DasSession.user.lazy == "select"



def test_das_session_default_version():
    das_session = DasSession()
    assert das_session.version == 1.1

