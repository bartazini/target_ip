import requests

from domain.services.ip_crud.exception import IpStackError


class IpStack:
    __access_key = "11b99a9b1c0a3b3ac981cca0b896697f"

    def __init__(self):
        self._base_api_url = "http://api.ipstack.com/{}?access_key={}"

    @classmethod
    def from_ip_stack(cls):
        return cls()

    def get_ip_location_details(self, ip_address: str):
        api_endpoint = self._base_api_url.format(ip_address, self.__access_key)

        response = requests.get(
            url=api_endpoint,
        )

        if response.ok:
            return response.json()

        raise IpStackError("Could not get valid response from IpStack API. Probably server is down.")
