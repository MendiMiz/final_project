from sqlalchemy import Column, Integer, String
from app_data.db.psql.models import Base


class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    region_name =  Column(String(100), nullable=False)



    def __repr__(self):
        return (
            f"<Region(id={self.id}, region_name='{self.region_name}')>"
        )
