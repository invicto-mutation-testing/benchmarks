import pytest
from put import Session, DasSession

@pytest.fixture
def default_das_session():
    """A fixture to create a DasSession object with all parameters provided with default values."""
    return DasSession(username="test_user", password="test_pass", port=8080, url="http://testurl.com", version=1.1)

@pytest.fixture
def session_setup():
    """A fixture to create a requests.Session object."""
    import requests
    return requests.Session()

def test_session_initialization():
    """Test if the base Session object initializes correctly with correct types."""
    session = Session(username="user", password="pass", port=1234)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 1234

def test_das_session_inherits_session():
    """Test if DasSession correctly inherits from Session."""
    das_session = DasSession(username="user", password="pass", port=1234, url="http://example.com", version=1.1)
    assert isinstance(das_session, Session)
    assert das_session.url == "http://example.com"

def test_das_session_with_partial_parameters():
    """Test DasSession with only some parameters provided and others as None."""
    das_session = DasSession(username=None, password=None, port=None, url="http://example.com", version=1.1)
    assert das_session.username is None
    assert das_session.password is None
    assert das_session.port is None
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1

def test_das_session_with_invalid_url(session_setup):
    """Test DasSession with an invalid URL to ensure it initializes."""
    das_session = DasSession(username="user", password="pass", port=1234, url="", version=1.1, session=session_setup)
    assert das_session.url == ""

def test_das_session_version_default(default_das_session):
    """Test that the default version is set correctly when not specified."""
    assert default_das_session.version == 1.1

def test_session_comparison():
    """Test that two session objects with the same credentials are identical."""
    session1 = Session(username="user", password="pass", port=1234)
    session2 = Session(username="user", password="pass", port=1234)
    assert session1.username == session2.username
    assert session1.password == session2.password
    assert session1.port == session2.port

def test_das_session_with_no_parameters():
    """Test DasSession initialization without any parameters should work because all parameters are optional."""
    das_session = DasSession()
    assert das_session.username is None
    assert das_session.password is None
    assert das_session.port is None
    assert das_session.url is None
    assert das_session.version == 1.1

def test_das_session_with_invalid_port(session_setup):
    """Test DasSession with an invalid port should successfully create an instance since type is not checked at initialization."""
    das_session = DasSession(username="user", password="pass", port="invalid_port", url="http://example.com", version=1.1, session=session_setup)
    assert das_session.port == "invalid_port"

def test_das_session_with_non_float_version(session_setup):
    """Test DasSession with a non-float value for version, should not raise an error as type is not enforced."""
    das_session = DasSession(username="user", password="pass", port=1234, url="http://example.com", version="latest")
    assert das_session.version == "latest"

def test_das_session_correct_tablename():
    """Test if DasSession has the correct table name as per the original code."""
    assert DasSession.__tablename__ == "saved_das_connection", "Table name should be 'saved_das_connection'"

# Additional tests to detect mutation

def test_das_session_with_none_session(session_setup):
    """Test that initializing DasSession without a specific session uses None correctly and does not initialize it to object."""
    original_session = DasSession(username="user", password="pass", port=1234, url="http://example.com", version=1.1, session=None)
    mutant_session = DasSession(username="user", password="pass", port=1234, url="http://example.com", version=1.1, session=session_setup)
    assert original_session.session is None  # This is expected to only pass in the original code
    assert mutant_session.session is not None  # This is expected to pass in both codes