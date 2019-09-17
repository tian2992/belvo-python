from typing import Dict, Generator, TypeVar

JWTSession = TypeVar("JWTSession")


class Resource:
    endpoint = None

    def __init__(self, session: JWTSession) -> None:
        self._session = session

    @property
    def session(self) -> JWTSession:
        return self._session

    def create(self, *args, **kwargs) -> Dict:
        raise NotImplementedError()

    def list(self, **kwargs) -> Generator:
        endpoint = self.endpoint
        return self.session.list(endpoint, params=kwargs)

    def get(self, id: str, **kwargs) -> Dict:
        return self.session.get(self.endpoint, id, params=kwargs)

    def delete(self, id: str) -> bool:
        return self.session.delete(self.endpoint, id)

    def resume(self, session: str, token: str, *, link: str = None, **kwargs) -> Dict:
        data = {"session": session, "token": token, "link": link}
        return self.session.patch(self.endpoint, data=data, **kwargs)


class Links(Resource):
    endpoint = "/api/links/"

    def create(
        self,
        institution: str,
        username: str,
        password: str,
        *,
        token: str = None,
        secret: str = None
    ) -> Dict:
        data = {"institution": institution, "username": username, "password": password}

        if token:
            data.update(token=token)

        if secret:
            data.update(secret=secret)

        return self.session.post(self.endpoint, data)


class Accounts(Resource):
    endpoint = "/api/accounts/"

    def create(self, link: str, **kwargs):
        return self.session.post(self.endpoint, data={"link": link}, **kwargs)


class Transactions(Resource):
    endpoint = "/api/transactions/"

    def create(self, link: str, date_from: str, date_to: str, *, account: str = None, **kwargs):
        data = {"link": link, "date_from": date_from}

        if date_to:
            data.update(date_to=date_to)

        if account:
            data.update(account=account)

        return self.session.post(self.endpoint, data=data, **kwargs)


class Institutions(Resource):
    endpoint = "/api/institutions/"

    def delete(self, id: str) -> bool:
        raise NotImplementedError()

    def resume(self, session: str, token: str, *, link: str = None, **kwargs) -> Dict:
        raise NotImplementedError()
