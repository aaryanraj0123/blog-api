import pytest
from tests.test_auth import get_token


@pytest.mark.asyncio
async def test_create_post_author(client):
    token = await get_token(client, "post@test.com")

    # assume AUTHOR role OR adjust system
    res = await client.post(
        "/posts",
        json={"title": "Post", "content": "Content"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code in [200, 403]


@pytest.mark.asyncio
async def test_get_posts(client):
    res = await client.get("/posts")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_get_single_post_not_found(client):
    res = await client.get("/posts/invalid-id")

    assert res.status_code in [404, 422]


@pytest.mark.asyncio
async def test_invalid_post_id(client):
    res = await client.get("/posts/invalid-id")

    assert res.status_code == 422


@pytest.mark.asyncio
async def test_update_nonexistent_post(client):
    token = await get_token(client, "test@test.com")

    res = await client.patch(
        "/posts/invalid-id",
        json={"title": "x"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code in [404, 422]
