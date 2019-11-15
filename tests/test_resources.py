from unittest.mock import MagicMock

from freezegun import freeze_time

from belvo.resources import Accounts, Links, Owners, Transactions


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
            "encryption_key": "fake-key",
        },
    )


@freeze_time("2019-02-28T12:00:00Z")
def test_transactions_create_sets_current_time_if_no_date_given(jwt_session):
    transactions = Transactions(jwt_session)
    transactions.session.post = MagicMock()
    transactions.create("fake-link-uuid", "2019-01-01")

    transactions.session.post.assert_called_with(
        "/api/transactions/",
        data={"link": "fake-link-uuid", "date_from": "2019-01-01", "date_to": "2019-02-28"},
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
            "encryption_key": "fake-key",
        },
    )


def test_accounts_create_sends_encryption_key_if_given(jwt_session):
    accounts = Accounts(jwt_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", encryption_key="fake-key")

    accounts.session.post.assert_called_with(
        "/api/accounts/", data={"link": "fake-link-uuid", "encryption_key": "fake-key"}
    )


def test_accounts_create_token_if_given(jwt_session):
    accounts = Accounts(jwt_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", token="fake-token")

    accounts.session.post.assert_called_with(
        "/api/accounts/", data={"link": "fake-link-uuid", "token": "fake-token"}
    )


def test_owners_create_sends_encryption_key_if_given(jwt_session):
    owners = Owners(jwt_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", encryption_key="fake-key")

    owners.session.post.assert_called_with(
        "/api/owners/", data={"link": "fake-link-uuid", "encryption_key": "fake-key"}
    )


def test_owners_create_token_if_given(jwt_session):
    owners = Owners(jwt_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", token="fake-token")

    owners.session.post.assert_called_with(
        "/api/owners/", data={"link": "fake-link-uuid", "token": "fake-token"}
    )
