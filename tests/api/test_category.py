import requests

from app.dto.category_dto import CategoryDTO


class TestCategories:

    def test_get_all(self, api_client: dict):
        url = f'{api_client['base_url']}/categories'
        response = requests.get(url=url)

        assert response.status_code == 200, 'invalid status code'
        
        for category in response.json():
            CategoryDTO(**category)

    
    def test_get_one(self, api_client: dict, access_token: str):
        headers = {
            'authorization': f'Bearer {access_token}'
        }

        url = f'{api_client['base_url']}/categories/1'
        response = requests.get(url=url, headers=headers)

        assert response.status_code == 200, 'invalid status code'

        json_data = [response.json()]
        assert len(json_data) == 1

        CategoryDTO(**json_data[0])


    def test_get_one_unexisted_category(self, api_client: dict, access_token: str):
        headers = {
            'authorization': f'Bearer {access_token}'
        }

        url = f'{api_client['base_url']}/categories/100000'
        response = requests.get(url=url, headers=headers)

        assert response.status_code == 404, 'invalid status code'

