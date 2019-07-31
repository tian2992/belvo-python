import pytest

from belvo.http import JWTSession


@pytest.fixture
def fake_url():
    yield "http://fake.url"


@pytest.fixture
def jwt_session(responses, fake_url):
    responses.add(
        responses.POST,
        f"{fake_url}/api/token/",
        json={"access": "123456-so-fake", "refresh": "654321-also-fake"},
        status=200,
    )

    session = JWTSession(fake_url)
    session.login(username="monty", password="python")

    yield session
