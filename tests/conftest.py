import pytest

from belvo.http import APISession


@pytest.fixture
def fake_url():
    yield "http://fake.url"


@pytest.fixture
def authorized_response(responses, fake_url):
    responses.add(responses.GET, "{}/api/".format(fake_url), json={}, status=200)
    yield


@pytest.fixture
def api_session(fake_url, authorized_response):
    session = APISession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")
    yield session


@pytest.fixture
def unauthorized_response(responses, fake_url):
    responses.add(
        responses.GET, "{}/api/".format(fake_url), json={"detail": "Unauthorized."}, status=401
    )
    yield
