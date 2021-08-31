import os
import pytest

ENV_VARS = [
    ("API_KEY", "TMDB API Key (v4) is required to work with this project."),
    ("USERNAME", "Set USERNAME in .env"),
    ("PASSWORD", "Set PASSWORD in .env"),
]


@pytest.mark.parametrize("var, message", ENV_VARS)
def test_required_variables_are_set(var, message):
    assert os.environ.get(var) is not None, message
