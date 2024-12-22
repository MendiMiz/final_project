import json
from collections import defaultdict
from sqlalchemy import func
from app_data.db.psql.database import session_maker
from app_data.db.psql.models import TargetType, Event, TargetTypeEvent, Region, Location, AttackType, AttackTypeEvent, \
    Country, Group, EventGroup

from sqlalchemy import func
from sqlalchemy.orm import aliased

from sqlalchemy.orm import aliased
from sqlalchemy.sql import func


def get_top5_terror_groups_by_region():
    # Using session_query() in a 'with' statement to ensure proper session management
    with session_maker() as session:
        # Query the database for the terror groups and their corresponding region
        query = (
            session.query(
                Region.region_name,
                Group.name.label('terror_group_name'),
                func.count(EventGroup.id).label('attacks_quantity')
            )
            .join(Location, Location.region_id == Region.id)  # Join Location to Region
            .join(Event, Event.location_id == Location.id)  # Join Event to Location
            .join(EventGroup, EventGroup.event_id == Event.id)  # Join EventGroup to Event
            .join(Group, Group.id == EventGroup.group_id)  # Join Group to EventGroup
            .group_by(Region.id, Group.id)  # Group by region and group
            .order_by(func.count(EventGroup.id).desc())  # Order by attacks_quantity in descending order
        )

        results = query.all()

        # Create a dictionary to hold regions and their terror groups
        region_terror_groups = defaultdict(list)

        for row in results:
            region_terror_groups[row.region_name].append({
                "name": row.terror_group_name,
                "attacks_quantity": row.attacks_quantity
            })

        # Convert the dictionary to the desired format
        terror_groups_by_region = [
            {"region": region, "terror_groups": sort_terror_groups_by_attacks(terror_groups)[1:6]}
            for region, terror_groups in region_terror_groups.items()
        ]

    return terror_groups_by_region

def sort_terror_groups_by_attacks(terror_groups):
    """
    Sorts the terror groups by their attack quantity in descending order.
    """
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
    """
    Extract the top `n` elements from a dictionary based on a specific key's value.

    :param input_dict: List of dictionaries to sort.
    :param key: The key used for sorting by its value.
    :param n: Number of top elements to retrieve (default: 5).
    :return: List of the top `n` dictionaries.
    """
    # Sort the list of dictionaries by the specified key in descending order
    sorted_items = sorted(input_dict, key=lambda x: x[key], reverse=True)
    # Return the top `n` items
    return sorted_items[:n]

def get_deadliest_attack_types():
    # Use session_maker to create a session and query the database
    with session_maker() as session:
        # Query to get the deadliest attack types based on total points (2 points per killed, 1 point per injured)
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

        # Execute the query and fetch the results
        results = query.all()

    # Return the results as a list of tuples (attack_type_name, total_points)
    return results

# # Example usage:
# deadliest_attack_types = get_deadliest_attack_types()
# print(deadliest_attack_types[0:5])
# for attack_type, total_points in deadliest_attack_types:
#     print(f"Attack Type: {attack_type}, Total Points: {total_points}")




def get_avg_victims_per_attack_by_region_try_map(mode="all"):
    # Use session_maker to create a session and query the database
    with session_maker() as session:
        # Query to get the average number of victims per attack for each region
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

        # Execute the query and fetch the results
        results = query.all()

        ordered_results = [{'region': row.region_name, 'avg_victims': row.avg_victims} for row in results]

        if mode == "top":
            ordered_results = get_top_n_by_value(ordered_results, "avg_victims", 5)

    return ordered_results


def get_avg_victims_per_attack_by_country_try_map(mode="all"):
    # Use session_maker to create a session and query the database
    with session_maker() as session:
        # Query to get the average number of victims per attack for each country
        query = (
            session.query(
                Country.country_name,
                func.avg((Event.killed * 2) + (Event.injured * 1)).label('avg_victims')
            )
            .join(Location, Location.country_id == Country.id)
            .join(Event, Event.location_id == Location.id)
            .group_by(Country.id)
            .order_by(func.avg((Event.killed * 2) + (Event.injured * 1)).desc())
        )

        # Execute the query and fetch the results
        results = query.all()
        ordered_results = [{'country': row.country_name, 'avg_victims': row.avg_victims} for row in results]
        if mode == "top":
            order_results = get_top_n_by_value(ordered_results, "avg_victims", 5)

    # Return the results as a list of dictionaries (country_name, avg_victims)
    return ordered_results


def get_avg_victims_per_attack_by_region():
    # Use session_maker to create a session and query the database
    with session_maker() as session:
        # Query to get the average number of victims per attack for each region
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

        # Execute the query and fetch the results
        results = query.all()

    # Return the results as a list of tuples (region_name, avg_victims)
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
    # Use session_maker to create a session and query the database
    with session_maker() as session:
        # Query to calculate the average number of victims (2 points per killed, 1 point per injured) by region
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

        # Execute the query and fetch the results
        results = query.all()

    # Return the results as a list of tuples (region_name, avg_victims)
    return results

# Example usage:
# avg_victims_by_region = get_avg_victims_by_region()
# for region_name, avg_victims in avg_victims_by_region:
#     print(f"Region: {region_name}, Average Victims: {avg_victims}")


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

        # Execute the query and fetch the results
        results = query.all()

    return results

# # Example usage:
# attack_target_correlation = get_attack_target_correlation()
# for attack_type, target_type, co_occurrence_count in attack_target_correlation:
#     print(f"Attack Type: {attack_type}, Target Type: {target_type}, Co-occurrence Count: {co_occurrence_count}")
#


def get_annual_attack_count():
    with session_maker() as session:
        # Query to count the total number of events (attacks) per year
        query = (
            session.query(
                Event.year,
                func.count(Event.id).label('total_attacks')
            )
            .group_by(Event.year)
            .order_by(Event.year)
        )

        # Execute the query and fetch the results
        results = query.all()

    return results

# Example usage:
# annual_attack_counts = get_annual_attack_count()
# for year, total_attacks in annual_attack_counts:
#     print(f"Year: {year}, Total Attacks: {total_attacks}")


def get_monthly_attack_count():
    with session_maker() as session:
        # Query to count the total number of events (attacks) per month and year
        query = (
            session.query(
                Event.year,
                Event.month,
                func.count(Event.id).label('total_attacks')
            )
            .group_by(Event.year, Event.month)
            .order_by(Event.year, Event.month)
        )

        # Execute the query and fetch the results
        results = query.all()

    return results
#
# # Example usage:
# monthly_attack_counts = get_monthly_attack_count()
# for year, month, total_attacks in monthly_attack_counts:
#     print(f"Year: {year}, Month: {month}, Total Attacks: {total_attacks}")

def get_most_active_groups_by_area(area_id):
    with session_maker() as session:
        query = (
            session.query(
                Group.name.label('group_name'),
                func.count(Event.id).label('incident_count')
            )
            .join(EventGroup, EventGroup.group_id == Group.id)  # Join to associate events with groups
            .join(Event, Event.id == EventGroup.event_id)  # Join to get event details
            .join(Location, Location.id == Event.location_id)  # Join to filter by area
            .filter(Location.region_id == area_id)  # Filter by region (can adjust to city or country)
            .group_by(Group.name)
            .order_by(func.count(Event.id).desc())  # Order by number of incidents
        )

        # Execute query and get top 5 most active groups in the area
        results = query.all()
        return [{"group_name": group_name, "incident_count": incident_count} for group_name, incident_count in results]


def get_top_5_active_groups_by_country():
    with session_maker() as session:
        # Query to get top 5 active groups per country
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

        # Organize data into a dictionary
        result = {}
        for country_name, group_name, event_count in top_groups_by_country:
            if country_name not in result:
                result[country_name] = []
            result[country_name].append({
                'group_name': group_name,
                'event_count': event_count
            })

        # Limit to top 5 groups per country
        for country_name in result:
            result[country_name] = result[country_name][:5]

    return result

