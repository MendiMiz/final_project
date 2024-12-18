from sqlalchemy import Column, Integer, String
from app_data.db.psql.models import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return (
            f"<Group(id={self.id}, course_name='{self.name}')>"
        )
