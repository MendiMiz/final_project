from app_data.db.psql.database import session_maker
from app_data.db.psql.models import Event, Location, City
from sqlalchemy.exc import SQLAlchemyError


def insert_model(model):
    with session_maker() as session:
        try:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model.id
        except SQLAlchemyError as e:
            session.rollback()
            print("Failed to insert: " + str(e))

def insert_location(location):
    with session_maker() as session:
        location_existing = session.query(Location).filter(Location.city_id == location.city_id).first()
        if location_existing:
            return location_existing.id
        else:
            try:
                session.add(location)
                session.commit()
                session.refresh(location)
                return location.id
            except SQLAlchemyError as e:
                session.rollback()
                print("Failed to insert: " + str(e))

def insert_city(city):
    with session_maker() as session:
        location_existing = session.query(City).filter(City.lat == city.lat).first()
        if location_existing:
            return city.id
        else:
            try:
                session.add(city)
                session.commit()
                session.refresh(city)
                return city.id
            except SQLAlchemyError as e:
                session.rollback()
                print("Failed to insert: " + str(e))


