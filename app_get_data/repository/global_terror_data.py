import csv
import json

csv_path = "C:/Users/INTERNET/PycharmProjects/Global_Terror_Radar/data/globalterrorismdb_0718dist-1000rows.csv"

def get_date(attack):
    return {"year": attack["iyear"], "month": attack["imonth"], "day": attack["iday"]}

def get_location(attack):
    return {"country": attack["country_txt"], "region": attack["region_txt"], "provstate": attack["provstate"],
            "city": attack["city"], "lat": attack["latitude"], "lon": attack["longitude"]}

def get_victims_n(attack):
    return {"killed": attack["nkill"], "wounded": attack["nwound"]}

def get_terror_groups(attack):
    return {"group1": attack["gname"], "group2": attack["gname2"], "group3": attack["gname3"]}

def normalize_csv_data():
    with open(csv_path, "r", encoding='iso-8859-1') as file:
        attacks = csv.DictReader(file)
        normalized_attacks = []
        for attack in attacks:
            attack_data = {
                "date": get_date(attack),
                "location": get_location(attack),
                "victims_count": get_victims_n(attack),
                "group_participating": get_terror_groups(attack),
                "number_of_terrorists": attack["nperps"]
            }
            normalized_attacks.append(attack_data)
        return json.dumps(normalized_attacks, indent=4)

print(normalize_csv_data())

# def produce_students_for_psql():
#     with open(students_path, 'r') as file:
#         students = csv.DictReader(file)
#         students_data = [student_data(student) for student in students]
#         produce_chunks(students_data, produce, students_data_topic, 100)
