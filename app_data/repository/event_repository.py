from app_data.db.psql.database import session_maker
from app_data.db.psql.models import Event, Location, City, Country, Region, ProvState, TargetType, EventGroup, \
    TargetTypeEvent, Group
from sqlalchemy.exc import SQLAlchemyError

from app_data.db.psql.models.attack_type import AttackType
from app_data.db.psql.models.attack_type_event import AttackTypeEvent


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









def insert_event_group(event_group: EventGroup):
    with session_maker() as session:
        existing_event_group = session.query(EventGroup).filter_by(
            event_id=event_group.event_id
        ).filter_by(
            group_id=event_group.group_id
        ).first()

        if existing_event_group:
            print(f"Event {event_group.event_id} and Group {event_group.group_id} relationship already exists.")
            return existing_event_group.id
        else:
            session.add(event_group)
            session.commit()
            session.refresh(event_group)
            return event_group.id


def insert_target_type_event(target_type_event: TargetTypeEvent):
    with session_maker() as session:
        existing_target_type_event = session.query(TargetTypeEvent).filter_by(
            event_id=target_type_event.event_id
        ).filter_by(
            target_type_id=target_type_event.target_type_id
        ).first()

        if existing_target_type_event:
            print(f"Event {target_type_event.event_id} and TargetType {target_type_event.target_type_id} relationship already exists.")
            return existing_target_type_event.id
        else:
            session.add(target_type_event)
            session.commit()
            session.refresh(target_type_event)
            return target_type_event.id



def insert_attack_type_event(attack_type_event: AttackTypeEvent):
    with session_maker() as session:
        existing_target_type_event = session.query(TargetTypeEvent).filter_by(
            event_id=attack_type_event.event_id
        ).filter_by(
            target_type_id=attack_type_event.attack_type_id
        ).first()

        if existing_target_type_event:
            print(f"Event {attack_type_event.event_id} and TargetType {attack_type_event.attack_type_id} relationship already exists.")
            return existing_target_type_event.id
        else:
            session.add(attack_type_event)
            session.commit()
            session.refresh(attack_type_event)
            return attack_type_event.id




def insert_entities_bulk(entity_class, entity_names, key_column):
    """
    Generic bulk insert function for entities like Region and ProvState.

    :param entity_class: The SQLAlchemy model class (e.g., Region, ProvState).
    :param entity_names: A list of names for the entities to insert.
    :param key_column: The attribute to filter and store the entity names (default is "name").
    :return: A dictionary with entity names as keys and their IDs as values.
    """
    entity_dict = {}

    with session_maker() as session:
        try:
            # Fetch all existing entities from the database
            existing_entities = session.query(
                getattr(entity_class, key_column), entity_class.id
            ).all()
            existing_entity_names = {
                name: eid for name, eid in existing_entities
            }

            # Prepare a list of new entities to insert
            entities_to_insert = [
                name for name in entity_names if name not in existing_entity_names
            ]

            # Insert new entities in bulk if there are any
            if entities_to_insert:
                new_entities = [
                    entity_class(**{key_column: name}) for name in entities_to_insert
                ]
                session.add_all(new_entities)
                session.commit()

                # Fetch newly added entities' IDs
                for entity in new_entities:
                    session.refresh(entity)  # Ensure the ID is available after insertion
                    entity_dict[getattr(entity, key_column)] = entity.id

            # Add existing entities to the dictionary
            entity_dict.update(existing_entity_names)

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Failed to insert {entity_class.__name__} entities in bulk: {str(e)}")

    return entity_dict

