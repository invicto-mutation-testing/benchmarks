from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_creation_valid_data():
    session = Session(username="user", password="pass", port=8080)
    assert session.username == "user"
    assert session.password == "pass"
    assert session.port == 8080

def test_dassession_creation_valid_data():
    sess = requests.Session()
    dassession = DasSession(username="user", password="pass", port=8080, url="http://localhost", version=1.0, session=sess)
    assert dassession.username == "user"
    assert dassession.password == "pass"
    assert dassession.port == 8080
    assert dassession.url == "http://localhost"
    assert dassession.version == 1.0
    assert dassession.session == sess

def test_dassession_correct_tablename():
    assert DasSession.__tablename__ == "saved_das_connection"

# def test_dassession_user_id_foreign_key():
#     # This test will pass on original since user_id is a ForeignKey and fail on mutant as user_id is None
#     assert callable(getattr(DasSession.user_id, 'property', None)), "user_id should have a property attribute"
