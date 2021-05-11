from unittest.mock import MagicMock, patch

import pytest

from belvo import resources
from belvo.enums import AccessMode


def test_links_create_sends_token_if_given(api_session):
    link = resources.Links(api_session)
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
        raise_exception=False,
    )


@pytest.mark.parametrize("mode", [AccessMode.RECURRENT, AccessMode.SINGLE])
def test_links_create_can_set_access_mode(api_session, mode):
    link = resources.Links(api_session)
    link.session.post = MagicMock()

    link.create("fake-bank", "fake-user", "fake-password", access_mode=mode)

    link.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "save_data": True,
            "access_mode": mode.value,
        },
        raise_exception=False,
    )


def test_links_create_sends_encryption_key_if_given(api_session):
    links = resources.Links(api_session)
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
        raise_exception=False,
    )


def test_links_create_sends_username2_if_given(api_session):
    links = resources.Links(api_session)
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
        },
        raise_exception=False,
    )


def test_links_create_sends_username3_if_given(api_session):
    links = resources.Links(api_session)
    links.session.post = MagicMock()
    links.create(
        "fake-bank",
        "fake-user",
        "fake-password",
        username2="fake-user-two",
        username3="fake-user-three",
    )

    links.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "username2": "fake-user-two",
            "username3": "fake-user-three",
            "password": "fake-password",
            "save_data": True,
        },
        raise_exception=False,
    )


def test_links_create_sends_password2_if_given(api_session):
    links = resources.Links(api_session)
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
        },
        raise_exception=False,
    )


def test_links_create_sends_username_type_if_given(api_session):
    links = resources.Links(api_session)
    links.session.post = MagicMock()
    links.create("fake-bank", "fake-user", "fake-password", username_type="001")

    links.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "save_data": True,
            "username_type": "001",
        },
        raise_exception=False,
    )


def test_links_create_with_key_cert(api_session):
    with patch("belvo.resources.links.read_file_to_b64") as mocked_b64:
        mocked_b64.return_value = "123b64file123"
        links = resources.Links(api_session)
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
                "certificate": "123b64file123",
                "private_key": "123b64file123",
            },
            raise_exception=False,
        )


def test_links_update_password(api_session):
    link = resources.Links(api_session)
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


@pytest.mark.parametrize("external_id", ["abc", "test@mail.com"])
def test_links_create_with_external_id(api_session, external_id):
    link = resources.Links(api_session)
    link.session.post = MagicMock()

    link.create("fake-bank", "fake-user", "fake-password", external_id=external_id)

    link.session.post.assert_called_with(
        "/api/links/",
        data={
            "institution": "fake-bank",
            "username": "fake-user",
            "password": "fake-password",
            "external_id": external_id,
            "save_data": True,
        },
        raise_exception=False,
    )
