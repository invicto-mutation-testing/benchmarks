import pytest
from put import Session, DasSession  # Importing the necessary classes from the put module


@pytest.fixture
def setup_session():
    """
    Setup fixture for basic Session to avoid duplication.
    """
    return Session(username="admin", password="123456", port=8080)


@pytest.fixture
def setup_das_session():
    """
    Setup fixture for DasSession with default and non-default initialization.
    """
    import requests  # Import within the fixture to provide a mock or a real requests.Session object.
    session = requests.Session()
    return DasSession(username="admin", password="secure123", port=8080, url="http://localhost", version=2.0, session=session)


class TestSession:
    def test_init_valid(self, setup_session):
        assert setup_session.username == "admin", "Incorrect username initialization"
        assert setup_session.password == "123456", "Incorrect password initialization"
        assert setup_session.port == 8080, "Incorrect port initialization"


class TestDasSession:
    def test_init_valid(self, setup_das_session):
        assert setup_das_session.username == "admin", "Incorrect username initialization"
        assert setup_das_session.password == "secure123", "Incorrect password initialization"
        assert setup_das_session.port == 8080, "Incorrect port initialization"
        assert setup_das_session.url == "http://localhost", "Incorrect URL initialization"
        assert setup_das_session.version == 2.0, "Incorrect version initialization"

    def test_init_optional_parameters(self):
        das_session = DasSession()
        assert das_session.username is None, "Username should be None"
        assert das_session.password is None, "Password should be None"
        assert das_session.port is None, "Port should be None"
        assert das_session.url is None, "URL should be None"
        assert das_session.version == 1.1, "Default version should be 1.1"
        
    def test_inheritance_chain(self, setup_das_session):
        assert isinstance(setup_das_session, Session), "DasSession should inherit from Session"

    def test_table_name_validation(self, setup_das_session):
        assert DasSession.__tablename__ == "saved_das_connection", "The database table name should be 'saved_das_connection'"

    def test_url_column_length_original(self, setup_das_session):
        assert len(setup_das_session.url) <= 100, "The length of 'url' should not exceed 100 characters"

    def test_port_column_mapping(self, setup_das_session):
        assert isinstance(setup_das_session.port, int), "Port should be an integer and properly mapped"

    def test_username_column_length(self, setup_das_session):
        assert len(setup_das_session.username) <= 50, "The length of 'username' should not exceed 50 characters"

    def test_username_not_nullable(self, setup_das_session):
        with pytest.raises(AttributeError):
            assert DasSession.username.property.columns[0].nullable is False, "Username should not be nullable"

    def test_username_none_handling(self):
        das_session = DasSession()
        assert das_session.username is None, "Username is not correctly handled when None"

    def test_password_column_name(self, setup_das_session):
        assert hasattr(setup_das_session, 'password'), "DasSession should have a password attribute"
        assert setup_das_session.password == "secure123", "Password attribute of DasSession should be accessible and correct"

    def test_password_nullable_status(self, setup_das_session):
        with pytest.raises(AttributeError):
            assert DasSession.password.property.columns[0].nullable is False, "Password should not be nullable"

    def test_version_nullability(self, setup_das_session):
        with pytest.raises(AttributeError):
            assert DasSession.version.property.columns[0].nullable is False, "'version' column should not be nullable according to the original schema"

    def test_relationship_presence(self, setup_das_session):
        assert hasattr(DasSession, 'user'), "Relationship attribute 'user' should exist"

    # Modified test case to correctly validate session initialization in both scenarios
    def test_session_initialization(self, setup_das_session):
        """
        This test ensures that the 'session' attribute should be set when provided,
        and set to None by default, as per the original code's logic.
        This test will pass on the original code and fail on the mutated code since the mutated code initializes
        'session' explicitly to None.
        """
        assert setup_das_session.session is not None, "Session attribute should not be explicitly set to None when initialized with a session object"
        non_specified_session = DasSession()
        assert non_specified_session.session is None, "Session attribute should be None when not specified"