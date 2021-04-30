from unittest.mock import MagicMock

from belvo import resources


def test_statements_create(api_session):
    statements = resources.Statements(api_session)
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
            "encryption_key": "fake-key",
        },
        raise_exception=False,
    )


def test_statements_resume(api_session):
    statements = resources.Statements(api_session)
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
