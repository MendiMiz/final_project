import csv

from app_data.db.psql.models import Country, Region, ProvState, City, Event, Location
from app_data.repository.event_repository import insert_model, insert_location, insert_city, insert_country, \
    insert_region, insert_provstate

csv_path = "/data/globalterrorismdb_0718dist-1000rows.csv"


def safe_int(value):
    try:
        print()
        if value == -99:
            return None
        else:
            return int(value) if value else None
    except (ValueError, TypeError):
        return None

def safe_float(value):
    try:
        return float(value) if value else None
    except (ValueError, TypeError):
        return None

def get_date(attack):
    return {"year": attack["iyear"], "month": attack["imonth"], "day": attack["iday"]}


def get_location(attack):
    return {"country": attack.get("country_txt", ""), "region": attack.get("region_txt", ""),
            "provstate": attack.get("provstate", ""), "city": attack.get("city", ""),
            "lat": safe_float(attack.get("latitude", None)), "lon": safe_float(attack.get("longitude", None))}


def get_victims_n(attack):
    return {"killed": safe_int(attack.get("nkill", 0)), "wounded": safe_int(attack.get("nwound", 0))}


def get_terror_groups(attack):
    return {"group1": attack["gname"], "group2": attack["gname2"], "group3": attack["gname3"]}



def attacks_from_csv():
    with open(csv_path, "r", encoding='iso-8859-1') as file:
        attacks = csv.DictReader(file)
        return [attack for attack in attacks]

def insert_to_location(attack):
    locations_details = get_location(attack)
    country_id = insert_country(Country(country_name=locations_details["country"]))
    region_id = insert_region(Region(region_name=locations_details["region"]))
    prov_state_id = insert_provstate(ProvState(prov_state_name=locations_details["provstate"]))
    city_id = insert_city(City(city_name=locations_details["city"],
                 lat= locations_details["lat"], lon= locations_details["lon"]))

    location_id = insert_location(
        Location(country_id=country_id, region_id=region_id, prov_state_id=prov_state_id, city_id=city_id)
    )
    return location_id

def insert_event(attack, location_id):
    date = get_date(attack)
    victims = get_victims_n(attack)
    terr_num = safe_int(attack.get("nperps", None))
    print(terr_num)
    event_id = insert_model(
        Event(
            location_id=location_id,
            killed=victims["killed"],
            injured=victims["wounded"],
            terrorists_count=safe_int(attack.get("nperps", None)),
            year=safe_int(date["year"]),
            month=safe_int(date["month"]),
            day=safe_int(date["day"])
        )
    )
    return event_id

def insert_attack(attack):
    location_id = insert_to_location(attack)
    event_id = insert_event(attack, location_id)
    return location_id

def insert_csv_to_psql(attacks):
    return[insert_attack(attack) for attack in attacks]


print(insert_csv_to_psql(attacks_from_csv()))



# def normalize_attack(attack):
#     return {
#                 "date": get_date(attack),
#                 "location": get_location(attack),
#                 "victims_count": get_victims_n(attack),
#                 "group_participating": get_terror_groups(attack),
#                 "number_of_terrorists": attack.get(["nperps"], -99)
#     }


# def normalized_csv_attacks_data():
#     with open(csv_path, "r", encoding='iso-8859-1') as file:
#         attacks = csv.DictReader(file)
#         return [normalize_attack(attack) for attack in attacks]

