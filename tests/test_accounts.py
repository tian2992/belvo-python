from unittest.mock import MagicMock

from belvo import resources


def test_accounts_create_sends_encryption_key_if_given(api_session):
    accounts = resources.Accounts(api_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", encryption_key="fake-key")

    accounts.session.post.assert_called_with(
        "/api/accounts/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
        raise_exception=False,
    )


def test_accounts_create_token_if_given(api_session):
    accounts = resources.Accounts(api_session)
    accounts.session.post = MagicMock()
    accounts.create("fake-link-uuid", token="fake-token")

    accounts.session.post.assert_called_with(
        "/api/accounts/",
        data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"},
        raise_exception=False,
    )


def test_account_resume(api_session):
    accounts = resources.Accounts(api_session)
    accounts.session.patch = MagicMock()
    accounts.resume("fake-session", "fake-token")

    accounts.session.patch.assert_called_with(
        "/api/accounts/",
        data={"session": "fake-session", "token": "fake-token"},
        raise_exception=False,
    )
