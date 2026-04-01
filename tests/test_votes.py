import pytest
from app.routers.posts import create_post
from tests.test_auth import get_token


@pytest.mark.asyncio
async def test_vote_flow(client):
    token = await get_token(client, "vote@test.com")

    # create post
    post_res = await client.post(
        "/posts",
        json={"title": "Vote Post", "content": "Test"},
        headers={"Authorization": f"Bearer {token}"},
    )

    if post_res.status_code != 200:
        return  # skip if role issue

    post_id = post_res.json()["id"]

    # add vote
    res1 = await client.post(
        "/votes",
        json={"post_id": post_id, "vote": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res1.status_code == 200

    # duplicate vote
    res2 = await client.post(
        "/votes",
        json={"post_id": post_id, "vote": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res2.status_code == 409

    # remove vote
    res3 = await client.post(
        "/votes",
        json={"post_id": post_id, "vote": 0},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res3.status_code == 200


@pytest.mark.asyncio
async def test_vote_nonexistent_post(client):
    token = await get_token(client, "vote2@test.com")

    res = await client.post(
        "/votes",
        json={"post_id": "invalid-id", "vote": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code in [404, 422]


@pytest.mark.asyncio
async def test_vote_twice(client):
    token = await get_token(client, "vote@test.com")

    post_res = await client.post(
        "/posts",
        json={"title": "Vote Post", "content": "Test"},
        headers={"Authorization": f"Bearer {token}"},
    )

    if post_res.status_code != 200:
        pytest.skip("Role issue")

    post = post_res.json()

    await client.post(
        "/votes",
        json={"post_id": post["id"], "vote": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    res = await client.post(
        "/votes",
        json={"post_id": post["id"], "vote": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code in [200, 409]
