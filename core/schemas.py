from pydantic import BaseModel


class AuthDetails(BaseModel):
    username: str = "admin"
    password: str = "admin"


class GetIpLocation(BaseModel):
    ip_address: str


class AddIpLocation(GetIpLocation):
    pass


class DeleteIpLocation(GetIpLocation):
    pass
