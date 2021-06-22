from unittest.mock import MagicMock

import pytest

from belvo import resources
from belvo.enums import TaxReturnType


def test_tax_returns_create(api_session):
    tax_returns = resources.TaxReturns(api_session)
    tax_returns.session.post = MagicMock()
    tax_returns.create("fake-link-uuid", "2019", "2019", attach_pdf=True)

    tax_returns.session.post.assert_called_with(
        "/api/tax-returns/",
        data={
            "link": "fake-link-uuid",
            "year_from": "2019",
            "year_to": "2019",
            "attach_pdf": True,
            "save_data": True,
            "type": "yearly",
        },
        raise_exception=False,
    )


def test_tax_returns_create_with_dates(api_session):
    tax_returns = resources.TaxReturns(api_session)
    tax_returns.session.post = MagicMock()
    tax_returns.create(
        "fake-link-uuid", "2019-01-01", "2019-01-02", attach_pdf=True, type_=TaxReturnType.MONTHLY
    )

    tax_returns.session.post.assert_called_with(
        "/api/tax-returns/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-01-02",
            "type": "monthly",
            "attach_pdf": True,
            "save_data": True,
        },
        raise_exception=False,
    )


@pytest.mark.parametrize("method", ["resume"])
def test_tax_returns_raises_not_implemented(method, api_session):
    tax_returns = resources.TaxReturns(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(tax_returns, method)
        assert func("fake-id", token="fake-token")
