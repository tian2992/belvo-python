from unittest.mock import MagicMock

import pytest

from belvo.client import Client
from belvo.exceptions import BelvoAPIException


def test_client_will_raise_exception_wheh_no_url_given():

    with pytest.raises(BelvoAPIException) as exc:
        Client(secret_key_id="a", secret_key_password="b")

    assert str(exc.value) == "You need to provide a URL."


@pytest.mark.usefixtures("unauthorized_response")
def test_client_will_raise_exception_when_login_has_failed():
    with pytest.raises(BelvoAPIException) as exc:
        Client(secret_key_id="a", secret_key_password="b", url="http://fake.url")

    assert str(exc.value) == "Login failed."


@pytest.mark.usefixtures("authorized_response")
@pytest.mark.parametrize(
    "resource_name",
    ["Accounts", "Links", "Transactions", "Owners", "Institutions", "Invoices", "TaxReturns"],
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
