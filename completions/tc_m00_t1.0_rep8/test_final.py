from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_normal_conditions():
    session = Session("user", "pass", 8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# def test_session_invalid_username_type():
#     with pytest.raises(TypeError):
#         Session(123, "pass", 8080)

# def test_session_invalid_password_type():
#     with pytest.raises(TypeError):
#         Session("user", 123, 8080)

# def test_session_invalid_port_type():
#     with pytest.raises(TypeError):
#         Session("user", "pass", "8080")

def test_das_session_normal_conditions():
    web_session = requests.Session()
    das_ses = DasSession("das_user", "das_pass", 9090, "http://api.example.com", 1.5, session=web_session)
    assert das_ses.username == "das_user"
    assert das_ses.password == "das_pass"
    assert das_ses.port == 9090
    assert das_ses.url == "http://api.example.com"
    assert das_ses.version == 1.5
    assert das_ses.session is web_session

def test_das_session_defaults():
    das_ses = DasSession()
    assert das_ses.username is None
    assert das_ses.password is None
    assert das_ses.port is None
    assert das_ses.url is None
    assert das_ses.version == 1.1
    assert das_ses.session is None

# def test_das_session_invalid_username_type():
#     with pytest.raises(TypeError):
#         DasSession(123, "pass", 8080, "http://api.example.com")

# def test_das_session_invalid_password_type():
#     with pytest.raises(TypeError):
#         DasSession("user", 123, 8080, "http://api.example.com")

# def test_das_session_invalid_port_type():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", "8080", "http://api.example.com")

# def test_das_session_invalid_url_type():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, 123)

# def test_das_session_invalid_version_type():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, "http://api.example.com", "1.1")

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key_mutation_detection():
#     assert isinstance(DasSession.id.property.columns[0].type, Integer) and DasSession.id.property.columns[0].primary_key



# def test_das_session_id_column_presence():
#     assert not hasattr(DasSession, 'id'), "DasSession should not have an 'id' attribute"



# def test_das_session_user_id():
#     """New test case to check user_id attribute to fail in mutated code."""
#     das_session = DasSession("username", "password", 80)
#     with pytest.raises(AttributeError):
#         _ = das_session.user_id  # user_id should exist and be correctly initialized in the original but is set to None in the mutant



# def test_das_session_url_column_name():
#     session = DasSession()
#     assert "url" in session.__table__.c, "Expected 'url' column in table, but not found."



def test_das_session_url_length_mutation():
    das_ses = DasSession(url='a' * 100)
    assert len(das_ses.url) == 100



def test_das_session_url_mutation():
    das_session = DasSession(url="http://valid.url")
    assert das_session.url == "http://valid.url", "URL should be initialized and match the provided value"



# def test_das_session_port_column_presence():
#     das_session = DasSession(port=9090)
#     assert hasattr(das_session, 'port'), "DasSession should have a 'port' attribute"



def test_das_session_port_attribute_presence():
    das_session = DasSession()
    assert hasattr(das_session, 'port'), "DasSession should have a 'port' attribute defined."



# def test_das_session_username_column_name():
#     assert DasSession.username.property.columns[0].name == "username"



# def test_das_session_username_column_length_validation():
#     """Test that asserts the length constraint of the username in DasSession matches the original specification."""
#     import pytest
#     from sqlalchemy.exc import DataError
#     with pytest.raises(DataError):
#         DasSession(username='a' * 51)



# def test_das_session_username_nullable_failure():
#     """Test that checks non-null constraint on username that should fail in mutated code where it is nullable."""
#     das_session = DasSession(username=None)
#     with pytest.raises(ValueError):
#         assert das_session.username is not None, "Username should not be None as per original definition."

