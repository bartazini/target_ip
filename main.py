from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import core.schemas as schemas
from auth.auth import AuthHandler
import domain.services.auth.auth_service as auth_service
import domain.services.ip_crud.ip_crud_service as ip_crud_service

from core.db_conf import get_db

app = FastAPI()


origins = [
    "https://target-ip.herokuapp.com/",
    "http://127.0.0.1/",
    "http://0.0.0.0/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


auth_handler = AuthHandler()


@app.get("/")
async def home():
    return {"message": "Hello World!"}


@app.post("/login")
async def login(auth_details: schemas.AuthDetails):
    return await auth_service.login(auth_details=auth_details)


@app.get("/get_ip_location/{ip_address}", dependencies=[Depends(auth_handler.auth_wrapper)])
async def get_ip_location(ip_address: str, db: Session = Depends(get_db)) -> JSONResponse:
    return await ip_crud_service.get_ip_location(ip_address=ip_address, db=db)


@app.post("/add_ip_location", dependencies=[Depends(auth_handler.auth_wrapper)])
async def add_ip_location(
        ip_address: schemas.AddIpLocation,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await ip_crud_service.add_ip_location(ip_address=ip_address.ip_address, db=db)


@app.delete("/delete_ip_location", dependencies=[Depends(auth_handler.auth_wrapper)])
async def delete_ip_location(
        ip_address: schemas.DeleteIpLocation,
        db: Session = Depends(get_db)
) -> JSONResponse:
    return await ip_crud_service.delete_ip_location(ip_address=ip_address.ip_address, db=db)
