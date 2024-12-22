from sqlalchemy import func

from app_data.db.psql.database import session_maker
from app_data.db.psql.models import TargetType, Event, TargetTypeEvent, Region, Location, AttackType, AttackTypeEvent


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


from sqlalchemy import func
from app_data.db.psql.models import Event, Group, EventGroup

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
