from app_data.db.psql.database import session_maker
from app_data.db.psql.models import Event, Location, City, Country, Region
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
        if city.lat:
            city_existing = session.query(City).filter(City.lat == city.lat).first()
        else:
            city_existing = session.query(City).filter(City.city_name == city.city_name).first()
        if city_existing:
          return city_existing.id
        else:
            try:
                session.add(city)
                session.commit()
                session.refresh(city)
                return city.id
            except SQLAlchemyError as e:
                session.rollback()
                print("Failed to insert: " + str(e))

def insert_country(country):
    with session_maker() as session:
        country_existing = session.query(Country).filter(Country.country_name == country.country_name).first()
        if country_existing:
          return country_existing.id
        else:
            try:
                session.add(country)
                session.commit()
                session.refresh(country)
                return country.id
            except SQLAlchemyError as e:
                session.rollback()
                print("Failed to insert: " + str(e))

def insert_region(region):
    with session_maker() as session:
        region_existing = session.query(Region).filter(Region.region_name == region.region_name).first()
        if region_existing:
          return region_existing.id
        else:
            try:
                session.add(region)
                session.commit()
                session.refresh(region)
                return region.id
            except SQLAlchemyError as e:
                session.rollback()
                print("Failed to insert: " + str(e))
