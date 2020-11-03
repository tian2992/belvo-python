from unittest.mock import MagicMock

from belvo import resources


def test_owners_create_sends_encryption_key_if_given(api_session):
    owners = resources.Owners(api_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", encryption_key="fake-key")

    owners.session.post.assert_called_with(
        "/api/owners/",
        data={"link": "fake-link-uuid", "save_data": True, "encryption_key": "fake-key"},
        raise_exception=False,
    )


def test_owners_create_token_if_given(api_session):
    owners = resources.Owners(api_session)
    owners.session.post = MagicMock()
    owners.create("fake-link-uuid", token="fake-token")

    owners.session.post.assert_called_with(
        "/api/owners/",
        data={"link": "fake-link-uuid", "save_data": True, "token": "fake-token"},
        raise_exception=False,
    )
