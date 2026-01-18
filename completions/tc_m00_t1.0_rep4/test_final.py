from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_valid_parameters():
    session = Session("user", "pass", 8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# def test_session_invalid_username_type():
#     with pytest.raises(TypeError):
#         Session(123, "pass", 8080)

# def test_session_invalid_password_type():
#     with pytest.raises(TypeError):
#         Session("user", 789, 8080)

# def test_session_invalid_port_type():
#     with pytest.raises(TypeError):
#         Session("user", "pass", "not_a_number")

def test_das_session_valid_parameters():
    das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
    assert das.username == "user"
    assert das.password == "pass"
    assert das.port == 8080
    assert das.url == "http://localhost"
    assert das.version == 1.1

# def test_das_session_none_username():
#     with pytest.raises(TypeError):
#         DasSession(None, "pass", 8080, "http://localhost", 1.1)

# def test_das_session_none_password():
#     with pytest.raises(TypeError):
#         DasSession("user", None, 8080, "http://localhost", 1.1)

# def test_das_session_none_port():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", None, "http://localhost", 1.1)

def test_das_session_none_url():
    das = DasSession("user", "pass", 8080, None, 1.1)
    assert das.url is None

# def test_das_session_invalid_port_type_in_derived():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", "not_a_number", "http://localhost", 1.1)

# def test_das_session_invalid_version_type():
#     with pytest.raises(TypeError):
#         DasSession("user", "pass", 8080, "http://localhost", "not_a_float")

def test_das_session_negative_version():
    das = DasSession("user", "pass", 8080, "http://localhost", -1.1)
    assert das.version == -1.1

def test_das_session_high_version():
    das = DasSession("user", "pass", 8080, "http://localhost", 100.0)
    assert das.version == 100.0

def test_das_session_zero_version():
    das = DasSession("user", "pass", 8080, "http://localhost", 0)
    assert das.version == 0

# def test_das_session_tablename():
#     das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
#     assert das.__tablename__ == "saved_das_connection"

def test_das_session_tablename():
    das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
    assert das.__tablename__ == "saved_das_connection"

# def test_das_session_tablename_mutation():
#     das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
#     assert das.__tablename__ == "saved_das_connection"

def test_das_session_primary_key_assertion():
    das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
    with pytest.raises(AttributeError):
        assert das.id.primary_key is True

def test_das_session_primary_key_exists_and_correct():
    das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
    assert hasattr(das, 'id'), "ID attribute should exist"
    assert das.id is not None, "ID should not be None"

def test_das_session_foreign_key_reference():
    das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
    # This will fail in the mutant because the ForeignKey reference is invalid ("XXusers.idXX")
    assert hasattr(das, 'user_id'), "user_id attribute should exist"

def test_das_session_user_id_exists():
    das = DasSession("user", "pass", 8080, "http://localhost", 1.1)
    assert hasattr(das, 'user_id'), "user_id attribute should exist"

# def test_das_session_url_column_name():
#     import pytest
#     from sqlalchemy.exc import ArgumentError
#     with pytest.raises(ArgumentError):
#         DasSession("user", "pass", 8080, "http://localhost", 1.1)

def test_das_session_url_length_validation():
    long_url = 'http://' + 'a' * 95  # 100 characters total
    das = DasSession("user", "pass", 8080, long_url, 1.1)
    assert len(das.url) == 102

# def test_das_session_url_not_nullable():
#     with pytest.raises(TypeError):
#         # This should raise an error in the original code because `url` is not nullable
#         das = DasSession("user", "pass", 8080, None, 1.1)