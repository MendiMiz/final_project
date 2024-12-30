from collections import defaultdict
from typing import List, Dict

from app_data.db.psql.database import session_maker
from app_data.db.psql.models import TargetType, Event, TargetTypeEvent, Region, Location, AttackType, AttackTypeEvent, \
    Country, Group, EventGroup
from sqlalchemy.sql import func


def get_top5_terror_groups_by_region():
    with session_maker() as session:
        query = (
            session.query(
                Region.region_name,
                Group.name.label('terror_group_name'),
                func.count(EventGroup.id).label('attacks_quantity')
            )
            .join(Location, Location.region_id == Region.id)
            .join(Event, Event.location_id == Location.id)
            .join(EventGroup, EventGroup.event_id == Event.id)
            .join(Group, Group.id == EventGroup.group_id)
            .group_by(Region.id, Group.id)
            .order_by(func.count(EventGroup.id).desc())
        )

        results = query.all()

        region_terror_groups = defaultdict(list)

        for row in results:
            region_terror_groups[row.region_name].append({
                "name": row.terror_group_name,
                "attacks_quantity": row.attacks_quantity
            })

        # Convert the dictionary to the desired format
        terror_groups_by_region = [
            {"region": region, "terror_groups": sort_terror_groups_by_attacks_quantity(terror_groups)[1:6]}
            for region, terror_groups in region_terror_groups.items()
        ]

    return terror_groups_by_region

def sort_terror_groups_by_attacks_quantity(terror_groups):
    return sorted(terror_groups, key=lambda x: x['attacks_quantity'], reverse=True)




def get_percentage_change_in_attacks_by_region(mode="all"):
    with session_maker() as session:
        query = (
            session.query(
                Region.region_name,
                Event.year,
                func.count(Event.id).label('attack_count')
            )
            .join(Location, Location.region_id == Region.id)
            .join(Event, Event.location_id == Location.id)
            .group_by(Region.region_name, Event.year)
            .order_by(Region.region_name, Event.year)
        )

        results = query.all()

    region_data = defaultdict(list)
    for row in results:
        region_data[row.region_name].append({'year': row.year, 'count': row.attack_count})

    percentage_changes_by_region = []
    for region, data in region_data.items():
        changes = []
        for i in range(1, len(data)):
            prev_count = data[i - 1]['count']
            curr_year = data[i]['year']
            curr_count = data[i]['count']

            if prev_count > 0:
                change = ((curr_count - prev_count) / prev_count) * 100
            else:
                change = None

            changes.append({
                'year': curr_year,
                'percentage_change': change
            })

            if mode == "top":
                changes = get_top_n_by_value(changes, "percentage_change", 5)

        percentage_changes_by_region.append({
            'region': region,
            'changes': changes
        })

    return percentage_changes_by_region

def get_top_n_by_value(input_dict, key, n=5):
    sorted_items = sorted(input_dict, key=lambda x: x[key], reverse=True)
    return sorted_items[:n]

def get_deadliest_attack_types():
    with session_maker() as session:
        query = (
            session.query(
                TargetType.target_type_name,
                func.sum(
                    Event.killed * 2 + (Event.injured * 1)
                ).label('total_points')
            )
            .join(TargetTypeEvent, TargetTypeEvent.event_id == Event.id)
            .join(TargetType, TargetType.id == TargetTypeEvent.target_type_id)
            .group_by(TargetType.id)
            .order_by(func.sum((Event.killed * 2) + (Event.injured * 1)).desc())
        )

        results = query.all()

    return results



def get_avg_victims_per_attack_by_region_try_map(mode="all"):
    with session_maker() as session:
        query = (
            session.query(
                Region.region_name,
                func.avg((Event.killed * 2) + (Event.injured * 1)).label('avg_victims')
            )
            .join(Location, Location.region_id == Region.id)
            .join(Event, Event.location_id == Location.id)
            .group_by(Region.id)
            .order_by(func.avg((Event.killed * 2) + (Event.injured * 1)).desc())
        )

        results = query.all()

        ordered_results = [{'region': row.region_name, 'avg_victims': row.avg_victims} for row in results]

        if mode == "top":
            ordered_results = get_top_n_by_value(ordered_results, "avg_victims", 5)

    return ordered_results


def get_avg_victims_per_country(mode: str = "all") -> List[Dict[str, float]]:

    if mode not in ["all", "top"]:
        raise ValueError("Invalid mode. Expected 'all' or 'top'.")

    with session_maker() as session:
        query = (
            session.query(
                Country.country_name,
                func.avg((Event.killed * 2) + (Event.injured * 1)).label('avg_victims')
            )
            .join(Location, Location.country_id == Country.id)
            .join(Event, Event.location_id == Location.id)
            .group_by(Country.country_name)
            .having(func.avg((Event.killed * 2) + (Event.injured * 1)) != None)  # Exclude NULL values
            .order_by(func.avg((Event.killed * 2) + (Event.injured * 1)).desc())
        )

        if mode == "top":
            query = query.limit(5)

        try:
            results = query.all()
            print(results)
        except Exception as e:
            print(f"Database query failed: {e}")
            return []

        return [{'country': row.country_name, 'avg_victims': row.avg_victims} for row in results]


def get_avg_victims_per_attack_by_region():
    with session_maker() as session:
        query = (
            session.query(
                Region.region_name,
                func.avg((Event.killed * 2) + (Event.injured * 1)).label('avg_victims')
            )
            .join(Location, Location.region_id == Region.id)
            .join(Event, Event.location_id == Location.id)
            .group_by(Region.id)
            .order_by(func.avg((Event.killed * 2) + (Event.injured * 1)).desc())
        )

        results = query.all()

    return results


def get_top_terror_groups():
    with session_maker() as session:
        query = (
            session.query(
                Group.name.label('group_name'),
                func.sum(func.coalesce(Event.killed, 0) * 2 + func.coalesce(Event.injured, 0)).label('total_points')
            )
            .join(EventGroup, EventGroup.group_id == Group.id)
            .join(Event, Event.id == EventGroup.event_id)
            .group_by(Group.name)
            .order_by(func.sum(func.coalesce(Event.killed, 0) * 2 + func.coalesce(Event.injured, 0)).desc())
            .limit(5)
        )

        results = query.all()

        return [{"group_name": group_name, "total_points": total_points} for group_name, total_points in results]

def get_avg_victims_by_region():
    with session_maker() as session:
        query = (
            session.query(
                Region.region_name,
                func.avg(
                    (Event.killed * 2) + (Event.injured * 1)
                ).label('avg_victims')
            )
            .join(Location, Location.region_id == Region.id)  # Join Location to get the region
            .join(Event, Event.location_id == Location.id)  # Join Event to get the victims data
            .group_by(Region.id)
            .order_by(func.avg((Event.killed * 2) + (Event.injured * 1)).desc())  # Order by average victims in descending order
        )

        results = query.all()

    return results



def get_attack_target_correlation():
    with session_maker() as session:
        query = (
            session.query(
                AttackType.attack_type_name,
                TargetType.target_type_name,
                func.count(AttackTypeEvent.event_id).label('co_occurrence_count')
            )
            .join(AttackTypeEvent, AttackTypeEvent.attack_type_id == AttackType.id)  # Join AttackTypeEvent
            .join(TargetTypeEvent, TargetTypeEvent.event_id == AttackTypeEvent.event_id)  # Join TargetTypeEvent to link target types
            .join(TargetType, TargetType.id == TargetTypeEvent.target_type_id)  # Join TargetType to get target names
            .group_by(AttackType.id, TargetType.id)
            .order_by(func.count(AttackTypeEvent.event_id).desc())  # Order by the co-occurrence count
        )

        results = query.all()

    return results



def get_annual_attack_count():
    with session_maker() as session:
        query = (
            session.query(
                Event.year,
                func.count(Event.id).label('total_attacks')
            )
            .group_by(Event.year)
            .order_by(Event.year)
        )

        results = query.all()

    return results



def get_monthly_attack_count():
    with session_maker() as session:
        query = (
            session.query(
                Event.year,
                Event.month,
                func.count(Event.id).label('total_attacks')
            )
            .group_by(Event.year, Event.month)
            .order_by(Event.year, Event.month)
        )

        results = query.all()

    return results



def get_most_active_groups_by_area(area_id):
    with session_maker() as session:
        query = (
            session.query(
                Group.name.label('group_name'),
                func.count(Event.id).label('incident_count')
            )
            .join(EventGroup, EventGroup.group_id == Group.id)
            .join(Event, Event.id == EventGroup.event_id)
            .join(Location, Location.id == Event.location_id)
            .filter(Location.region_id == area_id)
            .group_by(Group.name)
            .order_by(func.count(Event.id).desc())
        )

        results = query.all()
        return [{"group_name": group_name, "incident_count": incident_count} for group_name, incident_count in results]


def get_top_5_active_groups_by_country():
    with session_maker() as session:
        top_groups_by_country = (
            session.query(
                Country.country_name,
                Group.name,
                func.count(Event.id).label('event_count')
            )
            .join(Location, Location.country_id == Country.id)
            .join(Event, Event.location_id == Location.id)
            .join(EventGroup, EventGroup.event_id == Event.id)
            .join(Group, Group.id == EventGroup.group_id)
            .group_by(Country.id, Group.id)
            .order_by(Country.id, func.count(Event.id).desc())
            .all()
        )

        result = {}
        for country_name, group_name, event_count in top_groups_by_country:
            if country_name not in result:
                result[country_name] = []
            result[country_name].append({
                'group_name': group_name,
                'event_count': event_count
            })

        for country_name in result:
            result[country_name] = result[country_name][1:6]

    return result


