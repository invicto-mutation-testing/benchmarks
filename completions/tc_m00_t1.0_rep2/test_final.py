from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_base_session_input_types():
    session = Session("username", "password", 8080)
    assert session.username == "username"
    assert session.password == "password"
    assert session.port == 8080

def test_das_session_input_types():
    session = DasSession("user", "pass", 80, "http://example.com", 1.1, requests.Session())
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 80
    assert session.url == "http://example.com"
    assert session.version == 1.1

def test_das_session_default_version():
    session = DasSession("user", "pass", 80, "http://example.com")
    assert session.version == 1.1

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"

def test_das_session_id_column_not_none():
    assert DasSession.id is not None

def test_das_session_user_id_column_not_none():
    """This test checks if the `user_id` column in `DasSession` was removed or modified in the mutated code."""
    assert DasSession.user_id is not None

def test_das_session_url_attribute():
    session = DasSession("user", "pass", 80, "http://example.com")
    assert session.url == "http://example.com"

def test_das_session_port_attribute():
    session = DasSession("user", "pass", 80, "http://example.com")
    assert session.port == 80

# def test_das_session_username_max_length():
#     long_username = 'a' * 51  # This is exactly at the boundary of the mutation
#     with pytest.raises(ValueError):  # Adjust exception type based on actual validation in the implementation
#         DasSession(username=long_username, password="password", port=8080, url="http://example.com", version=1.1)
