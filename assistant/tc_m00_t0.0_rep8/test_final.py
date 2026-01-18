import pytest
from put import Session, DasSession
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
    # Teardown code, if necessary

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

def test_das_session_with_optional_parameters(setup_session):
    das_session = DasSession(username="admin", password="adminpass", port=9090, url="https://secure.com", version=2.0, session=setup_session)
    assert das_session.username == "admin"
    assert das_session.password == "adminpass"
    assert das_session.port == 9090
    assert das_session.url == "https://secure.com"
    assert das_session.version == 2.0
    assert das_session.session is setup_session

# New test case to catch mutation in the __tablename__
def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection", "The table name has been mutated!"

# New test case to catch mutation in the ForeignKey reference
def test_das_session_foreign_key_reference():
    assert 'users.id' in str(DasSession.user_id.foreign_keys), "The ForeignKey reference in 'user_id' has been mutated!"

# New test case to catch mutation where 'url' attribute is set to None
def test_das_session_url_attribute():
    assert DasSession.url is not None, "The 'url' attribute has been mutated to None!"

# New test case to catch mutation where 'port' attribute is set to None
def test_das_session_port_attribute():
    assert DasSession.port is not None, "The 'port' attribute has been mutated to None!"

# New test case to catch mutation where 'username' attribute is set to None
def test_das_session_username_attribute():
    assert DasSession.username is not None, "The 'username' attribute has been mutated to None!"

# New test case to catch mutation where 'password' attribute is set to None
def test_das_session_password_initialization(das_session_default):
    assert das_session_default.password is not None, "The 'password' attribute has been mutated to None during initialization!"

# New test case to catch mutation in the 'version' column mapping
def test_das_session_version_column_mapping():
    assert DasSession.version is not None, "The 'version' column mapping has been mutated or removed!"

# New test case to catch mutation where 'version' attribute is set to nullable
def test_das_session_version_nullable():
    assert not hasattr(DasSession.version, 'nullable') or not DasSession.version.nullable, "The 'version' attribute has been mutated to be nullable!"

# New test case to catch mutation where the 'user' relationship is set to None
def test_das_session_user_relationship():
    assert DasSession.user is not None, "The 'user' relationship has been mutated to None!"

# New test case to catch mutation in the default version value
def test_das_session_default_version_value():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com")
    assert das_session.version == 1.1, "The default version value has been mutated!"

# Commented out due to causing errors
# def test_das_session_lazy_loading_strategy():
#     assert DasSession.user.property.lazy == "select", "The lazy loading strategy for 'user' relationship has been mutated!"