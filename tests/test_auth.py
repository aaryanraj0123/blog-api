# import pytest

# @pytest.mark.asyncio
# async def test_register(client):
#     res = await client.post(
#         "/auth/register",
#         json={"email": "test1@emample.com", "password": "password123"},
#     )

#     assert res.status_code == 200
#     assert res.json()["email"] == "test1@emample.com"

# @pytest.mark.asyncio
# async def test_login(client):
#     await client.post(
#         "/auth/register",
#         json={"email": "test2@example.com", "password": "password123"},
#     )

#     res = await client.post(
#         "/auth/login",
#         json={"email": "test2@example.com", "password": "password123"},
#     )

#     assert res.status_code == 200
#     assert "access_token" in res.json()

# @pytest.mark.asyncio
# async def get_token(client, email):
#     await client.post(
#         "/auth/register",
#         json={"email": email, "password": "password123"},
#     )

#     res = await client.post(
#         "/auth/login",
#         json={"email": email, "password": "password123"},
#     )

#     return res.json()["access_token"]

import pytest


@pytest.mark.asyncio
async def test_register(client):
    res = await client.post(
        "/auth/register",
        json={"email": "test1@example.com", "password": "password123"},
    )

    assert res.status_code == 200
    assert res.json()["email"] == "test1@example.com"


@pytest.mark.asyncio
async def test_duplicate_register(client):
    await client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "password123"},
    )

    res = await client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "password123"},
    )

    assert res.status_code == 409


@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password123"},
    )

    res = await client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )

    assert res.status_code == 200
    assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_invalid_login(client):
    res = await client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrong"},
    )

    assert res.status_code == 401


async def get_token(client, email: str):
    await client.post(
        "/auth/register",
        json={"email": email, "password": "password123"},
    )

    res = await client.post(
        "/auth/login",
        json={"email": email, "password": "password123"},
    )

    return res.json()["access_token"]

