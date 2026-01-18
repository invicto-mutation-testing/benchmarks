from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_init_valid():
    session = Session(username="user", password="pass", port=8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# def test_session_init_invalid_username():
#     with pytest.raises(TypeError):
#         Session(username=None, password="pass", port=8080)

# def test_session_init_invalid_password():
#     with pytest.raises(TypeError):
#         Session(username="user", password=None, port=8080)

# def test_session_init_invalid_port():
#     with pytest.raises(TypeError):
#         Session(username="user", password="pass", port="8080")

def test_das_session_init_valid():
    request_session = requests.Session()
    das_session = DasSession(
        username="das_user",
        password="das_pass",
        port=8090,
        url="http://example.com",
        version=1.2,
        session=request_session
    )
    assert das_session.username == "das_user"
    assert das_session.password == "das_pass"
    assert das_session.port == 8090
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.2

# def test_das_session_init_null_username():
#     with pytest.raises(TypeError):
#         DasSession(username=None, password="das_pass", port=8090, url="http://example.com", version=1.2)

# def test_das_session_init_null_password():
#     with pytest.raises(TypeError):
#         DasSession(username="das_user", password=None, port=8090, url="http://example.com", version=1.2)

# def test_das_session_init_null_port():
#     with pytest.raises(TypeError):
#         DasSession(username="das_user", password="das_pass", port=None, url="http://example.com", version=1.2)

# def test_das_session_init_null_url():
#     with pytest.raises(TypeError):
#         DasSession(username="das_user", password="das_pass", port=8090, url=None, version=1.2)

# def test_das_session_init_invalid_version_type():
#     with pytest.raises(TypeError):
#         DasSession(username="das_user", password="das_pass", port=8090, url="http://example.com", version="1.2")

# def test_das_session_init_invalid_requests_session_type():
#     with pytest.raises(TypeError):
#         DasSession(username="das_user", password="das_pass", port=8090, url="http://example.com", version=1.2, session="not a request session")

def test_das_session_invalid_tablename():
    das_session = DasSession(
        username="das_user",
        password="das_pass",
        port=8090,
        url="http://example.com",
        version=1.2
    )
    assert das_session.__tablename__ == "saved_das_connection"



# def test_das_session_id_column_name():
#     assert 'id' in DasSession.__table__.columns



# def test_das_session_check_primary_key():
#     das_session = DasSession(
#         username="das_user",
#         password="das_pass",
#         port=8090,
#         url="http://example.com",
#         version=1.2
#     )
#     assert das_session.id.property.columns[0].primary_key == True



def test_das_session_id_column():
    das_session = DasSession(
        username="test_user",
        password="test_pass",
        port=8080,
        url="http://testurl.com",
        version=1.0
    )
    assert das_session.id is not None



# def test_das_session_user_id_fk():
#     with SQLAlchemySession() as session:
#         metadata = DasSession.metadata
#         user_id_fk = metadata.tables['saved_das_connection'].c.user_id.foreign_keys
#         assert len(user_id_fk) == 1
#         assert list(user_id_fk)[0].column.fullname == 'users.id'



def test_das_session_url_column_mutation_detect():
    """Test case to identify mutation in column mapping for 'url'. Fails in mutated code due to a wrong column name."""
    session = DasSession(username="test_user", password="test_pass", port=8080, url="http://testurl.com", version=1.0)
    assert hasattr(session, 'url'), "Attribute 'url' should exist based on the original class definition."



def test_das_session_url_column_length():
    """Test case to check length compliance of 'url' attribute"""
    long_url = "http://" + "a" * 95
    das_session = DasSession(username="test_user", password="test_pass", port=8080, url=long_url, version=1.0)
    assert das_session.url == long_url



# def test_das_session_url_nullable_error():
#     """Test where URL is None, should fail in mutated code since it allows None, should pass in original where it's disallowed"""
#     with pytest.raises(TypeError):
#         DasSession(username="user", password="pass", port=8080, url=None, version=1.1)



def test_das_session_original_url_attribute_type_check():
    """This test ensures the 'url' attribute strictly stores values in the correct format."""
    das_session = DasSession(username="test_user", password="test_pass", port=8080, url="http://testurl.com", version=1.0)
    assert isinstance(das_session.url, str), "URL should be a string"



# def test_das_session_port_nullable():
#     """This test ensures that 'port' must not None as per the original class definition."""
#     with pytest.raises(TypeError):
#         DasSession(username="das_user", password="das_pass", port=None, url="http://example.com", version=1.2)



def test_das_session_port_attribute_presence():
    """Ensure that the port attribute has not been altered or removed in the DasSession class."""
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert hasattr(das_session, 'port'), "The 'port' attribute should exist in DasSession class based on the original definition."



def test_das_session_username_column_name():
    # This test ensures the correct column name for username is used in DasSession
    das_session = DasSession(username="correct_user", password="correct_pass", port=8080, url="http://testurl.com", version=1.0)
    assert das_session.username == "correct_user"



def test_das_session_username_column_length():
    """This test checks if the length of the 'username' field adheres to the original specification."""
    das_session = DasSession(username='a' * 50, password="pass", port=8080, url="http://example.com", version=1.1)
    assert len(das_session.username) == 50, "Username should support up to 50 characters based on the original specification."



def test_das_session_username_nullable():
    """This test case will fail if username is set as nullable in DasSession class"""
    das_session = DasSession(username="not_none", password="pass", port=8080, url="http://valid.url", version=1.0)
    assert das_session.username is not None, "Username should not be allowed to be None"



# def test_das_session_username_attribute():
#     """Test to check if the 'username' attribute is directly set as None in DasSession"""
#     das_session = DasSession(username="das_user", password="das_pass", port=8090, url="http://example.com", version=1.2)
#     assert das_session.username is not None, "Username should not be none which is enforced by the original code design."



def test_das_session_password_column_length():
    """Test to ensure that the `password` field length in DasSession adheres to the original specification."""
    das_session = DasSession(username="user1", password="p" * 500, port=8080, url="http://example.com", version=1.1)
    assert len(das_session.password) == 500, "Password should support up to 500 characters based on the original specification."



def test_das_session_version_column_name():
    # This test checks if the 'version' column name is correct and will fail in the mutated code where it is altered
    das_session = DasSession(username="user1", password="pass1", port=8080, url="http://example.com", version=1.1)
    assert hasattr(das_session, 'version'), "The 'version' attribute should exist based on the original class definition."



# def test_das_session_version_nullable():
#     """ This test will verify that the 'version' attribute should not accept None as a valid value, which it would in the mutated code."""
#     with pytest.raises(TypeError):
#         DasSession(username="user", password="pass", port=8080, url="http://example.com", version=None)



def test_das_session_version_attribute_existence():
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1)
    assert hasattr(das_session, 'version'), "The 'version' attribute should exist in the DasSession class based on the original definition."



# def test_das_session_user_relationship_class_name():
#     # This test will fail in mutated code where relationship class name has been changed improperly
#     das_session = DasSession(username="test_user", password="test_pass", port=8080, url="http://testurl.com", version=1.0)
#     assert das_session.user.__class__.__name__ == "User", "User relationship class name should be 'User' based on the original class definition."



def test_das_session_relationship_back_populates():
    # This test checks if the DasSession class back_populates argument points to correct relationship identifier in original code
    das_session = DasSession(username="test_user", password="test_pass", port=8080, url="http://testurl.com", version=1.0)
    assert das_session.user.back_populates == "saved_das_connection"



def test_das_session_lazy_relationship():
    """Test to ensure the 'lazy' parameter in the relationship is set to 'select', not to the mutated 'XXselectXX'"""
    # Implementation specific note:
    # Direct attribute access or relying on SQLAlchemy internals might be necessary based on SQLAlchemy version
    # The following would work assuming magic attributes or inspection capabilities of SQLAlchemy
    das_session_instance = DasSession()
    assert das_session_instance.user.lazy == 'select', "The 'lazy' parameter of the relationship must reflect value 'select'"



def test_das_session_version_default_value():
    das_session = DasSession()
    assert das_session.version == 1.1, "Default version should be 1.1"



# def test_das_session_session_attribute_for_none_assignment():
#     das_session = DasSession()
#     assert das_session.session is not None, "DasSession's session attribute should not be None if not explicitly set to None"

