from sqlalchemy import Column, Integer, ForeignKey
from app_data.db.psql.models import Base


class TargetTypeEvent(Base):
    __tablename__ = 'target_type_event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    target_type_id = Column(Integer, ForeignKey('target_types.id'))


    def __repr__(self):
        return (
            f"<TargetTypeEvent(id={self.id}, event_id={self.event_id}, target_type_id={self.target_type_id})>"
        )
