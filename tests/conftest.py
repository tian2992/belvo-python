import pytest

from belvo.http import JWTSession


@pytest.fixture
def fake_url():
    yield "http://fake.url"


@pytest.fixture
def jwt_token_response(responses, fake_url):
    responses.add(
        responses.POST,
        "{}/api/token/".format(fake_url),
        json={"access": "123456-so-fake", "refresh": "654321-also-fake"},
        status=200,
    )
    yield


@pytest.fixture
def jwt_session(fake_url, jwt_token_response):
    session = JWTSession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")
    yield session


@pytest.fixture
def unauthorized_response(responses, fake_url):
    responses.add(
        responses.POST,
        "{}/api/token/".format(fake_url),
        json={"detail": "Unauthorized."},
        status=401,
    )
    yield
