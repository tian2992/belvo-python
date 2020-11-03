from unittest.mock import MagicMock

from freezegun import freeze_time

from belvo import resources


@freeze_time("2019-02-28T12:00:00Z")
def test_balances_create_sets_current_time_if_no_date_given(api_session):
    balances = resources.Balances(api_session)
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
    balances = resources.Balances(api_session)
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
    balances = resources.Balances(api_session)
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
    balances = resources.Balances(api_session)
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
