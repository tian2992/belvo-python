import os

from .exceptions import BelvoAPIException
from .http import JWTSession
from .resources import Accounts, Institutions, Links, Transactions


class Client:
    def __init__(self, username: str, password: str, url: str = None):
        if url is None:
            url = os.getenv("BELVO_API_URL")

        if not url:
            raise BelvoAPIException("You need to provide a URL.")

        self.session = JWTSession(url)

        if not self.session.login(username, password):
            raise BelvoAPIException("Login failed")

        self._links = Links(self.session)
        self._accounts = Accounts(self.session)
        self._transactions = Transactions(self.session)
        self._institutions = Institutions(self.session)

    @property
    def Links(self):
        return self._links

    @property
    def Accounts(self):
        return self._accounts

    @property
    def Transactions(self):
        return self._transactions

    @property
    def Institutions(self):
        return self._institutions
