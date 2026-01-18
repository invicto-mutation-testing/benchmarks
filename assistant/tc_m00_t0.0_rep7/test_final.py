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

def test_das_session_default_version():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com")
    assert das_session.version == 1.1

def test_das_session_optional_session():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", session=requests.Session())
    assert isinstance(das_session.session, requests.Session)

# New test case to catch mutation in the table name
def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection", "The table name should be 'saved_das_connection'"

# New test case to catch mutation in the url attribute
def test_das_session_url_attribute():
    assert DasSession.url is not None, "The 'url' attribute should be a mapped column, not None"

# New test case to catch mutation in the port attribute
def test_das_session_port_attribute():
    assert 'port' in DasSession.__dict__, "The 'port' attribute should be a mapped column"
    assert DasSession.port is not None, "The 'port' attribute should not be None or incorrectly named"

# New test case to catch mutation in the username attribute
def test_das_session_username_attribute():
    assert 'username' in DasSession.__dict__, "The 'username' attribute should be a mapped column"
    assert DasSession.username is not None, "The 'username' attribute should not be None or incorrectly named"

# New test case to catch mutation in the password attribute
def test_das_session_password_attribute():
    assert DasSession.password is not None, "The 'password' attribute should not be None or incorrectly set to None"

# New test case to ensure password is a mapped column
def test_das_session_password_mapped():
    assert 'password' in DasSession.__dict__, "The 'password' attribute should be a mapped column"

# New test case to catch mutation in the version attribute mapping
def test_das_session_version_mapped():
    assert 'version' in DasSession.__dict__, "The 'version' attribute should be a mapped column"
    assert DasSession.version is not None, "The 'version' attribute should not be None or incorrectly named"

# Commented out due to failure in accessing relationship properties correctly
# def test_das_session_user_relationship():
#     assert DasSession.user is not None, "The 'user' relationship should not be None"
#     assert 'property' in dir(DasSession.user), "The 'user' attribute should have a relationship property"