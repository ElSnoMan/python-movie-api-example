import pytest
from tmdb.discover import discover_movies


def test_discover_movies():
    params = {
        "page": 100,
        "include_video": True,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": "false",
    }
    response = discover_movies(params)
    assert response["page"] == 100


@pytest.mark.parametrize("params", [{}, None])
def test_discover_movies_with_no_params_uses_defaults(params):
    response = discover_movies(params)
    assert response["page"] == 1


@pytest.mark.parametrize("page", [0, 1001])
def test_discover_movies_with_invalid_page(page):
    params = {"page": page}
    with pytest.raises(ValueError):
        discover_movies(params)
