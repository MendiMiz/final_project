from sqlalchemy import Column, Integer, String
from app_data.db.psql.models import Base

class AttackType(Base):
    __tablename__ = "attack_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    attack_type_name = Column(String(200), unique=True, nullable=False)



    def __repr__(self):
        return (f"attack_type_id={self.id}, "
                f"attack_type_name={self.attack_type_name}")