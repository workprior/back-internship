import asyncio

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(scope="package")

test_data = {
    "username": "testasdudvbvsser",
    "email": "testtesasaxvsdvctest@exaasdmple.com",
    "firstname": "Test",
    "lastname": "User",
    "hashed_password": "testpasssdfword",
    "is_active": True,
    "city": "TestCity",
    "phone": "1231sdf1wqe",
    "avatar": "avatar.png",
    "is_superuser": False,
}
test_data_change = {
    "username": "testasasdduser",
    "firstname": "change",
    "lastname": "change",
    "hashed_password": "testpsdcassword",
    "is_active": True,
    "city": "TestCity",
    "phone": "582dv",
    "avatar": "avatar.png",
    "is_superuser": False,
}


class Id:
    id = 1
    token = ""

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token


user = Id()


async def test_create_user(async_client: AsyncClient):
    response = await async_client.post("/user/", json=test_data)
    assert response.status_code == 200
    data = response.json()

    assert data["email"] == test_data["email"]


async def test_get_users(async_client: AsyncClient):
    response = await async_client.get("/users/")
    assert response.status_code == 200
    user.set_id(response.json()["items"][-1]["id"])


async def test_login_user_with_local_jwt(async_client: AsyncClient):
    response = await async_client.post(
        "/user/login/",
        json={"username": test_data["username"], "hashed_password": test_data["hashed_password"]},
    )
    assert response.status_code == 200
    user.set_token(response.json()["access_token"])


async def test_get_me(async_client: AsyncClient):
    response = await async_client.get(
        "/user/me", headers={"Authorization": f"Bearer {user.get_token()}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == test_data["username"]


async def test_update_me(async_client: AsyncClient):
    response = await async_client.put(
        "/user/me/update",
        headers={"Authorization": f"Bearer {user.get_token()}"},
        json=test_data_change,
    )
    assert response.status_code == 200
    assert response.json()["username"] == test_data_change["username"]


async def test_delete_me(async_client: AsyncClient):
    response = await async_client.delete(
        "/user/me/delete", headers={"Authorization": f"Bearer {user.get_token()}"}
    )
    assert response.status_code == 200
    assert response.json()["detail"] == f"User deleted successfully"


# async def test_get_user(async_client: AsyncClient):
#     response = await async_client.get(f"/user/{user_id.get_id()}/")
#     assert response.status_code == 200


# async def test_create_wrong_user(async_client: AsyncClient):
#     response = await async_client.post("/user/", json=test_data)
#     assert response.status_code == 400
#     assert response.json()["detail"] == f"User with email {test_data['email']} already exists"


# async def test_change_user(async_client: AsyncClient):
#     response = await async_client.put(f"/user/{user_id.get_id()}/update/", json=test_data_change)
#     assert response.status_code == 200
#     assert response.json()["email"] == test_data_change["email"]


# async def test_delete_user(async_client: AsyncClient):
#     response = await async_client.delete(f"/user/{user.get_id()}/")
#     assert response.status_code == 200
#     assert response.json()["detail"] == f"User deleted successfully"
