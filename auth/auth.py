import os

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class AuthHandler:
    _security = HTTPBearer()
    _secret_key = os.environ["SECRET_KEY"]

    @staticmethod
    def verify_password(password_str, password_str_compare):
        return password_str == password_str_compare

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=60),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        print("hej")
        return jwt.encode(
            payload,
            self._secret_key,
            algorithm="HS256"
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(_security)):
        return self.decode_token(auth.credentials)
