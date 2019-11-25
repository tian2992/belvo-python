from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from belvo.resources import Accounts, Institutions, Invoices, Links, Owners, Transactions


def test_links_create_sends_token_if_given(jwt_session):
    link = Links(jwt_session)
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


def test_links_create_sends_encryption_key_if_given(jwt_session):
    links = Links(jwt_session)
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
def test_transactions_create_sets_current_time_if_no_date_given(jwt_session):
    transactions = Transactions(jwt_session)
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


def test_transactions_create_sends_token_if_given(jwt_session):
    transactions = Transactions(jwt_session)
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


def test_transactions_create_sends_account_if_given(jwt_session):
    transactions = Transactions(jwt_session)
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


def test_transactions_create_sends_encryption_key_if_given(jwt_session):
    transactions = Transactions(jwt_session)
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


def test_accounts_create_sends_encryption_key_if_given(jwt_session):
    accounts = Accounts(jwt_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", encryption_key="fake-key")

    accounts.session.post.assert_called_with(
        "/api/accounts/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
    )


def test_accounts_create_token_if_given(jwt_session):
    accounts = Accounts(jwt_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", token="fake-token")

    accounts.session.post.assert_called_with(
        "/api/accounts/", data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"}
    )


def test_owners_create_sends_encryption_key_if_given(jwt_session):
    owners = Owners(jwt_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", encryption_key="fake-key")

    owners.session.post.assert_called_with(
        "/api/owners/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
    )


def test_owners_create_token_if_given(jwt_session):
    owners = Owners(jwt_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", token="fake-token")

    owners.session.post.assert_called_with(
        "/api/owners/", data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"}
    )


def test_invoices_create(jwt_session):
    invoices = Invoices(jwt_session)
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


@pytest.mark.parametrize("method", ["get", "resume"])
def test_invoices_raises_not_implemented(method, jwt_session):
    invoices = Invoices(jwt_session)
    with pytest.raises(NotImplementedError):
        func = getattr(invoices, method)
        assert func("fake-id", token="fake-token")


@pytest.mark.parametrize(
    ("method", "params"), [("resume", {"fake-token", "fake-session"}), ("delete", {"fake-token"})]
)
def test_institutions_raises_not_implemented(method, params, jwt_session):
    invoices = Institutions(jwt_session)
    with pytest.raises(NotImplementedError):
        func = getattr(invoices, method)
        assert func(*params)


def test_account_resume(jwt_session):
    accounts = Accounts(jwt_session)
    accounts.session.patch = MagicMock()
    accounts.resume("fake-session", "fake-token")

    accounts.session.patch.assert_called_with(
        "/api/accounts/", data={"session": "fake-session", "token": "fake-token"}
    )
