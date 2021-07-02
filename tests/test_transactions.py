from unittest.mock import MagicMock

from freezegun import freeze_time

from belvo import resources


@freeze_time("2019-02-28T12:00:00Z")
def test_transactions_create_sets_current_time_if_no_date_given(api_session):
    transactions = resources.Transactions(api_session)
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
    transactions = resources.Transactions(api_session)
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
    transactions = resources.Transactions(api_session)
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
