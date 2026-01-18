import pytest
from put import Session, DasSession
import requests

# Setup and teardown fixtures
@pytest.fixture
def setup_session():
    # Create a basic session object
    session = Session("user", "pass", 8080)
    return session

@pytest.fixture
def setup_das_session():
    # Create a DasSession object with default parameters
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    return das_session

# Test cases for Session class
def test_session_init_valid(setup_session):
    assert setup_session.username == "user"
    assert setup_session.password == "pass"
    assert setup_session.port == 8080

# Test cases for DasSession class
def test_das_session_init_valid(setup_das_session):
    assert setup_das_session.username == "user"
    assert setup_das_session.password == "pass"
    assert setup_das_session.port == 8080
    assert setup_das_session.url == "http://example.com"
    assert setup_das_session.version == 1.1

def test_das_session_init_missing_session():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert isinstance(das_session.session, requests.Session) or das_session.session is None

def test_das_session_table_name():
    assert DasSession.__tablename__ == "saved_das_connection", "The table name has been mutated and does not match the expected 'saved_das_connection'."

def test_das_session_id_column_name():
    assert 'id' in DasSession.__dict__, "The 'id' column name has been mutated and does not match the expected 'id'."

def test_das_session_id_column_not_none():
    assert DasSession.id is not None, "The 'id' column should not be None."

def test_das_session_user_id_foreign_key():
    assert 'user_id' in DasSession.__dict__, "The 'user_id' ForeignKey has been mutated and does not match the expected 'users.id'."

def test_das_session_user_id_not_none():
    assert DasSession.user_id is not None, "The 'user_id' should not be None."

def test_das_session_url_column_name():
    assert 'url' in DasSession.__dict__, "The 'url' column name has been mutated and does not match the expected 'url'."

def test_das_session_url_not_none():
    assert DasSession.url is not None, "The 'url' attribute should not be None."

def test_das_session_url_initialization():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.url == "http://example.com", "The 'url' attribute is not initialized correctly."

def test_das_session_port_column_name():
    assert 'port' in DasSession.__dict__, "The 'port' column name has been mutated and does not match the expected 'port'."

def test_das_session_port_not_none():
    assert DasSession.port is not None, "The 'port' attribute should not be None."

def test_das_session_port_initialization():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.port == 8080, "The 'port' attribute is not initialized correctly."

def test_das_session_username_column_name():
    assert 'username' in DasSession.__dict__, "The 'username' column name has been mutated and does not match the expected 'username'."

def test_das_session_username_not_none():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.username is not None, "The 'username' attribute should not be None."

def test_das_session_password_column_name():
    assert 'password' in DasSession.__dict__, "The 'password' column name has been mutated and does not match the expected 'password'."

def test_das_session_password_not_none():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.password is not None, "The 'password' attribute should not be None."

def test_das_session_version_column_name():
    assert 'version' in DasSession.__dict__, "The 'version' column name has been mutated and does not match the expected 'version'."

def test_das_session_version_not_none():
    assert DasSession.version is not None, "The 'version' attribute should not be None."

def test_das_session_user_relationship():
    assert DasSession.user is not None, "The 'user' relationship should not be None."
    assert hasattr(DasSession.user, 'lazy'), "The 'user' relationship should have a 'lazy' attribute."
    assert DasSession.user.lazy == "select", "The 'lazy' attribute in the 'user' relationship has been mutated and does not match the expected 'select'."

def test_das_session_version_mutation():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.version == 1.1, "The 'version' attribute has been mutated and does not match the expected value of 1.1."

# New test case to catch the mutation in the session attribute
def test_das_session_session_attribute_mutation():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert das_session.session is None, "The 'session' attribute has been mutated and should be None when not explicitly set."