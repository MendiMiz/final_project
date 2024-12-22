from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app_data.db.psql.models import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name =  Column(String(100), nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"<City(id={self.id}, city_name='{self.city_name}, lat={self.lat}, lon={self.lon})>"
        )
