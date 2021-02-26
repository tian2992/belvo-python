from unittest.mock import MagicMock

from belvo import resources


def test_access_token_create(api_session):
    token = resources.WidgetToken(api_session)
    token.session.post = MagicMock()
    token.create()

    token.session.post.assert_called_with(
        "/api/token/",
        data={
            "id": "monty",
            "password": "python",
            "scopes": "read_institutions,write_links,read_links",
        },
        raise_exception=False,
    )


def test_link_token(api_session):
    link = resources.Links(api_session)
    link.session.post = MagicMock()
    link.token(link="fake-link-uuid", scopes="read_links,write_links")

    link.session.post.assert_called_with(
        "/api/token/",
        data={
            "id": "monty",
            "password": "python",
            "scopes": "read_links,write_links",
            "link_id": "fake-link-uuid",
        },
        raise_exception=False,
    )


def test_widget_token(api_session):
    link = resources.Links(api_session)
    link.session.post = MagicMock()
    widget = {
        "branding": {
            "company_logo": "https://acme.corp/fancy_logo.bmp",
            "company_color": "#eb34e1",
            "company_benefit_header": "Lorem ipsum",
            "company_benefit_content": "Lorem ipsum",
            "opportunity_loss": "Lorem ipsum",
            "company_name": "Acme Corp. SL",
        }
    }
    link.token(link="fake-link-uuid", scopes="read_links,write_links", widget=widget)
    link.session.post.assert_called_with(
        "/api/token/",
        data={
            "id": "monty",
            "password": "python",
            "scopes": "read_links,write_links",
            "link_id": "fake-link-uuid",
            "widget": {
                "branding": {
                    "company_logo": "https://acme.corp/fancy_logo.bmp",
                    "company_color": "#eb34e1",
                    "company_benefit_header": "Lorem ipsum",
                    "company_benefit_content": "Lorem ipsum",
                    "opportunity_loss": "Lorem ipsum",
                    "company_name": "Acme Corp. SL",
                }
            },
        },
        raise_exception=False,
    )
