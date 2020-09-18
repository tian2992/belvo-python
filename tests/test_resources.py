from unittest.mock import MagicMock, patch

import pytest
from freezegun import freeze_time

from belvo.enums import AccessMode
from belvo.resources import (
    Accounts,
    Balances,
    Incomes,
    Institutions,
    Invoices,
    Links,
    Owners,
    Statements,
    TaxReturns,
    TaxStatus,
    Transactions,
    WidgetToken,
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
            "access_mode": "single",
        },
        raise_exception=False,
    )


def test_links_create_recurrent_link(api_session):
    link = Links(api_session)
    link.session.post = MagicMock()

    link.create("fake-bank", "fake-user", "fake-password", access_mode=AccessMode.RECURRENT)

    link.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "save_data": True,
            "access_mode": "recurrent",
        },
        raise_exception=False,
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
            "access_mode": "single",
        },
        raise_exception=False,
    )


def test_links_create_sends_username2_if_given(api_session):
    links = Links(api_session)
    links.session.post = MagicMock()
    links.create("fake-bank", "fake-user", "fake-password", username2="fake-user-two")

    links.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "username2": "fake-user-two",
            "password": "fake-password",
            "save_data": True,
            "access_mode": "single",
        },
        raise_exception=False,
    )


def test_links_create_sends_password2_if_given(api_session):
    links = Links(api_session)
    links.session.post = MagicMock()
    links.create("fake-bank", "fake-user", "fake-password", password2="fake-password-two")

    links.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "password2": "fake-password-two",
            "save_data": True,
            "access_mode": "single",
        },
        raise_exception=False,
    )


def test_links_create_sends_username_type_if_given(api_session):
    links = Links(api_session)
    links.session.post = MagicMock()
    links.create("fake-bank", "fake-user", "fake-password", username_type="001")

    links.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "save_data": True,
            "access_mode": "single",
            "username_type": "001",
        },
        raise_exception=False,
    )


def test_links_create_with_key_cert(api_session):
    with patch("belvo.resources.read_file_to_b64") as mocked_b64:
        mocked_b64.return_value = "123b64file123"
        links = Links(api_session)
        links.session.post = MagicMock()
        links.create(
            "fake-bank",
            "fake-user",
            "fake-password",
            certificate="/path/to/cert",
            private_key="/path/to/key",
        )

        links.session.post.assert_called_with(
            "/api/links/",
            data={
                "institution": "fake-bank",
                "username": "fake-user",
                "password": "fake-password",
                "save_data": True,
                "access_mode": "single",
                "certificate": "123b64file123",
                "private_key": "123b64file123",
            },
            raise_exception=False,
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
        raise_exception=False,
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
        raise_exception=False,
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
        raise_exception=False,
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
        raise_exception=False,
    )


@freeze_time("2019-02-28T12:00:00Z")
def test_balances_create_sets_current_time_if_no_date_given(api_session):
    balances = Balances(api_session)
    balances.session.post = MagicMock()
    balances.create("fake-link-uuid", "2019-01-01", save_data=False)

    balances.session.post.assert_called_with(
        "/api/balances/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": False,
        },
        raise_exception=False,
    )


def test_balance_create_sends_token_if_given(api_session):
    balances = Balances(api_session)
    balances.session.post = MagicMock()
    balances.create("fake-link-uuid", "2019-01-01", date_to="2019-02-28", token="fake-token")

    balances.session.post.assert_called_with(
        "/api/balances/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": True,
            "token": "fake-token",
        },
        raise_exception=False,
    )


def test_balances_create_sends_account_if_given(api_session):
    balances = Balances(api_session)
    balances.session.post = MagicMock()
    balances.create("fake-link-uuid", "2019-01-01", date_to="2019-02-28", account="fake-account-id")

    balances.session.post.assert_called_with(
        "/api/balances/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": True,
            "account": "fake-account-id",
        },
        raise_exception=False,
    )


def test_balances_create_sends_encryption_key_if_given(api_session):
    balances = Balances(api_session)
    balances.session.post = MagicMock()
    balances.create("fake-link-uuid", "2019-01-01", date_to="2019-02-28", encryption_key="fake-key")

    balances.session.post.assert_called_with(
        "/api/balances/",
        data={
            "link": "fake-link-uuid",
            "date_from": "2019-01-01",
            "date_to": "2019-02-28",
            "save_data": True,
            "encryption_key": "fake-key",
        },
        raise_exception=False,
    )


def test_accounts_create_sends_encryption_key_if_given(api_session):
    accounts = Accounts(api_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", encryption_key="fake-key")

    accounts.session.post.assert_called_with(
        "/api/accounts/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
        raise_exception=False,
    )


def test_accounts_create_token_if_given(api_session):
    accounts = Accounts(api_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", token="fake-token")

    accounts.session.post.assert_called_with(
        "/api/accounts/",
        data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"},
        raise_exception=False,
    )


def test_owners_create_sends_encryption_key_if_given(api_session):
    owners = Owners(api_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", encryption_key="fake-key")

    owners.session.post.assert_called_with(
        "/api/owners/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
        raise_exception=False,
    )


def test_owners_create_token_if_given(api_session):
    owners = Owners(api_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", token="fake-token")

    owners.session.post.assert_called_with(
        "/api/owners/",
        data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"},
        raise_exception=False,
    )


def test_incomes_create(api_session):
    incomes = Incomes(api_session)
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
    incomes = Incomes(api_session)
    with pytest.raises(NotImplementedError):
        getattr(incomes, method)(*params)


def test_invoices_create(api_session):
    invoices = Invoices(api_session)
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
        "/api/accounts/",
        data={"session": "fake-session", "token": "fake-token"},
        raise_exception=False,
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
        raise_exception=False,
    )


@pytest.mark.parametrize("method", ["resume"])
def test_tax_returns_raises_not_implemented(method, api_session):
    tax_returns = TaxReturns(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(tax_returns, method)
        assert func("fake-id", token="fake-token")


def test_tax_status_create(api_session):
    tax_status = TaxStatus(api_session)
    tax_status.session.post = MagicMock()
    tax_status.create("fake-link-uuid", attach_pdf=True)

    tax_status.session.post.assert_called_with(
        "/api/tax-status/",
        data={"link": "fake-link-uuid", "attach_pdf": True, "save_data": True},
        raise_exception=False,
    )


@pytest.mark.parametrize("method", ["resume"])
def test_tax_status_raises_not_implemented(method, api_session):
    tax_status = TaxStatus(api_session)
    with pytest.raises(NotImplementedError):
        func = getattr(tax_status, method)
        assert func("fake-id", token="fake-token")


def test_links_update_password(api_session):
    link = Links(api_session)
    link.session.put = MagicMock()

    link.update(
        "fake-link-uuid",
        password="fake-password",
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
        raise_exception=False,
    )


def test_statements_create(api_session):
    statements = Statements(api_session)
    statements.session.post = MagicMock()
    statements.create("fake-link-uuid", "fake-account-uuid", "2019", "12", attach_pdf=True)

    statements.session.post.assert_called_with(
        "/api/statements/",
        data={
            "link": "fake-link-uuid",
            "account": "fake-account-uuid",
            "year": "2019",
            "month": "12",
            "attach_pdf": True,
            "save_data": True,
        },
        raise_exception=False,
    )


def test_statements_resume(api_session):
    statements = Statements(api_session)
    statements.session.patch = MagicMock()
    statements.resume(
        "fake-session", "fake-token", link="fake-link-uuid", account="fake-account-uuid"
    )

    statements.session.patch.assert_called_with(
        "/api/statements/",
        data={
            "session": "fake-session",
            "token": "fake-token",
            "link": "fake-link-uuid",
            "account": "fake-account-uuid",
        },
        raise_exception=False,
    )


def test_access_token_create(api_session):
    token = WidgetToken(api_session)
    token.session.post = MagicMock()
    token.create()

    token.session.post.assert_called_with(
        "/api/token/",
        data={
            "id": "monty",
            "password": "python",
            "scopes": "read_institutions,write_links,read_links,delete_links",
        },
        raise_exception=False,
    )
