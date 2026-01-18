from typing import Optional

import pytest
import requests
from nds_script import DasSession, Session
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def test_session_init():
    session = Session("user", "password123", 8080)
    assert session.username == "user"
    assert session.password == "password123"
    assert session.port == 8080

def test_das_session_init_all_parameters():
    das_sess = DasSession(
        username="user",
        password="secret",
        port=8081,
        url="https://example.com",
        version=2.5
    )
    assert das_sess.username == "user"
    assert das_sess.password == "secret"
    assert das_sess.port == 8081
    assert das_sess.url == "https://example.com"
    assert das_sess.version == 2.5

def test_das_session_with_no_parameters():
    das_sess = DasSession()
    assert das_sess.username is None
    assert das_sess.password is None
    assert das_sess.port is None
    assert das_sess.url is None
    assert das_sess.version == 1.1

def test_das_session_init_without_optional_parameters():
    das_sess = DasSession(
        username="admin",
        password="adminPass",
        port=443
    )
    assert das_sess.username == "admin"
    assert das_sess.password == "adminPass"
    assert das_sess.port == 443
    assert das_sess.url is None
    assert das_sess.version == 1.1

# def test_das_session_type_error_on_username():
#     with pytest.raises(TypeError):
#         DasSession(
#             username=123,
#             password="password",
#             port=443
#         )

# def test_das_session_type_error_on_password():
#     with pytest.raises(TypeError):
#         DasSession(
#             username="user",
#             password=987,
#             port=443
#         )

# def test_das_session_value_error_on_port():
#     with pytest.raises(ValueError):
#         DasSession(
#             username="user",
#             password="password",
#             port="eighty"
#         )

# def test_das_session_type_error_on_version():
#     with pytest.raises(TypeError):
#         DasSession(
#             username="user",
#             password="password",
#             port=443,
#             version="latest"
#         )

# def test_das_session_tablename():
#     das_sess = DasSession()
#     assert das_sess.__tablename__ == "saved_das_connection"



def test_das_session_tablename():
    das_sess = DasSession()
    assert das_sess.__tablename__ == "saved_das_connection"



def test_das_session_tablename_check():
    das_sess = DasSession()
    assert das_sess.__tablename__ == "saved_das_connection"



# def test_primary_key_status():
#     das_sess = DasSession()
#     assert hasattr(das_sess, 'id')
#     assert das_sess.id.property.columns[0].primary_key



def test_das_session_primary_key_initialized():
    das_sess = DasSession()
    assert das_sess.id is not None



# def test_foreign_key_user_id_properly_set():
#     das_sess = DasSession()
#     assert 'users.id' in str(das_sess.user_id.property.columns[0].foreign_keys)

