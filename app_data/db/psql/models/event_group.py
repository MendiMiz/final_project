from sqlalchemy import Column, Integer, ForeignKey
from app_data.db.psql.models import Base


class EventGroup(Base):
    __tablename__ = 'event-group'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

    def __repr__(self):
        return (
            f"<EventGroup(id={self.id}, event_id={self.event_id}, group_id={self.group_id})>"
        )
