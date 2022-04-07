from sqlalchemy import Column, Integer, String

from core.db_conf import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    geo_location_details = Column(String)
