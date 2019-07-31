import logging
from typing import Dict, Generator, Union, List

from requests import Session, HTTPError

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
        auth_url = f"{self.url}/api/token/"
        r = self.session.post(
            auth_url, data={"username": username, "password": password}, timeout=5
        )
        try:
            r.raise_for_status()
        except HTTPError as exc:
            logger.exception("Login failed.", exc_info=exc)
            return False
        tokens = r.json()
        self.set_tokens(**tokens)
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        return True

    def _get_page(self, url: str, params: Dict = None) -> Union[List, Dict]:
        if params is None:
            params = {}

        r = self.session.get(url=url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def get(self, endpoint: str, params: Dict = None) -> Generator:
        url = f"{self.url}{endpoint}"
        while True:
            data = self._get_page(url, params=params)
            for result in data["results"]:
                yield result

            if not data["next"]:
                break

            url = data["next"]
            params = None

    def post(self, endpoint: str, data: Dict, *args, **kwargs) -> Union[List, Dict]:
        url = f"{self.url}{endpoint}"
        r = self.session.post(url=url, data=data, *args, **kwargs)
        return r.json()

    def delete(self, endpoint: str, resource_id: str) -> bool:
        url = f"{self.url}{endpoint}/{resource_id}/"
        r = self.session.delete(url, timeout=10)
        try:
            r.raise_for_status()
        except HTTPError:
            return False
        return True
