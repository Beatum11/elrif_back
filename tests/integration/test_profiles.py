# import pytest
# from httpx import AsyncClient

# pytestmark = pytest.mark.asyncio


# async def test_profiles_endpoint_exists(test_client: AsyncClient):
#     response = await test_client.post("/api/0.1.0/profiles/", json={})
#     # Если получаем 404 - роутер не подключен
#     # Если получаем 422 - роутер подключен, но валидация не прошла
#     print(f"Status: {response.status_code}")
#     print(f"Response: {response.json()}")


# async def test_profile_create(created_profile: dict):
#     assert created_profile['name'] == 'John'
#     assert created_profile['surname'] == 'Doe'


# async def test_get_profile(test_client: AsyncClient, created_profile: dict):
    
#     profile_id = created_profile['id']

#     res = await test_client.get(f'/api/0.1.0/profiles/{profile_id}')
#     assert res.status_code == 200
#     assert res.json()['name'] == "John"


# async def test_patch_profile(test_client: AsyncClient, created_profile: dict):
#     new_data = {
#         'name': 'Jeremy'
#     }
#     profile_id = created_profile['id']
#     res = await test_client.patch(f'/api/0.1.0/profiles/{profile_id}', json=new_data)

#     assert res.status_code == 200
#     assert res.json()['name'] == 'Jeremy'
#     assert res.json()['surname'] == 'Doe'


# async def test_put_profile(test_client: AsyncClient, created_profile: dict):
#     new_data = {
#         'name': 'Jeremy',
#         'surname': 'Some',
#         'email': 'jeremy@gmail.com',
#         'wallet_address': '12343321',
#         'additional_info': 'New_Info'
#     }
#     profile_id = created_profile['id']
#     res = await test_client.put(f'/api/0.1.0/profiles/{profile_id}', json=new_data)

#     assert res.status_code == 200
#     assert res.json()['name'] == 'Jeremy'
#     assert res.json()['surname'] == 'Some'
#     assert res.json()['wallet_address'] == '12343321'

# async def test_delete_profile(test_client: AsyncClient, created_profile: dict):
    
#     profile_id = created_profile['id']

#     delete_res = await test_client.delete(f'/api/0.1.0/profiles/{profile_id}')
#     assert delete_res.status_code == 204

