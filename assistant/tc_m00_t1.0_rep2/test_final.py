# Import necessary modules and classes from 'put.py' for use in the pytest suite
import pytest
from put import Session, DasSession

# Setup and teardown fixtures for Session class
@pytest.fixture
def session_fixture():
    return Session('testuser', 'testpass', 8080)

# Setup and teardown fixtures for DasSession class, modified to include the session from requests library
@pytest.fixture
def dassession_fixture():
    import requests
    test_session = requests.Session()
    return DasSession(username='testuser', password='testpass', port=8080, url='http://localhost', version=1.1, session=test_session)

# Test Suite for Session class
class TestSession:
    def test_valid_initialization(self, session_fixture):
        assert session_fixture.username == 'testuser'
        assert session_fixture.password == 'testpass'
        assert session_fixture.port == 8080

# Test Suite for DasSession class
class TestDasSession:
    def test_valid_initialization(self, dassession_fixture):
        assert dassession_fixture.username == 'testuser'
        assert dassession_fixture.password == 'testpass'
        assert dassession_fixture.port == 8080
        assert dassession_fixture.url == 'http://localhost'
        assert dassession_fixture.version == 1.1

    def test_tablename(self):
        assert DasSession.__tablename__ == "saved_das_connection"

    def test_user_id_exists(self):
        assert hasattr(DasSession, 'user_id'), "user_id attribute does not exist"

    def test_url_attribute_mapping(self):
        instance = DasSession(url='http://example.com')
        assert instance.url == 'http://example.com', "URL attribute should be assigned from initializer"

    def test_port_attribute_mapping(self):
        das_session = DasSession(port=8080)
        assert das_session.port is not None, "Port attribute was removed or mutated to None"
        assert das_session.port == 8080, "Port attribute does not properly assign the value"

    def test_username_attribute_valid_mapping(self):
        instance = DasSession(username='testuser')
        assert instance.username == 'testuser', "Username attribute should be assigned and mapped correctly"

    def test_password_attribute_valid_mapping(self):
        instance = DasSession(password='testpass')
        assert instance.password == 'testpass', "Password attribute should be assigned and mapped correctly"

    def test_version_attribute_mapping(self):
        instance = DasSession()
        assert instance.version is not None, "Version attribute should not be None"
        assert isinstance(instance.version, float), "Version attribute should be a float"
        assert instance.version == 1.1, "Version attribute should be assigned the default value of 1.1 if not specified"

    def test_user_relation_exists(self):
        assert hasattr(DasSession, 'user'), "The 'user' attribute should exist on DasSession."

    # New Test Cases to detect the mutation or correct setup
    def test_session_initialization(self, dassession_fixture):
        assert dassession_fixture.session is not None, "DasSession.session attribute should not be None upon proper initialization."
        # This assertion now correctly reflects intended setup from fixture modification