import pytest

from belvo import __version__
from belvo.http import JWTSession


def test_tokens_are_set_correctly(fake_url):
    session = JWTSession(fake_url)
    tokens = {"access": "Some access token", "refresh": "Some refresh token"}
    session.set_tokens(**tokens)

    assert session.access_token == tokens["access"]
    assert session.refresh_token == tokens["refresh"]


def test_login_sets_authorization_header(responses, fake_url):
    responses.add(
        responses.POST,
        "{}/api/token/".format(fake_url),
        json={"access": "123456-so-fake", "refresh": "654321-also-fake"},
        status=200,
    )

    session = JWTSession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")

    assert session.headers["Authorization"] == "Bearer 123456-so-fake"


@pytest.mark.parametrize("wrong_http_code", [400, 401, 403, 500])
def test_login_returns_false_when_bad_response(wrong_http_code, responses, fake_url):
    responses.add(responses.POST, "{}/api/token/".format(fake_url), json={}, status=wrong_http_code)

    session = JWTSession(fake_url)
    result = session.login(secret_key_id="monty", secret_key_password="python")

    assert not result


@pytest.mark.parametrize("wrong_http_code", [400, 401, 403, 500])
def test_delete_returns_false_when_bad_response(wrong_http_code, responses, fake_url, jwt_session):
    responses.add(
        responses.DELETE, "{}/api/resource/666/".format(fake_url), json={}, status=wrong_http_code
    )
    result = jwt_session.delete("/api/resource/", 666)

    assert not result


def test_get_yields_all_results_when_response_contains_next_page(responses, fake_url, jwt_session):
    resource_url = "{}/api/resources/".format(fake_url)
    data = {
        "next": "{}?page=2".format(resource_url),
        "count": 10,
        "results": ["one", "two", "three", "four", "five"],
    }
    resource_url_page_2 = "{}/api/resources/?page=2".format(fake_url)
    data_page_2 = {"next": None, "count": 10, "results": ["six", "seven", "eight", "nine", "ten"]}
    responses.add(responses.GET, resource_url, json=data, status=200, match_querystring=True)
    responses.add(
        responses.GET, resource_url_page_2, json=data_page_2, status=200, match_querystring=True
    )

    results = list(jwt_session.list("/api/resources/"))

    assert len(results) == 10
    assert results == [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
    ]


def test_login_set_correct_user_agent(responses, fake_url):
    responses.add(
        responses.POST,
        "{}/api/token/".format(fake_url),
        json={"access": "123456-so-fake", "refresh": "654321-also-fake"},
        status=200,
    )

    session = JWTSession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")

    assert session.headers["User-Agent"] == f"belvo-python ({__version__})"
