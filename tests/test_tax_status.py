from unittest.mock import MagicMock

import pytest

from belvo import resources


def test_tax_status_create(api_session):
    tax_status = resources.TaxStatus(api_session)
    tax_status.session.post = MagicMock()
    tax_status.create("fake-link-uuid", encryption_key="fake-key", attach_pdf=True)

    tax_status.session.post.assert_called_with(
        "/api/tax-status/",
        data={"link": "fake-link-uuid", "attach_pdf": True, "save_data": True, "encryption_key": "fake-key"},
        raise_exception=False,
    )


@pytest.mark.parametrize("method", ["resume"])
def test_tax_status_raises_not_implemented(method, api_session):
    tax_status = resources.TaxStatus(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(tax_status, method)
        assert func("fake-id", token="fake-token")
