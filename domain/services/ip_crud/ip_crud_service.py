import json

from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse

from core.models import Address
from ip_stack.IpStack import IpStack


async def get_ip_location(ip_address: str, db: Session) -> JSONResponse:
    try:
        db_address = db.query(Address).filter(Address.address == ip_address).first()

    except Exception as e:
        return JSONResponse(
            content={"status": f"Critical database issue: {e.__class__.__name__}"}, status_code=500
        )

    if db_address:
        content = json.loads(db_address.geo_location_details)
        return JSONResponse(content=content, status_code=200)

    try:
        ip_address_location_details = await _get_ip_address_geolocation_details(ip_address=ip_address)

    except Exception as e:
        return JSONResponse(
            content={"status": f"Could not get geolocation data for: {ip_address} due to: {e.__class__.__name__}"}
        )

    return JSONResponse(content=ip_address_location_details, status_code=200)


async def add_ip_location(ip_address: str, db: Session) -> JSONResponse:
    try:
        db_address = db.query(Address).filter(Address.address == ip_address).first()

    except Exception as e:
        return JSONResponse(
            content={"status": f"Critical database issue: {e.__class__.__name__}"}, status_code=500
        )

    if db_address:
        return JSONResponse(content={"status": "Address already exists in database"}, status_code=200)

    try:
        ip_address_location_details = await _get_ip_address_geolocation_details(ip_address=ip_address)

    except Exception as e:
        return JSONResponse(
            content={"status": f"Could not get geolocation data for: {ip_address} due to: {e.__class__.__name__}"}
        )

    try:
        db_url = Address(
            address=ip_address,
            geo_location_details=json.dumps(ip_address_location_details)
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)

    except Exception as e:
        return JSONResponse(
            content={"status": f"Critical database issue due to: {e.__class__.__name__}"}, status_code=500
        )

    return JSONResponse(content=ip_address_location_details, status_code=201)


async def delete_ip_location(ip_address: str, db: Session) -> JSONResponse:
    try:
        db_address = db.query(Address).filter(Address.address == ip_address).first()

    except Exception as e:
        return JSONResponse(
            content={"status": f"Critical database issue due to: {e.__class__.__name__}"}, status_code=500
        )

    if not db_address:
        return JSONResponse(
            content={"status": f"It seems like address: '{ip_address}' does not exist in database"},
            status_code=200
        )

    try:
        db.query(Address).filter(Address.address == ip_address).delete()
        db.commit()

    except Exception as e:
        return JSONResponse(
            content={"status": f"Critical database issue: {e.__class__.__name__}"}, status_code=500
        )

    return JSONResponse(content={"status": "success"}, status_code=200)


async def _get_ip_address_geolocation_details(ip_address):
    return IpStack.from_ip_stack().get_ip_location_details(ip_address=ip_address)
