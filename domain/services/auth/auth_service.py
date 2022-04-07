from fastapi import HTTPException
from fastapi.responses import JSONResponse

from core.schemas import AuthDetails
from auth.auth import AuthHandler


auth_handler = AuthHandler()


async def login(auth_details: AuthDetails):
    hardcoded_username = "admin"
    hardcoded_password = "admin"

    if all(
        [
            auth_details.username == hardcoded_username,
            auth_handler.verify_password(auth_details.password, hardcoded_password)
        ]
    ):
        token = auth_handler.encode_token(hardcoded_username)
        return JSONResponse(content={'access_token': token})

    raise HTTPException(status_code=401, detail='Invalid username and/or password')
