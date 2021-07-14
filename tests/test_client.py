import os
from unittest.mock import MagicMock, patch

import pytest

from belvo.client import Client
from belvo.exceptions import BelvoAPIException


def test_client_will_raise_exception_wheh_no_url_given():

    with pytest.raises(BelvoAPIException) as exc:
        Client(secret_key_id="a", secret_key_password="b")

    assert str(exc.value) == "You need to provide a URL or a valid environment."


@pytest.mark.usefixtures("unauthorized_response")
def test_client_will_raise_exception_when_login_has_failed():
    with pytest.raises(BelvoAPIException) as exc:
        Client(secret_key_id="a", secret_key_password="b", url="http://fake.url")

    assert str(exc.value) == "Login failed."


@pytest.mark.usefixtures("authorized_response")
@pytest.mark.parametrize(
    "resource_name",
    [
        "Accounts",
        "Links",
        "Transactions",
        "Balances",
        "Owners",
        "Institutions",
        "Incomes",
        "Invoices",
        "TaxReturns",
        "Statements",
        "WidgetToken",
    ],
)
def test_client_resources_uses_same_session_as_client(resource_name):
    c = Client(secret_key_id="a", secret_key_password="b", url="http://fake.url")

    assert c.session is getattr(c, resource_name).session


def test_client_passes_params_as_querystring_when_given(api_session):
    api_session.session.get = MagicMock()
    api_session.get("/api/fake-endpoint/", "fake-id", params={"foo": "bar"})

    api_session.session.get.assert_called_with(
        params={"foo": "bar"}, timeout=5, url="http://fake.url/api/fake-endpoint/fake-id/"
    )


@pytest.mark.parametrize(
    "environment, expected_url",
    [
        ("sandbox", "https://sandbox.belvo.com"),
        ("development", "https://development.belvo.com"),
        ("production", "https://api.belvo.com"),
        ("https://sandbox.belvo.com", "https://sandbox.belvo.com"),
        ("https://development.belvo.com", "https://development.belvo.com"),
        ("https://api.belvo.com", "https://api.belvo.com"),
        ("http://localhost:8000", "http://localhost:8000"),
    ],
)
def test_client_url_is_ok_when_passing_an_url_or_environment_name_in_client(
    responses, environment, expected_url
):
    responses.add(responses.GET, f"{expected_url}/api/")
    client = Client("secret-key", "secret-password", environment)

    assert client.session.url == expected_url


@pytest.mark.parametrize(
    "environment, expected_url",
    [
        ("sandbox", "https://sandbox.belvo.com"),
        ("development", "https://development.belvo.com"),
        ("production", "https://api.belvo.com"),
        ("https://sandbox.belvo.com", "https://sandbox.belvo.com"),
    ],
)
def test_client_url_is_ok_when_environment_is_set_as_variable_variable(
    responses, environment, expected_url
):
    responses.add(responses.GET, f"{expected_url}/api/")

    with patch.dict(os.environ, {"BELVO_API_URL": environment}):
        client = Client("secret-key", "secret-password")

    assert client.session.url == expected_url
