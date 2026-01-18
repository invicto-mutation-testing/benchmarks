import pytest
from put import Session, DasSession, Mapped
import requests

# Setup and teardown fixtures
@pytest.fixture
def setup_session():
    # Setup code before each test
    session = requests.Session()
    yield session
    # Teardown code after each test
    session.close()

@pytest.fixture
def das_session_default():
    # Setup code for a default DasSession object
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    yield das_session
    # No specific teardown needed

# Test cases for Session class
def test_session_initialization():
    session = Session(username="user", password="pass", port=8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# Test cases for DasSession class
def test_das_session_initialization(das_session_default):
    assert das_session_default.username == "user"
    assert das_session_default.password == "pass"
    assert das_session_default.port == 8080
    assert das_session_default.url == "http://example.com"
    assert das_session_default.version == 1.1

def test_das_session_with_requests_session(setup_session):
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1, session=setup_session)
    assert das_session.session is setup_session

def test_das_session_optional_parameters():
    das_session = DasSession()
    assert das_session.username is None
    assert das_session.password is None
    assert das_session.port is None
    assert das_session.url is None
    assert das_session.version == 1.1  # Default version

def test_das_session_password_attribute_not_none():
    das_session = DasSession(password="pass")
    assert das_session.password == "pass", "The 'password' attribute should not be None when provided"

def test_das_session_password_attribute_exists():
    assert hasattr(DasSession, 'password'), "The 'password' attribute should exist in DasSession"

def test_das_session_version_initialization():
    das_session = DasSession(version=2.0)
    assert das_session.version == 2.0, "The 'version' attribute should correctly reflect the initialized value"

def test_das_session_version_not_none():
    das_session = DasSession()
    assert das_session.version is not None, "The 'version' attribute should not be None by default"

def test_das_session_version_attribute_exists():
    assert hasattr(DasSession, 'version'), "The 'version' attribute should exist in DasSession"

# New test cases to catch the mutation
def test_das_session_user_relationship_not_none():
    das_session = DasSession()
    assert das_session.user is not None, "The 'user' attribute should not be None"

def test_das_session_user_relationship_type():
    das_session = DasSession()
    assert isinstance(das_session.user, Mapped), "The 'user' attribute should be of type Mapped"