import json
from collections import defaultdict
from sqlalchemy import func

from app_data.db.psql.database import session_maker
from app_data.db.psql.models import Group, Event, EventGroup, TargetType, Location, Country, TargetTypeEvent, Region, \
    AttackType, AttackTypeEvent


def get_events_with_multiple_groups():
    with session_maker() as session:
        events_with_groups = (
            session.query(
                Event.id.label("event_id"),
                func.array_agg(Group.name).label("group_names")
            )
            .join(EventGroup, EventGroup.event_id == Event.id)
            .join(Group, Group.id == EventGroup.group_id)
            .group_by(Event.id)
            .having(func.count(Group.id) > 1)
            .all()
        )

        result = [
            {"event_id": event.event_id, "group_names": event.group_names}
            for event in events_with_groups
        ]

    return result


def get_group_cooperation():
    """
    Retrieves a list of terrorist groups and the groups they cooperated with in attacks.

    Returns:
        list: A list of dictionaries, each containing a terrorist group and a list of groups it cooperated with.
    """
    with session_maker() as session:
        events_with_groups = (
            session.query(
                Event.id.label("event_id"),
                func.array_agg(Group.name).label("group_names")
            )
            .join(EventGroup, EventGroup.event_id == Event.id)
            .join(Group, Group.id == EventGroup.group_id)
            .group_by(Event.id)
            .having(func.count(Group.id) > 1)
            .all()
        )

        cooperation_data = {}

        # Build the cooperation map
        for event in events_with_groups:
            group_names = event.group_names
            for group in group_names:
                if group not in cooperation_data:
                    cooperation_data[group] = set()
                cooperation_data[group].update(name for name in group_names if name != group)

        result = [{"terror_group": group, "cooperate_with": list(cooperators)} for group, cooperators in cooperation_data.items()]

    return result


def get_top_targets_per_country():
    with session_maker() as session:
        targets_query = (
            session.query(
                Country.country_name,
                TargetType.target_type_name.label("target_type_name"),
                Group.name.label("group_name")
            )
            .join(Location, Location.country_id == Country.id)
            .join(Event, Event.location_id == Location.id)
            .join(EventGroup, EventGroup.event_id == Event.id)
            .join(Group, Group.id == EventGroup.group_id)
            .join(TargetTypeEvent, TargetTypeEvent.event_id == Event.id)
            .join(TargetType, TargetType.id == TargetTypeEvent.target_type_id)
            .distinct(Country.id, TargetType.id, Group.id)
            .all()
        )

        result = {}
        for country_name, target_type_name, group_name in targets_query:
            if country_name not in result:
                result[country_name] = {}
            if target_type_name not in result[country_name]:
                result[country_name][target_type_name] = set()
            result[country_name][target_type_name].add(group_name)

        # Select the target type with the most groups for each country
        top_targets = []
        for country_name, targets in result.items():
            top_target = max(
                targets.items(),
                key=lambda x: len(x[1])
            )
            target_type_name, groups = top_target
            top_targets.append({
                "country": country_name,
                "target_type_name": target_type_name,
                "groups_involved": list(groups)
            })

    return top_targets



def get_most_attacked_target_type_per_region():
    """
    Retrieves the target type that was attacked by the most terrorist groups for each region.
    Returns:
        list: A list of dictionaries containing the region, the target type, and the groups involved.
    """
    with session_maker() as session:
        query = (
            session.query(
                Region.region_name,  # Region name
                TargetType.target_type_name,  # Target type name
                Group.name.label('group_name')  # Group name
            )
            .join(Location, Location.region_id == Region.id)  # Join on region to get locations
            .join(Event, Event.location_id == Location.id)  # Join on events
            .join(EventGroup, EventGroup.event_id == Event.id)  # Join on EventGroup to link groups
            .join(Group, Group.id == EventGroup.group_id)  # Join on Group
            .join(TargetTypeEvent, TargetTypeEvent.event_id == Event.id)  # Join on TargetTypeEvent to get target type
            .join(TargetType, TargetType.id == TargetTypeEvent.target_type_id)  # Join on TargetType
            .all()
        )

        # Step 1: Organize data by region and target type, counting the unique groups involved
        region_target_groups = {}

        for region_name, target_type_name, group_name in query:
            if region_name not in region_target_groups:
                region_target_groups[region_name] = {}

            if target_type_name not in region_target_groups[region_name]:
                region_target_groups[region_name][target_type_name] = set()  # Using a set to avoid duplicates

            region_target_groups[region_name][target_type_name].add(group_name)

        # Step 2: Identify the target type with the most unique groups for each region
        result = []
        for region_name, target_types in region_target_groups.items():
            # Sort the target types by the number of unique groups (descending) and pick the one with the most groups
            most_attacked_target_type = max(
                target_types.items(),
                key=lambda x: len(x[1])  # Sort by number of unique groups involved
            )

            target_type_name, groups_involved = most_attacked_target_type
            result.append({
                "region": region_name,
                "target_type_name": target_type_name,
                "groups_involved": list(groups_involved)  # List of groups involved
            })

    return result



def get_top_5_groups_by_target_type_in_region(region_id):
    with session_maker() as session:
        # Query to get the top 5 groups with the most target types attacked in the region
        top_groups = (
            session.query(
                Group.name,
                func.count(func.distinct(TargetTypeEvent.target_type_id)).label('target_types_count')
            )
            .join(EventGroup, EventGroup.group_id == Group.id)
            .join(Event, Event.id == EventGroup.event_id)
            .join(TargetTypeEvent, TargetTypeEvent.event_id == Event.id)
            .join(Location, Location.id == Event.location_id)
            .join(TargetType, TargetType.id == TargetTypeEvent.target_type_id)
            .filter(Location.region_id == region_id)
            .group_by(Group.id)
            .order_by(func.count(func.distinct(TargetTypeEvent.target_type_id)).desc())
            .limit(5)  # Get the top 5 groups
            .all()
        )

        # Format the result into a list of dictionaries
        result = [{'group_name': group_name, 'target_types_count': target_types_count} for group_name, target_types_count in top_groups]

    return result


def get_groups_by_all_locations(location_type: str):
    """
    Retrieve the number of distinct groups and their names for all countries or regions.

    :param location_type: Either "country" or "region".
    :return: A list of dictionaries, each containing location name, group count, and group names.
    """
    if location_type not in {"country", "region"}:
        raise ValueError("location_type must be 'country' or 'region'")

    with session_maker() as session:

        location_name_column = {
            "country": Country.country_name,
            "region": Region.region_name,
        }[location_type]

        query = (
            session.query(
                location_name_column.label("location_name"),
                func.count(Group.id.distinct()).label("group_count"),
                func.array_agg(func.distinct(Group.name)).label("group_names")
            )
            .join(EventGroup, Group.id == EventGroup.group_id)
            .join(Event, Event.id == EventGroup.event_id)
            .join(Location, Event.location_id == Location.id)
            .join(Country, Location.country_id == Country.id, isouter=True)
            .join(Region, Location.region_id == Region.id, isouter=True)
            .group_by(location_name_column)
        )

        results = query.all()

        return [
            {"location_name": row.location_name, "group_count": row.group_count, "group_names": row.group_names}
            for row in results
        ]


def get_groups_with_common_targets_by_years():
    with session_maker() as session:
        query = (
            session.query(
                Event.year,
                Group.name.label('group_name'),
                TargetType.target_type_name,
                func.count(Event.id).label('attack_count')
            )
            .join(EventGroup, Event.id == EventGroup.event_id)
            .join(Group, EventGroup.group_id == Group.id)
            .join(TargetTypeEvent, Event.id == TargetTypeEvent.event_id)
            .join(TargetType, TargetTypeEvent.target_type_id == TargetType.id)
            .group_by(Event.year, Group.name, TargetType.target_type_name)
            .order_by(Event.year, TargetType.target_type_name, Group.name)
        )

        results = query.all()

        targeting_patterns = defaultdict(lambda: defaultdict(list))
        for row in results:
            targeting_patterns[row.year][row.target_type_name].append({
                'group': row.group_name,
                'attacks': row.attack_count
            })

        return targeting_patterns


