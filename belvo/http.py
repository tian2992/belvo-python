import logging
from typing import Dict, Generator, List, Union

from requests import HTTPError, Session

logger = logging.getLogger(__name__)


class JWTSession:
    def __init__(self, url: str) -> None:
        self._url = url
        self._username = None
        self._password = None
        self._access_token = None
        self._refresh_token = None
        self._session = Session()

    @property
    def url(self) -> str:
        return self._url

    @property
    def username(self) -> str:
        return self._username

    @property
    def session(self) -> Session:
        return self._session

    @property
    def headers(self) -> Dict:
        return self.session.headers

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    def set_tokens(self, access: str, refresh: str) -> None:
        self._access_token = access
        self._refresh_token = refresh

    def login(self, username: str, password: str) -> bool:
        auth_url = "{}/api/token/".format(self.url)
        r = self.session.post(
            auth_url, data={"username": username, "password": password}, timeout=5
        )
        try:
            r.raise_for_status()
        except HTTPError:
            return False
        tokens = r.json()
        self.set_tokens(**tokens)
        self.session.headers.update({"Authorization": "Bearer {}".format(self.access_token)})
        return True

    def _get(self, url: str, params: Dict = None) -> Union[List, Dict]:
        if params is None:
            params = {}

        r = self.session.get(url=url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def get(self, endpoint: str, id: str, params: Dict = None) -> Dict:
        url = "{}{}{}/".format(self.url, endpoint, id)
        return self._get(url=url, params=params)

    def list(self, endpoint: str, params: Dict = None) -> Generator:
        url = "{}{}".format(self.url, endpoint)
        while True:
            data = self._get(url, params=params)
            for result in data["results"]:
                yield result

            if not data["next"]:
                break

            url = data["next"]
            params = None

    def post(self, endpoint: str, data: Dict, *args, **kwargs) -> Union[List, Dict]:
        url = "{}{}".format(self.url, endpoint)
        r = self.session.post(url=url, data=data, *args, **kwargs)
        return r.json()

    def delete(self, endpoint: str, id: str) -> bool:
        url = "{}{}{}/".format(self.url, endpoint, id)
        r = self.session.delete(url, timeout=10)
        try:
            r.raise_for_status()
        except HTTPError:
            return False
        return True
