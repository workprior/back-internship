import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(scope="package")

test_data = {
    "username": "testaasdadssdudvbvsser",
    "email": "testtesasaxvasdassdvctest@exaasdmple.com",
    "firstname": "Test",
    "lastname": "User",
    "hashed_password": "testpasssdfword",
    "is_active": True,
    "city": "TestCity",
    "phone": "1231sdasdf1wqe",
    "avatar": "avataasdr.png",
    "is_superuser": False,
}
test_data_change = {
    "username": "testasasadassdsdfduser",
    "firstname": "chdsfange",
    "lastname": "change",
    "hashed_password": "testpsdcassword",
    "is_active": True,
    "city": "TestCity",
    "phone": "582dv",
    "avatar": "avatar.png",
    "is_superuser": False,
}

company_data = {
    "name": "tessdfttt",
    "description": "testnjktt",
    "address": "tenjkstt",
    "phone": "tesnjktt",
    "email": "tesnjktt@exaasdmple.com",
    "website": "tetnst",
    "visibility": True,
}

company_update_data = {
    "name": "njkjktt",
    "description": "tnjet",
    "address": "tnjkstt",
    "phone": "tenjktt",
    "email": "toijes@exaasdmple.com",
    "website": "tnjket",
    "visibility": True,
}


class Id:
    id = 1
    token = ""
    company_id = 1

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

    def get_company_id(self):
        return self.company_id

    def set_company_id(self, company_id):
        self.company_id = company_id


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


async def test_create_company(async_client: AsyncClient):
    response = await async_client.post(
        "/companies/create",
        json=company_data,
        headers={"Authorization": f"Bearer {user.get_token()}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == company_data["name"]
    user.set_company_id(response.json()["id"])


async def test_get_compani_by_id(async_client: AsyncClient):
    response = await async_client.get(
        f"/companies/{user.get_company_id()}",
        headers={"Authorization": f"Bearer {user.get_token()}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == company_data["name"]


async def test_update_company(async_client: AsyncClient):
    response = await async_client.put(
        f"/companies/{user.get_company_id()}/update",
        json=company_update_data,
        headers={"Authorization": f"Bearer {user.get_token()}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == company_update_data["name"]


async def test_change_company_visibility(async_client: AsyncClient):
    response = await async_client.patch(
        f"/companies/{user.get_company_id()}/visibility",
        json={"visibility": False},
        headers={"Authorization": f"Bearer {user.get_token()}"},
    )
    assert response.status_code == 200
    assert response.json()["visibility"] == False


async def test_get_all_companies(async_client: AsyncClient):
    response = await async_client.get(
        "/companies/all", headers={"Authorization": f"Bearer {user.get_token()}"}
    )
    assert response.status_code == 200


async def test_delete_company(async_client: AsyncClient):
    response = await async_client.delete(
        f"/companies/{user.get_company_id()}/delete",
        headers={"Authorization": f"Bearer {user.get_token()}"},
    )
    assert response.status_code == 200
    assert response.json()["detail"] == f"Company deleted with ID: {user.get_company_id()}"


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


async def test_get_user(async_client: AsyncClient):
    response = await async_client.get(f"/user/{user.get_id()}/")
    assert response.status_code == 200


async def test_create_wrong_user(async_client: AsyncClient):
    response = await async_client.post("/user/", json=test_data)
    assert response.status_code == 400
    assert response.json()["detail"] == f"User with email {test_data['email']} already exists"


async def test_change_user(async_client: AsyncClient):
    response = await async_client.put(f"/user/{user.get_id()}/update/", json=test_data_change)
    assert response.status_code == 200
    assert response.json()["username"] == test_data_change["username"]


async def test_delete_user(async_client: AsyncClient):
    response = await async_client.delete(f"/user/{user.get_id()}/")
    assert response.status_code == 200
    assert response.json()["detail"] == f"User deleted successfully"


async def test_delete_me(async_client: AsyncClient):
    response = await async_client.delete(
        "/user/me/delete", headers={"Authorization": f"Bearer {user.get_token()}"}
    )
    assert response.status_code == 200
    assert response.json()["detail"] == f"User deleted successfully"
