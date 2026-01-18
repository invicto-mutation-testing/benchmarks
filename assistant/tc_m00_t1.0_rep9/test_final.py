import pytest
from put import Session, DasSession
import requests
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import configure_mappers

configure_mappers()

# Fixture for creating a basic session instance
@pytest.fixture
def basic_session():
    session = Session("user1", "pass1", 8080)
    yield session
    del session

# Fixture for creating a DasSession instance
@pytest.fixture
def das_session():
    session = requests.Session()
    das = DasSession(username="user2", password="pass2", port=8081, url="http://example.com", version=1.1, session=session)
    yield das
    session.close()
    del das

# Test cases from the original suite
def test_das_session_correct_initialization(das_session):
    assert das_session.username == "user2"
    assert das_session.password == "pass2"
    assert das_session.port == 8081
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1

def test_das_session_incomplete_username():
    das = DasSession(username=None, password="pass2", port=8081, url="http://example.com", version=1.1, session=requests.Session())
    assert das.username is None

def test_das_session_incomplete_password():
    das = DasSession(username="user2", password=None, port=8081, url="http://example.com", version=1.1, session=requests.Session())
    assert das.password is None

def test_das_session_incomplete_port():
    das = DasSession(username="user2", password="pass2", port=None, url="http://example.com", version=1.1, session=requests.Session())
    assert das.port is None

def test_das_session_correct_tablename():
    assert DasSession.__tablename__ == 'saved_das_connection', "Table name has been altered and does not match original specification."

def test_das_session_primary_key():
    assert hasattr(DasSession, 'id'), "Attribute 'id' is missing on DasSession."
    assert DasSession.id is not None, "Attribute 'id' should not be None."

def test_das_session_user_id_foreign_key():
    assert hasattr(DasSession, 'user_id'), "Attribute 'user_id' is missing on DasSession."
    assert DasSession.user_id is not None, "Attribute 'user_id' should not be None."

def test_das_session_url_column_definition():
    assert hasattr(DasSession, 'url'), "Attribute 'url' is missing on DasSession."
    assert DasSession.url is not None, "The 'url' should not be initialized with None."

def test_das_session_url_initial_value():
    das = DasSession(username="user2", password="pass2", port=8081, url=None, version=1.1, session=requests.Session())
    assert das.url is None, "The 'url' attribute should start as None until set during initialization."

def test_das_session_port_column_definition():
    assert hasattr(DasSession, 'port'), "Attribute 'port' is missing or altered in DasSession."
    assert DasSession.port is not None, "The 'port' column should exist and not be altered."

def test_das_session_attributes_integrity():
    attributes = [attr for attr in dir(DasSession) if not attr.startswith('__')]
    expected_attrs = ['id', 'user_id', 'url', 'port', 'username', 'password', 'version', 'user']
    assert all(item in attributes for item in expected_attrs), "DasSession attributes have been mutated from original design."

def test_das_session_username_column_definition_detection():
    assert hasattr(DasSession, 'username'), "Attribute 'username' should exist on DasSession."
    assert DasSession.username is not None, "Attribute 'username' is unexpectedly assigned a None."

def test_das_session_version_initialization(das_session):
    assert das_session.version == 1.1, "DasSession version attribute should be initialized to the passed float value and match the constructor."

def test_das_session_version_exists():
    assert hasattr(DasSession, 'version'), "Attribute 'version' is missing on DasSession."

def test_das_session_user_relationship_existence():
    assert hasattr(DasSession, 'user'), "Attribute 'user' should exist on DasSession."
    assert DasSession.user is not None, "DasSession 'user' relationship should not be None."

# New test case to catch the mutation in session initialization
def test_das_session_session_initialization(das_session):
    assert das_session.session is not None, "DasSession 'session' attribute should be initialized with the passed session object, not None."

def test_das_session_default_version_check(das_session):
    assert das_session.version == 1.1, f"Default version value should be 1.1, found {das_session.version} instead"