from app_data.db.psql.database import session_maker
from app_data.db.psql.models import Location, City, Country
from sqlalchemy.exc import SQLAlchemyError


def get_all_countries_from_db():
    with session_maker() as session:
        countries = session.query(Country).all()
        countries_names = [country.country_name for country in countries]
        return countries_names




def insert_entities_bulk(entity_class, entity_names, key_column):
    entity_dict = {}

    with session_maker() as session:
        try:
            existing_entities = session.query(
                getattr(entity_class, key_column), entity_class.id
            ).all()
            existing_entity_names = {
                name: eid for name, eid in existing_entities
            }

            entities_to_insert = [
                name for name in entity_names if name not in existing_entity_names
            ]

            if entities_to_insert:
                new_entities = [
                    entity_class(**{key_column: name}) for name in entities_to_insert
                ]
                session.add_all(new_entities)
                session.commit()

                for entity in new_entities:
                    session.refresh(entity)
                    entity_dict[getattr(entity, key_column)] = entity.id

            entity_dict.update(existing_entity_names)

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Failed to insert {entity_class.__name__} entities in bulk: {str(e)}")

    return entity_dict


def insert_cities_bulk(cities):

    city_dict = {}

    with session_maker() as session:
        existing_cities = session.query(City.city_name, City.lat, City.lon, City.id).all()
        existing_city_names = {
            (city_name, lat, lon): city_id
            for city_name, lat, lon, city_id in existing_cities
        }

        cities_to_insert = [
            city for city in cities
            if (city["city_name"], city["lat"], city["lon"]) not in existing_city_names
        ]

        if cities_to_insert:
            try:
                session.add_all([
                    City(city_name=city["city_name"], lat=city["lat"], lon=city["lon"])
                    for city in cities_to_insert
                ])
                session.commit()

                for city in cities_to_insert:
                    city_id = session.query(City).filter_by(city_name=city["city_name"], lat=city["lat"], lon=city["lon"]).first().id
                    city_dict[city["city_name"]] = city_id
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Failed to insert cities in bulk: {e}")

        for (city_name, lat, lon), city_id in existing_city_names.items():
            city_dict[city_name] = city_id

    return city_dict





def insert_location_bulk(locations):
    with session_maker() as session:
        existing_locations = session.query(Location.city_id, Location.id).all()
        existing_location_ids = {location.city_id: location.id for location in existing_locations}

        locations_to_insert = [loc for loc in locations if loc.city_id not in existing_location_ids]

        if locations_to_insert:
            try:
                session.add_all(locations_to_insert)
                session.commit()
                for location in locations_to_insert:
                    session.refresh(location)
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Failed to insert locations in bulk: {e}")

        updated_existing_locations = session.query(Location.city_id, Location.id).all()
        updated_existing_location_ids = {location.city_id: location.id for location in updated_existing_locations}
        location_ids_list = [updated_existing_location_ids[loc.city_id] for loc in locations]

    return location_ids_list


def insert_event_bulk(events):
    event_dict = {}
    with session_maker() as session:
        try:
            session.add_all(events)
            session.commit()
            for event in events:
                session.refresh(event)
                event_dict[event.id] = event.id
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Failed to insert events in bulk: {e}")
    return event_dict


def insert_event_group_bulk(event_groups):
    with session_maker() as session:
        try:
            session.add_all(event_groups)
            session.commit()
            for event_group in event_groups:
                session.refresh(event_group)
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Failed to insert event groups in bulk: {e}")

def insert_target_type_event_bulk(target_type_events):
    with session_maker() as session:
        try:
            session.add_all(target_type_events)
            session.commit()
            for target_type_event in target_type_events:
                session.refresh(target_type_event)
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Failed to insert target type events in bulk: {e}")


def insert_attack_type_event_bulk(attack_type_events):
    with session_maker() as session:
        try:
            session.add_all(attack_type_events)
            session.commit()
            for attack_type_event in attack_type_events:
                session.refresh(attack_type_event)
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Failed to insert attack type events in bulk: {e}")

