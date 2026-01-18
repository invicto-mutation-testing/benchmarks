import pytest
from put import Session, DasSession, Mapped
import requests

# Fixture for creating a basic Session object
@pytest.fixture
def basic_session():
    return Session(username="user", password="pass", port=8080)

# Fixture for creating a DasSession with proper initialization
@pytest.fixture
def das_session():
    return DasSession(username="das_user", password="das_pass", port=8081, url="http://localhost", version=1.1)

# Tests for basic Session class initialization validation
class TestSession:
    def test_session_initialization(self, basic_session):
        assert basic_session.username == "user"
        assert basic_session.password == "pass"
        assert basic_session.port == 8080

# Tests for DasSession class, inheriting from Session
class TestDasSession:
    def test_das_session_initialization(self, das_session):
        assert das_session.username == "das_user"
        assert das_session.password == "das_pass"
        assert das_session.port == 8081
        assert das_session.url == "http://localhost"
        assert das_session.version == 1.1
        assert isinstance(das_session.session, requests.Session) or das_session.session is None

    def test_das_session_with_optional_parameters(self):
        das_session = DasSession()
        assert das_session.username is None
        assert das_session.password is None
        assert das_session.port is None
        assert das_session.url is None
        assert das_session.version == 1.1  # Default

    def test_das_session_bound_defaults(self, das_session):
        session_partial = DasSession(username="partial_user", password="partial_pass")
        assert session_partial.username == "partial_user"
        assert session_partial.password == "partial_pass"
        assert session_partial.port is None
        assert session_partial.url is None

class TestDasSessionTableName:
    def test_table_name(self):
        assert DasSession.__tablename__ == "saved_das_connection", "The table name has been mutated and does not match the expected value."

class TestDasSessionURLMapping:
    def test_url_column_mapping(self):
        assert hasattr(DasSession, 'url'), "URL attribute should be present in DasSession."
        das = DasSession(url="http://example.com")
        assert das.url == "http://example.com", "URL should be correctly set and retrievable in DasSession."

class TestDasSessionPortAttribute:
    def test_port_attribute_presence_and_type(self):
        assert hasattr(DasSession, 'port'), "The 'port' attribute should exist in DasSession."
        das_session = DasSession(port=8081)
        assert das_session.port is not None, "The 'port' attribute should not be None."
        assert isinstance(das_session.port, int), "The 'port' attribute should be of type 'int'."

class TestDasSessionPasswordAttribute:
    def test_password_length_constraint(self, das_session):
        assert len(das_session.password) <= 500, "Passwords can contain up to 500 characters."

class TestDasSessionVersionAttribute:
    def test_version_attribute_initialization(self):
        das_session_with_version = DasSession(username="dummy_user", password="dummy_pass", port=9090, url="http://dummy.com", version=1.2)
        das_session_without_version = DasSession(username="dummy_user", password="dummy_pass", port=9090, url="http://dummy.com")
        assert das_session_with_version.version == 1.2, "Version attribute value does not match the expected"
        assert das_session_without_version.version == 1.1, "Version attribute default value does not match the expected when omitted."

class TestDasSessionUserRelation:
    def test_user_relationship_presence(self):
        """ Verify that the user relationship is correctly set up in the DasSession class. """
        assert hasattr(DasSession, 'user'), "The 'user' relationship should exist in DasSession."
        assert isinstance(DasSession.user, Mapped), "The 'user' attribute should be a mapped type."

# Additional tests to catch mutation
class TestDasSessionMutation:
    def test_session_initialization_retains_provided_session(self):
        provided_session = requests.Session()
        das_session = DasSession(session=provided_session)
        assert das_session.session is provided_session, "DasSession should retain the session object provided during initialization, which it does not in the mutant code."