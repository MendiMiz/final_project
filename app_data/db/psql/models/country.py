from sqlalchemy import Column, Integer, String
from app_data.db.psql.models import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name =  Column(String(100), nullable=False)



    def __repr__(self):
        return (
            f"<Country(id={self.id}, city_name='{self.country_name}')>"
        )
