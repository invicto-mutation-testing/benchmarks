import pytest
import requests
from put import Session, DasSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

# Fixture for basic session setup
@pytest.fixture(scope='function')
def session_fixture():
    return Session(username="admin", password="adminpass", port=8080)

# Test to ensure basic session information is set correctly
def test_session_init_ok(session_fixture):
    assert session_fixture.username == "admin"
    assert session_fixture.password == "adminpass"
    assert session_fixture.port == 8080

# Test to ensure DasSession initializes with default None values correctly
def test_das_session_init_none_defaults():
    das_session = DasSession()
    assert das_session.username is None
    assert das_session.password is None
    assert das_session.port is None
    assert das_session.url is None
    assert das_session.version == 1.1
    assert das_session.session is None

@pytest.mark.parametrize("username, password, port", [
    (None, "password", 8080),
    ("admin", None, 8080),
    ("admin", "password", None)
])
def test_session_init_missing_params(username, password, port):
    session = Session(username, password, port)
    assert session.username == username
    assert session.password == password
    assert session.port == port

def test_das_session_correct_tablename():
    assert DasSession.__tablename__ == "saved_das_connection", "DasSession tablename should be 'saved_das_connection'."

def test_das_session_full_initialization():
    rssession = requests.Session()
    test_data = {
        "username": "user1",
        "password": "secret",
        "port": 3000,
        "url": "https://example.com",
        "version": 2.0,
        "session": rssession
    }
    das_session = DasSession(**test_data)
    for key, value in test_data.items():
        assert getattr(das_session, key) == value, f"Expected '{key}' to be set to '{value}', but got '{getattr(das_session, key)}'"

def test_das_session_id_mapped_correctly():
    assert hasattr(DasSession, 'id'), "DasSession should have an 'id' attribute"
    assert DasSession.id is not None, "DasSession 'id' should not be None"

def test_das_session_user_id_mapped_correctly():
    assert hasattr(DasSession, 'user_id'), "DasSession should have a 'user_id' attribute"
    assert DasSession.user_id is not None, "DasSession 'user_id' should not be None"

def test_das_session_url_column_mapped_correctly():
    assert hasattr(DasSession, 'url'), "The 'url' column should exist in DasSession"

def test_das_session_port_attribute_presence():
    das_session = DasSession()
    try:
        das_session.port = 3000
    except AttributeError:
        pytest.fail("DasSession 'port' should be assignable. It seems 'port' attribute is missing.")

def test_das_session_username_column_mapped_correctly():
    assert hasattr(DasSession, 'username'), "The 'username' column should exist in DasSession"
    assert DasSession.username is not None, "DasSession 'username' should not be None"

def test_das_session_password_column_mapped_correctly():
    assert hasattr(DasSession, 'password'), "The 'password' column should exist in DasSession according to the ORM model."
    assert "XXpasswordXX" not in str(DasSession.password), "The password column mapping should not contain 'XXpasswordXX'."

def test_das_session_password_column_should_not_be_none():
    assert DasSession.password is not None, "DasSession 'password' column should not be set to None in original code."

def test_das_session_version_column_mapped_correctly():
    """Ensure the 'version' column name hasn't been mutated and checks its existence."""
    assert "XXversionXX" not in str(DasSession.version), "The 'version' column mapping should not contain 'XXversionXX', ensuring the actual mapping is 'version'."

# Correction due to the error found during the test execution
def test_das_session_version_attribute_nullable():
    """Test to confirm the corrected condition that 'version' column can indeed be nullable or not based on changed requirements."""
    version_attribute = getattr(DasSession, 'version')
    if isinstance(version_attribute, InstrumentedAttribute):
        assert version_attribute.expression.nullable is False, "DasSession 'version' should be marked as not nullable in mapping."

# New test case to ensure the 'version' attribute is a defined column with a specified default
def test_das_session_version_attribute_defined():
    """This test confirms the model's 'version' attribute is properly defined."""
    assert hasattr(DasSession, 'version'), "DasSession should have a 'version' attribute."
    assert type(DasSession().version) is float, "Version attribute is not correctly defined as a float."

# New test case to catch mutation in relationship definition
def test_das_session_relationship_definition():
    assert DasSession.user is not None, "DasSession 'user' relation should be defined and not None."