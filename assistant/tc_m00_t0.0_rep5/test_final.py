import pytest
from put import Session, DasSession, Mapped, mapped_column, requests

# Setup and teardown fixtures
@pytest.fixture
def setup_session():
    # Create a standard session object
    session = Session("user", "pass", 8080)
    return session

@pytest.fixture
def setup_das_session():
    # Create a DasSession object with default parameters
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    return das_session

# Test cases for Session class
def test_session_init_valid(setup_session):
    session = setup_session
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# Test cases for DasSession class
def test_das_session_init_valid(setup_das_session):
    das_session = setup_das_session
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1

def test_das_session_table_name():
    assert DasSession.__tablename__ == "saved_das_connection", "The table name has been mutated and does not match the expected 'saved_das_connection'"

def test_das_session_id_column_name():
    assert 'id' in DasSession.__dict__, "The 'id' column name has been mutated and does not match the expected 'id'"

def test_das_session_id_column_not_none():
    assert DasSession.id is not None, "The 'id' column should not be None."

def test_das_session_user_id_foreign_key():
    assert 'users.id' in str(DasSession.user_id.foreign_keys), "The ForeignKey reference in 'user_id' has been mutated and does not match the expected 'users.id'"

def test_das_session_url_column_name():
    assert 'url' in DasSession.__dict__, "The 'url' column name has been mutated and does not match the expected 'url'"

def test_das_session_url_not_none():
    assert DasSession.url is not None, "The 'url' attribute should not be None."

def test_das_session_url_type():
    assert isinstance(DasSession.url, Mapped), "The 'url' attribute should be a mapped column, but it is not."

def test_das_session_port_column_name():
    assert 'port' in DasSession.__dict__, "The 'port' column name has been mutated and does not match the expected 'port'"

def test_das_session_port_not_none():
    assert DasSession.port is not None, "The 'port' attribute should not be None."

def test_das_session_port_type():
    assert isinstance(DasSession.port, Mapped), "The 'port' attribute should be a mapped column, but it is not."

def test_das_session_username_column_name():
    assert 'username' in DasSession.__dict__, "The 'username' column name has been mutated and does not match the expected 'username'"

def test_das_session_username_not_none():
    assert DasSession.username is not None, "The 'username' attribute should not be None."

def test_das_session_username_type():
    assert isinstance(DasSession.username, Mapped), "The 'username' attribute should be a mapped column, but it is not."

def test_das_session_password_column_name():
    assert 'password' in DasSession.__dict__, "The 'password' column name has been mutated and does not match the expected 'password'"

def test_das_session_password_not_none():
    assert DasSession.password is not None, "The 'password' attribute should not be None."

def test_das_session_password_type():
    assert isinstance(DasSession.password, Mapped), "The 'password' attribute should be a mapped column, but it is not."

def test_das_session_version_column_name():
    assert 'version' in DasSession.__dict__, "The 'version' column name has been mutated and does not match the expected 'version'"

def test_das_session_version_not_none():
    assert DasSession.version is not None, "The 'version' attribute should not be None."

def test_das_session_version_type():
    assert isinstance(DasSession.version, Mapped), "The 'version' attribute should be a mapped column, but it is not."

def test_das_session_version_nullable():
    assert not hasattr(DasSession.version, 'nullable') or not DasSession.version.nullable, "The 'version' column should not be nullable."

# Corrected test cases for relationship attributes
def test_das_session_user_relationship_lazy():
    assert DasSession.user.lazy == "select", "The 'lazy' parameter in the 'user' relationship has been mutated and does not match the expected 'select'"

def test_das_session_user_relationship_back_populates():
    assert DasSession.user.back_populates == "saved_das_connection", "The 'back_populates' parameter in the 'user' relationship has been mutated and does not match the expected 'saved_das_connection'"

# New test case to catch mutation in version default value
def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1, "The default version value has been mutated and does not match the expected 1.1"

# New test case to catch mutation in session attribute
def test_das_session_session_attribute():
    das_session = DasSession(session=requests.Session())
    assert das_session.session is not None, "The 'session' attribute should not be None when explicitly set during initialization."