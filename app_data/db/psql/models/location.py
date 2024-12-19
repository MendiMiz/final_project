from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app_data.db.psql.models import Base


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))
    prov_state_id = Column(Integer, ForeignKey('prov_states.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))


    def __repr__(self):
        return (
            f"<Location(id={self.id}, region_id={self.region_id}, prov_state_id={self.prov_state_id},"
            f"country_id={self.country_id}, city_id={self.city_id}>)>"
        )

