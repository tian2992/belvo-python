from unittest.mock import MagicMock

from belvo import resources


def test_incomes_create(api_session):
    incomes = resources.Incomes(api_session)
    incomes.session.post = MagicMock()
    incomes.create("fake-link-uuid")
    incomes.session.post.assert_called()
    incomes.session.post.assert_called_with(
        "/api/incomes/", data={"link": "fake-link-uuid", "save_data": True}, raise_exception=False
    )


def test_income_resume(api_session):
    incomes = resources.Incomes(api_session)
    incomes.session.patch = MagicMock()
    incomes.resume("fake-session", "fake-token")

    incomes.session.patch.assert_called_with(
        "/api/incomes/",
        data={"session": "fake-session", "token": "fake-token"},
        raise_exception=False,
    )
