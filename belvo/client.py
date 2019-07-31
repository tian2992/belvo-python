import os

from .exceptions import BelvoAPIException
from .http import JWTSession
from .resources import Links, Accounts, Transactions


class Client:
    def __init__(self, username: str, password: str, url: str = None):
        if url is None:
            url = os.getenv("BELVO_API_URL")

        if not url:
            raise BelvoAPIException("You need to provide a URL.")

        self.session = JWTSession(url)
        self.session.login(username, password)

        self._links = Links(self.session)
        self._accounts = Accounts(self.session)
        self._transactions = Transactions(self.session)

    @property
    def Links(self):
        return self._links

    @property
    def Accounts(self):
        return self._accounts

    @property
    def Transactions(self):
        return self._transactions
