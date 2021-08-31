from typing import Dict

import requests
from settings import BASE_URL, HEADERS


def discover_movies(params: Dict) -> Dict:
    response = requests.get(BASE_URL + "/discover/movie", headers=HEADERS, params=params)

    if not response.ok:
        raise ValueError(f"{response.status_code} - {response.text}")
    return response.json()
