from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from belvo.resources import (
    Accounts,
    Institutions,
    Invoices,
    Links,
    Owners,
    TaxReturns,
    Transactions,
)


def test_links_create_sends_token_if_given(api_session):
    link = Links(api_session)
    link.session.post = MagicMock()

    link.create("fake-bank", "fake-user", "fake-password", token="fake-token")

    link.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "save_data": True,
            "token": "fake-token",
        },
    )


def test_links_create_sends_encryption_key_if_given(api_session):
    links = Links(api_session)
    links.session.post = MagicMock()
    links.create("fake-bank", "fake-user", "fake-password", encryption_key="fake-key")

    links.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "save_data": True,
            "encryption_key": "fake-key",
        },
    )


@freeze_time("2019-02-28T12:00:00Z")
def test_transactions_create_sets_current_time_if_no_date_given(api_session):
    transactions = Transactions(api_session)
    transactions.session.post = MagicMock()
    transactions.create("fake-link-uuid", "2019-01-01", save_data=False)

    transactions.session.post.assert_called_with(
        "/api/transactions/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": False,
        },
    )


def test_transactions_create_sends_token_if_given(api_session):
    transactions = Transactions(api_session)
    transactions.session.post = MagicMock()
    transactions.create("fake-link-uuid", "2019-01-01", date_to="2019-02-28", token="fake-token")

    transactions.session.post.assert_called_with(
        "/api/transactions/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": True,
            "token": "fake-token",
        },
    )


def test_transactions_create_sends_account_if_given(api_session):
    transactions = Transactions(api_session)
    transactions.session.post = MagicMock()
    transactions.create(
        "fake-link-uuid", "2019-01-01", date_to="2019-02-28", account="fake-account-id"
    )

    transactions.session.post.assert_called_with(
        "/api/transactions/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": True,
            "account": "fake-account-id",
        },
    )


def test_transactions_create_sends_encryption_key_if_given(api_session):
    transactions = Transactions(api_session)
    transactions.session.post = MagicMock()
    transactions.create(
        "fake-link-uuid", "2019-01-01", date_to="2019-02-28", encryption_key="fake-key"
    )

    transactions.session.post.assert_called_with(
        "/api/transactions/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": True,
            "encryption_key": "fake-key",
        },
    )


def test_accounts_create_sends_encryption_key_if_given(api_session):
    accounts = Accounts(api_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", encryption_key="fake-key")

    accounts.session.post.assert_called_with(
        "/api/accounts/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
    )


def test_accounts_create_token_if_given(api_session):
    accounts = Accounts(api_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", token="fake-token")

    accounts.session.post.assert_called_with(
        "/api/accounts/", data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"}
    )


def test_owners_create_sends_encryption_key_if_given(api_session):
    owners = Owners(api_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", encryption_key="fake-key")

    owners.session.post.assert_called_with(
        "/api/owners/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
    )


def test_owners_create_token_if_given(api_session):
    owners = Owners(api_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", token="fake-token")

    owners.session.post.assert_called_with(
        "/api/owners/", data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"}
    )


def test_invoices_create(api_session):
    invoices = Invoices(api_session)
    invoices.session.post = MagicMock()
    invoices.create("fake-link-uuid", "2019-10-01", "2019-11-30", "INFLOW")

    invoices.session.post.assert_called_with(
        "/api/invoices/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-10-01",
            "date_to": "2019-11-30",
            "type": "INFLOW",
            "save_data": True,
        },
    )


@pytest.mark.parametrize("method", ["resume"])
def test_invoices_raises_not_implemented(method, api_session):
    invoices = Invoices(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(invoices, method)
        assert func("fake-id", token="fake-token")


@pytest.mark.parametrize(
    ("method", "params"), [("resume", {"fake-token", "fake-session"}), ("delete", {"fake-token"})]
)
def test_institutions_raises_not_implemented(method, params, api_session):
    institutions = Institutions(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(institutions, method)
        assert func(*params)


def test_account_resume(api_session):
    accounts = Accounts(api_session)
    accounts.session.patch = MagicMock()
    accounts.resume("fake-session", "fake-token")

    accounts.session.patch.assert_called_with(
        "/api/accounts/", data={"session": "fake-session", "token": "fake-token"}
    )


def test_tax_returns_create(api_session):
    tax_returns = TaxReturns(api_session)
    tax_returns.session.post = MagicMock()
    tax_returns.create("fake-link-uuid", 2019, 2019, attach_pdf=True)

    tax_returns.session.post.assert_called_with(
        "/api/tax-returns/",
        data={
            "link": "fake-link-uuid",
            "year_from": 2019,
            "year_to": 2019,
            "attach_pdf": True,
            "save_data": True,
        },
    )


@pytest.mark.parametrize("method", ["resume"])
def test_tax_returns_raises_not_implemented(method, api_session):
    tax_returns = TaxReturns(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(tax_returns, method)
        assert func("fake-id", token="fake-token")


def test_links_update_password(api_session):
    link = Links(api_session)
    link.session.put = MagicMock()

    link.update(
        "fake-link-uuid",
        "fake-password",
        password2="fake-pw2",
        token="fake-token",
        encryption_key="fake-enc-key",
    )

    link.session.put.assert_called_with(
        "/api/links/",
        id="fake-link-uuid",
        data={
            "password": "fake-password",
            "save_data": True,
            "password2": "fake-pw2",
            "token": "fake-token",
            "encryption_key": "fake-enc-key",
        },
    )
