import pytest
from settings import PASSWORD, USERNAME
from tmdb import account
from tmdb.models.media import MediaRequestObject


def test_create_request_token():
    token = account.create_request_token()
    assert token is not None


def test_authenticate_token(create_token):
    authenticated_token = account.authorize_request_token_with_login(create_token, USERNAME, PASSWORD)
    assert authenticated_token is not None


INVALID_LOGIN_CREDS = [
    {"username": "bad username", "password": PASSWORD, "request_token": None},
    {"username": USERNAME, "password": "bad password", "request_token": None},
    {"username": USERNAME, "password": PASSWORD, "request_token": "bad token"},
]


@pytest.mark.parametrize("payload", INVALID_LOGIN_CREDS)
def test_cannot_auth_token_with_invalid_inputs(payload):
    with pytest.raises(ValueError):
        account.authorize_request_token_with_login(**payload)


def test_create_session_id(auth_token):
    session_id = account.create_session_id(auth_token)
    assert session_id is not None


def test_cannot_create_session_with_unauthenticated_token(create_token):
    with pytest.raises(ValueError):
        account.create_session_id(create_token)


def test_get_my_account_details(session_id):
    my_details = account.get_my_account_details(session_id)
    assert my_details["username"] == USERNAME


def test_cannot_get_account_details_with_invalid_session_id(session_id):
    with pytest.raises(ValueError):
        account.get_my_account_details("1234")


def test_mark_as_favorite(session_id, account_id):
    suicide_squad = 436969
    media = MediaRequestObject(**{"media_type": "movie", "media_id": suicide_squad, "favorite": True})
    response = account.mark_as_favorite(media, session_id, account_id)
    assert response["success"] is True


def test_cannot_favorite_movie_that_does_not_exist(session_id, account_id):
    media_id = 0
    with pytest.raises(ValueError):
        media = MediaRequestObject(**{"media_type": "movie", "media_id": media_id, "favorite": True})
        account.mark_as_favorite(media, session_id, account_id)
