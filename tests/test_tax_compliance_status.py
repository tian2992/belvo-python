from unittest.mock import MagicMock

import pytest

from belvo import resources


def test_tax_compliance_status_create(api_session):
    tax_compliance_status = resources.TaxComplianceStatus(api_session)
    tax_compliance_status.session.post = MagicMock()
    tax_compliance_status.create("fake-link-uuid", attach_pdf=True)

    tax_compliance_status.session.post.assert_called_with(
        "/api/tax-compliance-status/",
        data={"link": "fake-link-uuid", "attach_pdf": True, "save_data": True},
        raise_exception=False,
    )


@pytest.mark.parametrize("method", ["resume"])
def test_tax_compliance_status_raises_not_implemented(method, api_session):
    tax_compliance_status = resources.TaxComplianceStatus(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(tax_compliance_status, method)
        assert func("fake-id", token="fake-token")
