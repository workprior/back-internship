import asyncio

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(scope="package")

test_data = {
    "email": "t@example.com",
    "firstname": "Test",
    "lastname": "User",
    "password": "testpassword",
    "is_active": True,
    "city": "TestCity",
    "phone": "123",
    "avatar": "avatar.png",
    "is_superuser": False,
}
test_data_change = {
    "email": "chafest@example.com",
    "firstname": "change",
    "lastname": "change",
    "password": "testpassword",
    "is_active": True,
    "city": "TestCity",
    "phone": "582",
    "avatar": "avatar.png",
    "is_superuser": False,
}


class Id:
    id = 1

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id


user_id = Id()


async def test_example(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200


async def test_create_user(async_client: AsyncClient):
    response = await async_client.post("/user/", json=test_data)
    assert response.status_code == 200
    data = response.json()

    assert data["email"] == test_data["email"]


async def test_get_users(async_client: AsyncClient):
    response = await async_client.get("/users/")
    assert response.status_code == 200
    user_id.set_id(response.json()["items"][-1]["id"])


async def test_get_user(async_client: AsyncClient):
    response = await async_client.get(f"/user/{user_id.get_id()}/")
    assert response.status_code == 200


async def test_create_wrong_user(async_client: AsyncClient):
    response = await async_client.post("/user/", json=test_data)
    assert response.status_code == 400
    assert response.json()["detail"] == f"User with email {test_data['email']} already exists"


async def test_change_user(async_client: AsyncClient):
    response = await async_client.put(f"/user/{user_id.get_id()}/update/", json=test_data_change)
    assert response.status_code == 200
    assert response.json()["email"] == test_data_change["email"]


async def test_delete_user(async_client: AsyncClient):
    response = await async_client.delete(f"/user/{user_id.get_id()}/")
    assert response.status_code == 200
    assert response.json()["detail"] == f"User deleted successfully"
