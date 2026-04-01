import pytest
from tests.test_auth import get_token


@pytest.mark.asyncio
async def test_author_cannot_delete(client):
    token = await get_token(client, "author3@test.com")

    res = await client.delete(
        "/posts/some-random-id", headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code in [403, 422]
