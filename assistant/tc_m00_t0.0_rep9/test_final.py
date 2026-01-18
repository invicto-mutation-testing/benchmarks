import pytest
from put import Session, DasSession, Mapped
import requests

# Setup and teardown fixtures
@pytest.fixture
def setup_session():
    # Setup code for creating a session object
    session = Session(username="user", password="pass", port=8080)
    return session

@pytest.fixture
def setup_das_session():
    # Setup code for creating a DasSession object
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    return das_session

# Test cases for Session class
def test_session_init(setup_session):
    session = setup_session
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# Test cases for DasSession class
def test_das_session_init(setup_das_session):
    das_session = setup_das_session
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1

def test_das_session_missing_session():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert isinstance(das_session.session, requests.Session) or das_session.session is None

def test_das_session_table_name():
    assert DasSession.__tablename__ == "saved_das_connection", "The table name should be 'saved_das_connection'"

def test_das_session_primary_key():
    assert DasSession.id is not None, "The 'id' attribute should not be None"

def test_das_session_foreign_key():
    assert 'users.id' in str(DasSession.user_id.foreign_keys), "The ForeignKey should reference 'users.id'"

def test_das_session_url_column():
    assert DasSession.url is not None, "The URL attribute should not be None"

def test_das_session_port_attribute():
    assert DasSession.port is not None, "The 'port' attribute should not be None"

def test_das_session_username_attribute():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.username == "user", "The 'username' attribute should be 'user'"

def test_das_session_username_nullable():
    assert DasSession.username is not None, "The 'username' column should not be None"

def test_das_session_password_attribute():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.password == "pass", "The 'password' attribute should be 'pass'"

def test_das_session_password_not_none():
    assert DasSession.password is not None, "The 'password' attribute should not be None"

def test_das_session_version_column_mapping():
    assert hasattr(DasSession, 'version'), "DasSession should have a 'version' attribute"
    assert not hasattr(DasSession, 'XXversionXX'), "DasSession should not have a 'XXversionXX' attribute"

def test_das_session_version_type_and_not_none():
    assert isinstance(DasSession.version, Mapped), "Version should be a mapped column"
    assert DasSession.version is not None, "Version attribute should not be None"

def test_das_session_user_relationship():
    assert DasSession.user is not None, "The 'user' attribute should not be None"

def test_das_session_user_relationship_type():
    assert isinstance(DasSession.user, Mapped), "The 'user' attribute should be a mapped relationship"

def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1, "The default version should be 1.1"

# New test case to catch the mutation in session initialization
def test_das_session_session_initialization():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1, session=requests.Session())
    assert das_session.session is not None, "Session should not be None when explicitly provided"