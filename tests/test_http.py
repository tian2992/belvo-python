import pytest

from belvo import __version__
from belvo.exceptions import RequestError
from belvo.http import APISession


@pytest.mark.parametrize("wrong_http_code", [400, 401, 403, 500])
def test_login_returns_false_when_bad_response(wrong_http_code, responses, fake_url):
    responses.add(responses.GET, "{}/api/".format(fake_url), json={}, status=wrong_http_code)

    session = APISession(fake_url)
    result = session.login(secret_key_id="monty", secret_key_password="python")

    assert not result


@pytest.mark.parametrize("wrong_http_code", [400, 401, 403, 500])
def test_delete_returns_false_when_bad_response(wrong_http_code, responses, fake_url, api_session):
    responses.add(
        responses.DELETE, "{}/api/resource/666/".format(fake_url), json={}, status=wrong_http_code
    )
    result = api_session.delete("/api/resource/", 666)

    assert not result


def test_get_yields_all_results_when_response_contains_next_page(responses, fake_url, api_session):
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

    results = list(api_session.list("/api/resources/"))

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


def test_login_sets_correct_user_agent(responses, fake_url):
    responses.add(responses.GET, "{}/api/".format(fake_url), json={}, status=200)

    session = APISession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")

    assert session.headers["User-Agent"] == f"belvo-python ({__version__})"


def test_login_sets_key_id(responses, fake_url):
    responses.add(responses.GET, "{}/api/".format(fake_url), json={}, status=200)

    session = APISession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")

    assert session.key_id == "monty"


def test_post_raises_exception_on_error_if_raises_exception_is_true(responses, fake_url):
    responses.add(
        responses.POST,
        "{}/fake-resource/".format(fake_url),
        json=[{"code": "unsupported", "message": "Wait, that's illegal!"}],
        status=400,
    )
    session = APISession(fake_url)

    with pytest.raises(RequestError) as exc:
        session.post("/fake-resource/", {}, raise_exception=True)

    assert exc.value.status_code == 400
    assert exc.value.detail == [{"code": "unsupported", "message": "Wait, that's illegal!"}]
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


def test_post_doesnt_raise_exception_on_error_by_default(responses, fake_url):
    responses.add(
        responses.POST,
        "{}/fake-resource/".format(fake_url),
        json=[{"code": "unsupported", "message": "Wait, that's illegal!"}],
        status=400,
    )
    session = APISession(fake_url)

    result = session.post("/fake-resource/", {})

    assert result == [{"code": "unsupported", "message": "Wait, that's illegal!"}]
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


def test_put_raises_exception_on_error_if_raises_exception_is_true(responses, fake_url):
    responses.add(
        responses.PUT,
        "{}/fake-resource/some-id/".format(fake_url),
        json=[{"code": "unsupported", "message": "Wait, that's illegal!"}],
        status=400,
    )
    session = APISession(fake_url)

    with pytest.raises(RequestError) as exc:
        session.put("/fake-resource/", "some-id", {}, raise_exception=True)

    assert exc.value.status_code == 400
    assert exc.value.detail == [{"code": "unsupported", "message": "Wait, that's illegal!"}]
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


def test_put_doesnt_raise_exception_on_error_by_default(responses, fake_url):
    responses.add(
        responses.PUT,
        "{}/fake-resource/some-id/".format(fake_url),
        json=[{"code": "unsupported", "message": "Wait, that's illegal!"}],
        status=400,
    )
    session = APISession(fake_url)

    result = session.put("/fake-resource/", "some-id", {})

    assert result == [{"code": "unsupported", "message": "Wait, that's illegal!"}]
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


def test_patch_raises_exception_on_error_if_raises_exception_is_true(responses, fake_url):
    responses.add(
        responses.PATCH,
        "{}/fake-resource/".format(fake_url),
        json=[{"code": "unsupported", "message": "Wait, that's illegal!"}],
        status=400,
    )
    session = APISession(fake_url)

    with pytest.raises(RequestError) as exc:
        session.patch("/fake-resource/", {}, raise_exception=True)

    assert exc.value.status_code == 400
    assert exc.value.detail == [{"code": "unsupported", "message": "Wait, that's illegal!"}]
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"


def test_patch_doesnt_raise_exception_on_error_by_default(responses, fake_url):
    responses.add(
        responses.PATCH,
        "{}/fake-resource/".format(fake_url),
        json=[{"code": "unsupported", "message": "Wait, that's illegal!"}],
        status=400,
    )
    session = APISession(fake_url)

    result = session.patch("/fake-resource/", {})

    assert result == [{"code": "unsupported", "message": "Wait, that's illegal!"}]
    assert responses.calls[0].request.headers["Content-Type"] == "application/json"
