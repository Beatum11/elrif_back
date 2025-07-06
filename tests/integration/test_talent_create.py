import pytest
from httpx import AsyncClient
import uuid

pytestmark = pytest.mark.asyncio

async def test_talent_profile_create(created_talent: dict):
    assert created_talent['bio'] == 'amazing developer'


async def test_talent_profile_get(test_client: AsyncClient, created_talent: dict):

    profile_id = created_talent['profile_id']

    created_talent_res = await test_client.get(f'/api/0.1.0/profiles/{profile_id}/talent/')
    assert created_talent_res.status_code == 200

    cr_talent_data = created_talent_res.json()
    assert cr_talent_data['bio'] == 'amazing developer'
    assert cr_talent_data['profile_id'] == profile_id


async def test_talent_profile_delete(test_client: AsyncClient, created_talent: dict):
    profile_id = created_talent['profile_id']

    res = await test_client.delete(f'/api/0.1.0/profiles/{profile_id}/talent/')
    assert res.status_code == 204
