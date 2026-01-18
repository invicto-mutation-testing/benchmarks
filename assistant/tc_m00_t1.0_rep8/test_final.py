import pytest
from put import Session, DasSession, Mapped, requests

class TestSession:
    def test_init_valid_parameters(self):
        session = Session(username="user", password="pass", port=8080)
        assert session.username == "user"
        assert session.password == "pass"
        assert session.port == 8080

class TestDasSession:
    @pytest.fixture(scope="function")
    def setup_das_session(self):
        requests_session = requests.Session()
        das_session = DasSession(
            username="das_user",
            password="das_pass",
            port=9090,
            url="http://localhost",
            version=1.1,
            session=requests_session)
        return das_session

    def test_init_valid_parameters(self, setup_das_session):
        das_session = setup_das_session
        assert das_session.username == "das_user"
        assert das_session.password == "das_pass"
        assert das_session.port == 9090
        assert das_session.url == "http://localhost"
        assert das_session.version == 1.1
        assert isinstance(das_session.session, requests.Session)

    def test_init_with_none_parameters(self):
        das_session = DasSession(
            username=None,
            password=None,
            port=None,
            url=None,
            version=None,
            session=None
        )
        assert das_session.username is None
        assert das_session.password is None
        assert das_session.port is None
        assert das_session.url is None
        assert das_session.version is None
        assert das_session.session is None

    def test_session_attributes(self, setup_das_session):
        das_session = setup_das_session
        assert hasattr(das_session, "username")
        assert hasattr(das_session, "password")
        assert hasattr(das_session, "port")
        assert hasattr(das_session, "url")
        assert hasattr(das_session, "version")
        assert hasattr(das_session, "session")

    def test_tablename_matches_original(self):
        assert DasSession.__tablename__ == "saved_das_connection"

    def test_id_column_exists(self):
        assert hasattr(DasSession, 'id')

    def test_user_id_column_exists(self):
        assert hasattr(DasSession, 'user_id')

    def test_url_column_attribute_name(self):
        assert hasattr(DasSession, 'url')

    def test_url_column_not_misnamed(self):
        assert not hasattr(DasSession, 'XXurlXX')

    def test_port_column_not_misnamed(self):
        assert not hasattr(DasSession, 'XXportXX')

    def test_username_column_properly_named(self):
        assert hasattr(DasSession, 'username')

    def test_username_column_not_misnamed(self):
        assert not hasattr(DasSession, 'XXusernameXX')

    def test_username_column_exists_with_value(self, setup_das_session):
        das_session = setup_das_session
        assert das_session.username is not None, "username attribute should not be None or removed"

    def test_username_column_is_mapped(self):
        assert isinstance(DasSession.username, Mapped)

    def test_password_column_properly_named(self):
        assert hasattr(DasSession, 'password')

    def test_password_column_not_misnamed(self):
        assert not hasattr(DasSession, 'XXpasswordXX')

    def test_password_mapped_column(self):
        assert isinstance(DasSession.password, Mapped)

    def test_version_column_properly_named(self):
        assert hasattr(DasSession, 'version')

    def test_version_column_not_misnamed(self):
        assert not hasattr(DasSession, 'XXversionXX')

    # Revised version of the test to check for the default version.
    # This test no longer requires 'mocker' which was causing issues.
    def test_default_version_matches_expected(self):
        # Directly create a new DasSession to check the default version value
        das_session = DasSession(
            username="test_user",
            password="test_pass",
            port=8080,
            url="http://example.com"
        )
        assert das_session.version == 1.1, "Default version should be 1.1"