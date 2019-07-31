import pytest

from belvo.client import Client
from belvo.exceptions import BelvoAPIException


def test_client_will_raise_exception_wheh_no_url_given():

    with pytest.raises(BelvoAPIException) as exc:
        Client(username="a", password="b")

    assert str(exc.value) == "You need to provide a URL."
