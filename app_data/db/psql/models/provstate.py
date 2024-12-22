from sqlalchemy import Column, Integer, String
from app_data.db.psql.models import Base


class ProvState(Base):
    __tablename__ = 'prov_states'

    id = Column(Integer, primary_key=True, autoincrement=True)
    prov_state_name =  Column(String(100), nullable=True)



    def __repr__(self):
        return (
            f"<ProvState(id={self.id}, prov_state_name='{self.prov_state_name}')>"
        )

