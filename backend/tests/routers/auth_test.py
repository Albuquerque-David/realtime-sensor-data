# tests/routers/auth_test.py
import pytest
from datetime import timedelta
from utils.auth import create_access_token
from middlewares.auth_middleware import get_current_user
from fastapi import HTTPException

@pytest.fixture
def user_data():
    return {"username": "test_user"}

@pytest.fixture
def token(user_data):
    return create_access_token(data=user_data)

def test_create_access_token(user_data):
    token = create_access_token(data=user_data)
    assert isinstance(token, str)

@pytest.mark.asyncio
async def test_get_current_user_valid_token(user_data, token):
    user = await get_current_user(token=token)
    assert user["username"] == user_data["username"]

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    invalid_token = "invalid.token.string"
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=invalid_token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid or expired token"

@pytest.mark.asyncio
async def test_get_current_user_expired_token():
    expired_token = create_access_token(data={"username": "test_user"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=expired_token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid or expired token"
