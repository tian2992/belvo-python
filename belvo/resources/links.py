from typing import Dict, List, Union

from belvo.enums import AccessMode
from belvo.resources.base import Resource
from belvo.utils import read_file_to_b64


class Links(Resource):
    endpoint = "/api/links/"

    def create(
        self,
        institution: str,
        username: str,
        password: str,
        *,
        username2: str = None,
        password2: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        access_mode: AccessMode = AccessMode.SINGLE,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
    ) -> Union[List[Dict], Dict]:

        data = {
            "institution": institution,
            "username": username,
            "password": password,
            "save_data": save_data,
            "access_mode": access_mode.value,
        }

        if username2:
            data.update(username2=username2)

        if password2:
            data.update(password2=password2)

        if token:
            data.update(token=token)

        if encryption_key:
            data.update(encryption_key=encryption_key)

        if username_type:
            data.update(username_type=username_type)

        if certificate:
            data.update(certificate=read_file_to_b64(certificate))

        if private_key:
            data.update(private_key=read_file_to_b64(private_key))

        return self.session.post(self.endpoint, data=data, raise_exception=raise_exception)

    def update(
        self,
        link: str,
        *,
        password: str = None,
        password2: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        raise_exception: bool = False,
        username_type: str = None,
        certificate: str = None,
        private_key: str = None,
    ) -> Union[List[Dict], Dict]:

        data = {"password": password, "save_data": save_data}

        if password:
            data.update(password=password)

        if password2:
            data.update(password2=password2)

        if token:
            data.update(token=token)

        if encryption_key:
            data.update(encryption_key=encryption_key)

        if username_type:
            data.update(username_type=username_type)

        if certificate:
            data.update(certificate=read_file_to_b64(certificate))

        if private_key:
            data.update(private_key=read_file_to_b64(private_key))

        return self.session.put(self.endpoint, id=link, data=data, raise_exception=raise_exception)

    def token(
        self, link: str, scopes: str, *, raise_exception: bool = False
    ) -> Union[List[Dict], Dict]:
        data = {"scopes": scopes}
        return self.session.post(
            f"{self.endpoint}{link}/token/", data=data, raise_exception=raise_exception
        )
