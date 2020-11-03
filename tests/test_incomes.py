from unittest.mock import MagicMock

import pytest

from belvo import resources


def test_incomes_create(api_session):
    incomes = resources.Incomes(api_session)
    incomes.session.post = MagicMock()
    incomes.create("fake-link-uuid")
    incomes.session.post.assert_called()
    incomes.session.post.assert_called_with(
        "/api/incomes/", data={"link": "fake-link-uuid", "save_data": True}, raise_exception=False
    )


@pytest.mark.parametrize(
    ("method", "params"),
    [
        ("list", []),
        ("get", ["fake-id"]),
        ("delete", ["fake-id"]),
        ("resume", ["fake-id", "fake-token"]),
    ],
)
def test_incomes_raises_not_implemented(method, params, api_session):
    incomes = resources.Incomes(api_session)
    with pytest.raises(NotImplementedError):
        getattr(incomes, method)(*params)
