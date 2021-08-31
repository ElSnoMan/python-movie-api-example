""" Account and Authentication

# Generate Session ID
1. Create a new request token
2. Get the user to authorize the request token
3. Create a new session id with the athorized request token
"""
from typing import Dict

import requests
from settings import BASE_URL, HEADERS

from tmdb.models.media import MediaRequestObject


AUTH_URL = BASE_URL + "/authentication"
ACCOUNT_URL = BASE_URL + "/account"


def create_request_token() -> str:
    response = requests.get(AUTH_URL + "/token/new", headers=HEADERS)
    if not response.ok:  # pragma: no cover
        raise ValueError(f"{response.status_code} - {response.text}")

    return response.json()["request_token"]


def authorize_request_token_with_login(request_token: str, username: str, password: str) -> str:
    payload = {
        "username": username,
        "password": password,
        "request_token": request_token,
    }
    response = requests.post(f"{AUTH_URL}/token/validate_with_login", headers=HEADERS, data=payload)
    if not response.ok:
        raise ValueError(f"{response.status_code} - {response.text}")
    return response.json()["request_token"]


def create_session_id(authenticated_token: str) -> str:
    payload = {"request_token": authenticated_token}
    response = requests.post(f"{AUTH_URL}/session/new", headers=HEADERS, data=payload)
    if not response.ok:
        raise ValueError(f"{response.status_code} - {response.text}")
    return response.json()["session_id"]


def get_my_account_details(session_id: str) -> Dict:
    params = {"session_id": session_id}
    response = requests.get(ACCOUNT_URL, params=params, headers=HEADERS)
    if not response.ok:
        raise ValueError(f"{response.status_code} - {response.text}")
    return response.json()


def mark_as_favorite(media: MediaRequestObject, session_id: str, account_id: int) -> Dict:
    params = {"session_id": session_id}
    payload = media.dict()
    response = requests.post(
        f"{ACCOUNT_URL}/{account_id}/favorite",
        params=params,
        data=payload,
        headers=HEADERS,
    )
    if not response.ok:
        raise ValueError(f"{response.status_code} - {response.text}")
    return response.json()
