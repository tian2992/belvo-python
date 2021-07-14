from typing import Dict, List, Union

from belvo.resources.base import Resource


class TaxComplianceStatus(Resource):
    endpoint = "/api/tax-compliance-status/"

    def create(
        self,
        link: str,
        *,
        attach_pdf: bool = False,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:

        data = {"link": link, "attach_pdf": attach_pdf, "save_data": save_data}

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Dict:
        raise NotImplementedError()
