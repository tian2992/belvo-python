from belvo.resources.base import Resource


class WidgetToken(Resource):
    endpoint = "/api/token/"

    def create(self, *, raise_exception: bool = False):
        data = {
            "id": self.session._secret_key_id,
            "password": self.session._secret_key_password,
            "scopes": "read_institutions,write_links,read_links,delete_links",
        }
        return self.session.post(self.endpoint, data=data, raise_exception=raise_exception)
