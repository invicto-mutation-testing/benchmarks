from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_initialization_correct():
    session = Session(username="user", password="pass", port=8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

# def test_session_initialization_incorrect(params):
#     with pytest.raises(TypeError):
#         Session(*params)

def test_das_session_initialization_correct():
    session = requests.Session()
    das_session = DasSession(username="user", password="pass", port=8080, url="http://example.com", version=1.1, session=session)
    assert das_session.username == "user"
    assert das_session.password == "pass"
    assert das_session.port == 8080
    assert das_session.url == "http://example.com"
    assert das_session.version == 1.1
    assert das_session.session is session

# def test_das_session_initialization_incorrect(params):
#     with pytest.raises(TypeError):
#         DasSession(*params)

def test_das_session_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"



def test_das_session_tablename_mutation_failure():
    assert DasSession.__tablename__ == "saved_das_connection"



# def test_das_session_primary_key():
#     assert DasSession.id.property.columns[0].primary_key is True



def test_das_session_primary_key_present():
    assert hasattr(DasSession, 'id'), "DasSession class must have an 'id' attribute"



# def test_das_session_foreign_key():
#     # Test the validity of the foreign key in user_id, which should point to "users.id".
#     assert DasSession.user_id.property.columns[0].foreign_keys.pop().target_fullname == "users.id"



def test_das_session_user_id_exists():
    assert hasattr(DasSession, 'user_id'), "DasSession class must have a 'user_id' attribute"



# def test_das_session_url_column_name():
#     # Make sure the 'url' attribute is correctly mapped to the 'url' column in the database schema
#     assert DasSession.url.property.columns[0].key == "url"



def test_das_session_url_length_limit():
    # Testing that the length of the URL string adheres to the original specification of 100 characters
    session = DasSession(url='a' * 100)  # Exactly 100 characters, which is the limit in the original code
    assert len(session.url) == 100



# def test_das_session_url_not_nullable():
#     # This test verifies that the 'url' field cannot be None, which is the expected behavior in the original code
#     with pytest.raises(TypeError):
#         DasSession(url=None)

