from sqlalchemy import Column, Integer, ForeignKey
from app_data.db.psql.models import Base


class AttackTypeEvent(Base):
    __tablename__ = 'attack_type_event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    attack_type_id = Column(Integer, ForeignKey('attack_types.id'))


    def __repr__(self):
        return (
            f"<AttackTypeEvent(id={self.id}, event_id={self.event_id}, attack_type_id={self.attack_type_id})>"
        )
