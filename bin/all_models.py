# from sqlalchemy import Column, Integer, String, ForeignKey, Float
# from app_data.db.psql.models import Base
#
# class AttackType(Base):
#     __tablename__ = "attack_types"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     attack_type_name = Column(String(200), unique=True, nullable=False)
#
#
#
#     def __repr__(self):
#         return (f"attack_type_id={self.id}, "
#                 f"attack_type_name={self.attack_type_name}")
#
#
# class AttackTypeEvent(Base):
#     __tablename__ = 'attack_type_event'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     event_id = Column(Integer, ForeignKey('events.id'))
#     attack_type_id = Column(Integer, ForeignKey('attack_types.id'))
#
#
#     def __repr__(self):
#         return (
#             f"<AttackTypeEvent(id={self.id}, event_id={self.event_id}, attack_type_id={self.attack_type_id})>"
#         )
#
# class City(Base):
#     __tablename__ = 'cities'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     city_name =  Column(String(100), nullable=True)
#     lat = Column(Float, nullable=True)
#     lon = Column(Float, nullable=True)
#
#     def __repr__(self):
#         return (
#             f"<City(id={self.id}, city_name='{self.city_name}, lat={self.lat}, lon={self.lon})>"
#         )
#
# class Country(Base):
#     __tablename__ = 'countries'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     country_name =  Column(String(100), nullable=False)
#
#
#
#     def __repr__(self):
#         return (
#             f"<Country(id={self.id}, city_name='{self.country_name}')>"
#         )
#
# class Event(Base):
#     __tablename__ = 'events'
#
#     id = Column(Integer, primary_key=True)
#     location_id = Column(Integer, ForeignKey('locations.id'))
#     killed = Column(Integer)
#     injured = Column(Integer)
#     terrorists_count = Column(Integer, nullable=True)
#     year = Column(Integer)
#     month = Column(Integer)
#     day = Column(Integer)
#
#     def __repr__(self):
#         return (
#             f"<Event(id={self.id}, location_id={self.location_id}, killed={self.killed}, injured={self.injured}, "
#             f"terrorist_num={self.terrorists_count}, year={self.year}, month={self.month}, day={self.day})>"
#         )
#
# class EventGroup(Base):
#     __tablename__ = 'event-group'
#
#     id = Column(Integer, primary_key=True)
#     event_id = Column(Integer, ForeignKey('events.id'))
#     group_id = Column(Integer, ForeignKey('groups.id'))
#
#     def __repr__(self):
#         return (
#             f"<EventGroup(id={self.id}, event_id={self.event_id}, group_id={self.group_id})>"
#         )
#
# class Group(Base):
#     __tablename__ = 'groups'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255), nullable=False)
#
#     def __repr__(self):
#         return (
#             f"<Group(id={self.id}, course_name='{self.name}')>"
#         )
#
# class Location(Base):
#     __tablename__ = 'locations'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     country_id = Column(Integer, ForeignKey('countries.id'))
#     region_id = Column(Integer, ForeignKey('regions.id'))
#     prov_state_id = Column(Integer, ForeignKey('prov_states.id'))
#     city_id = Column(Integer, ForeignKey('cities.id'))
#
#
#     def __repr__(self):
#         return (
#             f"<Location(id={self.id}, region_id={self.region_id}, prov_state_id={self.prov_state_id},"
#             f"country_id={self.country_id}, city_id={self.city_id}>)>"
#         )
# class ProvState(Base):
#     __tablename__ = 'prov_states'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     prov_state_name =  Column(String(100), nullable=True)
#
#
#
#     def __repr__(self):
#         return (
#             f"<ProvState(id={self.id}, prov_state_name='{self.prov_state_name}')>"
#         )
#
# class Region(Base):
#     __tablename__ = 'regions'
#
#     id = Column(Integer, primary_key=True)
#     region_name =  Column(String(100), nullable=False)
#
#
#
#     def __repr__(self):
#         return (
#             f"<Region(id={self.id}, region_name='{self.region_name}')>"
#         )
# class TargetType(Base):
#     __tablename__ = "target_types"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     target_type_name = Column(String(200), unique=True, nullable=False)
#
#
#
#     def __repr__(self):
#         return (f"target_type_id={self.id}, "
#                 f"target_type_name={self.target_type_name}")
#
#
# class TargetTypeEvent(Base):
#     __tablename__ = 'target_type_event'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     event_id = Column(Integer, ForeignKey('events.id'))
#     target_type_id = Column(Integer, ForeignKey('target_types.id'))
#
#
#     def __repr__(self):
#         return (
#             f"<TargetTypeEvent(id={self.id}, event_id={self.event_id}, target_type_id={self.target_type_id})>"
#         )
