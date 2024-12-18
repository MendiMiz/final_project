from sqlalchemy import Column, Integer, String
from app_data.db.psql.models import Base

class TargetType(Base):
    __tablename__ = "target_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_type_name = Column(String(200), unique=True, nullable=False)



    def __repr__(self):
        return (f"target_type_id={self.id}, "
                f"target_type_name={self.target_type_name}")