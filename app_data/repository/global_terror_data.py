import csv

from app_data.db.psql.models import Country, Region, ProvState, City, Event, Location
from app_data.repository.event_repository import insert_model, insert_location, insert_city

csv_path = "C:/Users/INTERNET/PycharmProjects/Global_Terror_Radar/data/globalterrorismdb_0718dist-1000rows.csv"


def get_date(attack):
    return {"year": attack["iyear"], "month": attack["imonth"], "day": attack["iday"]}


def get_location(attack):
    return {"country": attack.get("country_txt", ""), "region": attack.get("region_txt", ""),
            "provstate": attack.get("provstate", ""), "city": attack.get("city_txt", ""),
            "lat": attack.get("latitude", ""), "lon": attack.get("longitude", "")}


def get_victims_n(attack):
    return {"killed": attack["nkill"], "wounded": attack["nwound"]}


def get_terror_groups(attack):
    return {"group1": attack["gname"], "group2": attack["gname2"], "group3": attack["gname3"]}


def normalize_attack(attack):
    return {
                "date": get_date(attack),
                "location": get_location(attack),
                "victims_count": get_victims_n(attack),
                "group_participating": get_terror_groups(attack),
                "number_of_terrorists": attack["nperps"]
    }


def normalized_csv_attacks_data():
    with open(csv_path, "r", encoding='iso-8859-1') as file:
        attacks = csv.DictReader(file)
        return [normalize_attack(attack) for attack in attacks]

def attacks_from_csv():
    with open(csv_path, "r", encoding='iso-8859-1') as file:
        attacks = csv.DictReader(file)
        return [attack for attack in attacks]

def insert_to_location(attack):
    locations_details = get_location(attack)

    country_id = insert_model(Country(country_name=locations_details["country"]))
    region_id = insert_model(Region(region_name=locations_details["region"]))
    prov_state_id = insert_model(ProvState(prov_state_name=locations_details["provstate"]))
    city_id = insert_city(City(city_name=locations_details["city"],
                 lat= locations_details["lat"], lon= locations_details["lon"]))

    location_id = insert_location(
        Location(country_id=country_id, region_id=region_id, prov_state_id=prov_state_id, city_id=city_id)
    )
    return location_id

def insert_attack(attack):
    location_id = insert_to_location(attack)
    return location_id

def insert_csv_to_psql(attacks):
    return[insert_attack(attack) for attack in attacks]


print(insert_csv_to_psql(attacks_from_csv()))




# def produce_students_for_psql():
#     with open(students_path, 'r') as file:
#         students = csv.DictReader(file)
#         students_data = [student_data(student) for student in students]
#         produce_chunks(students_data, produce, students_data_topic, 100)
