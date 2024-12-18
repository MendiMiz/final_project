from sqlalchemy import Column, Integer, ForeignKey
from app_data.db.psql.models import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    killed = Column(Integer)
    injured = Column(Integer)
    terrorist_num = Column(Integer)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

    def __repr__(self):
        return (
            f"<Event(id={self.id}, location_id={self.location_id}, killed={self.killed}, injured={self.injured}, "
            f"terrorist_num={self.terrorist_num}, year={self.year}, month={self.month}, day={self.day})>"
        )
