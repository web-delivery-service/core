import json
import pytest

import requests

from app.settings.config import settings


@pytest.fixture(scope='class')
def api_client() -> str:
    return {'base_url': settings.API_BASE_URL}


@pytest.fixture(scope='session')
def access_token() -> str:
    credentials = {'email': "leonhard11@yandex.ru", 'password': "admin"}

    try:
        response = requests.post(url=f'{settings.API_BASE_URL}/auth/login', json=credentials)
    except:
        raise Exception('Login error')
    
    json_data = response.json()

    if not json_data['accessToken']:
        raise Exception('access token doesnt exist')
    
    return json_data['accessToken']