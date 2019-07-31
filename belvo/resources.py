from typing import TypeVar, Dict, Generator

JWTSession = TypeVar("JWTSession")


class Resource:
    endpoint = None

    def __init__(self, session: JWTSession) -> None:
        self._session = session

    @property
    def session(self) -> JWTSession:
        return self._session

    def get(self, params: Dict = None) -> Generator:
        if params is None:
            params = {}

        return self.session.get(self.endpoint, params=params)

    def delete(self, id: str) -> bool:
        return self.session.delete(self.endpoint, id)


class Links(Resource):
    endpoint = "/api/links/"

    def create(self, institution: str, username: str, password: str, token: str = None) -> Dict:
        data = {"institution": institution, "username": username, "password": password}
        if token:
            data.update(token=token)

        return self.session.post(self.endpoint, data)


class Accounts(Resource):
    endpoint = "/api/accounts/"

    def create(self, link_uuid: str, belvo_token: str):
        return self.session.post(
            self.endpoint, data={"link": link_uuid, "belvo_token": belvo_token}, timeout=60
        )


class Transactions(Resource):
    endpoint = "/api/transactions/"

    def create(
        self,
        link_uuid: str,
        belvo_token: str,
        date_from: str,
        date_to: str,
        account_uuid: str = None,
    ):
        data = {"link": link_uuid, "belvo_token": belvo_token, "date_from": date_from}

        if date_to:
            data.update(date_to=date_to)

        if account_uuid:
            data.update(account=account_uuid)

        return self.session.post(self.endpoint, data=data, timeout=60)
