from unittest.mock import MagicMock

import pytest

from belvo import resources


def test_invoices_create(api_session):
    invoices = resources.Invoices(api_session)
    invoices.session.post = MagicMock()
    invoices.create("fake-link-uuid", "2019-10-01", "2019-11-30", "INFLOW", attach_xml=True)

    invoices.session.post.assert_called_with(
        "/api/invoices/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-10-01",
            "date_to": "2019-11-30",
            "type": "INFLOW",
            "attach_xml": True,
            "save_data": True,
        },
        raise_exception=False,
    )


@pytest.mark.parametrize("method", ["resume"])
def test_invoices_raises_not_implemented(method, api_session):
    invoices = resources.Invoices(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(invoices, method)
        assert func("fake-id", token="fake-token")
