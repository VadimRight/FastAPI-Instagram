import pytest

from tests.conftest import client

def test_register():
    responce = client.post("/register", json = {
        "email": "user@example.com",
        "username": "string",
        "password": "string",
    })

    assert responce.status_code == 200
    assert responce.json() == {
    "username": "string",
    "email": "user@example.com",
    "is_active": True,
    "is_verified": False,
    }