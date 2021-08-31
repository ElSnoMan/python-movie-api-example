import pytest
from settings import USERNAME, PASSWORD
from tmdb import account


@pytest.fixture(scope="function")
def create_token() -> str:
    return account.create_request_token()


@pytest.fixture(scope="function")
def auth_token(create_token) -> str:
    token = create_token
    return account.authorize_request_token_with_login(token, USERNAME, PASSWORD)


@pytest.fixture(scope="function")
def session_id(auth_token) -> str:
    return account.create_session_id(auth_token)


@pytest.fixture(scope="function")
def account_id(session_id) -> str:
    return account.get_my_account_details(session_id)["id"]
