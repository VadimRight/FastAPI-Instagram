from uuid import uuid4
import pytest
from src.auth.crud import create_access_token
from tests.conftest import client
from conftest import async_session
from src.models.models import User
from httpx import AsyncClient
from datetime import timedelta
from src.main import app

def test_register():
    responce = client.post("/register", json = {
        "email": "test@example.com",
        "username": "test",
        "password": "test",
    })
    assert responce.status_code == 200
    assert responce.json() == {
    "username": "test",
    "email": "test@example.com",
    "is_active": True,
    "is_verified": False,
    }


async def test_login_for_access_token():
    # Create a test user
    # async with async_session() as session:
    #     user = User(id= uuid4(), username="test", email="test@example.com", hashed_password=User.hash_password("test"))
    #     session.add(user)
    #     await session.commit()

    # Prepare request form data
    form_data = {
        "username": "test",
        "password": "test",
        "email": "test@example.com",
        "is_active": True,
        "is_verified": False,
    }

    # Make a request to the login endpoint
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/token", data=form_data)

    # Check if the response is successful
    assert response.status_code == 200

    # Decode the access token to get the user ID
    access_token = response.json()["access_token"]
    token_data = await verify_token(access_token)
    user_id = token_data["sub"]

    # Check if the user ID in the token matches the test user's ID
    assert user_id == User.id

async def verify_token(access_token):
# Implement token verification logic here
# For example, using the same method as in the authentication middleware
# Here we'll just decode the token and return the decoded data
    decoded_token = await decode_access_token(access_token)
    return decoded_token

# Helper function to decode the access token
async def decode_access_token(access_token):
    # Decode the access token and return the decoded data
    decoded_token = create_access_token(access_token)
    return decoded_token