import json

import pandas as pd
import numpy as np
import csv

from app_data.db.psql.models import Country, Region, ProvState, City, Event, Location, Group, EventGroup, \
    TargetTypeEvent, TargetType
from app_data.db.psql.models.attack_type import AttackType
from app_data.db.psql.models.attack_type_event import AttackTypeEvent
from app_data.repository.event_repository import insert_model, insert_location, insert_city, \
     insert_event_group, insert_target_type_event, \
    insert_attack_type_event, insert_entities_bulk

# Define the path to the CSV file
csv_path = "C:/Users/INTERNET/PycharmProjects/Global_Terror_Radar/data/globalterrorismdb_0718dist-1000rows.csv"


# Safe conversion functions
def safe_int(value):
    try:
        return None if value == -99 else int(value)
    except (ValueError, TypeError):
        return None


def safe_float(value):
    try:
        return float(value) if value else None
    except (ValueError, TypeError):
        return None


# Function to normalize the data into a pandas DataFrame
def normalize_data_to_dataframe(csv_path):
    # Load the CSV into a pandas DataFrame
    df = pd.read_csv(csv_path, encoding='iso-8859-1')

    # Select and rename relevant columns
    normalized_df = pd.DataFrame({
        "year": df["iyear"].apply(safe_int),
        "month": df["imonth"].apply(safe_int),
        "day": df["iday"].apply(safe_int),
        "country": df["country_txt"],
        "region": df["region_txt"],
        "prov_state": df["provstate"],
        "city": df["city"],
        "latitude": df["latitude"].apply(safe_float),
        "longitude": df["longitude"].apply(safe_float),
        "killed": df["nkill"].apply(safe_int),
        "wounded": df["nwound"].apply(safe_int),
        "terrorists_count": df["nperps"].apply(safe_int),
        "group1": df["gname"],
        "group2": df["gname2"],
        "group3": df["gname3"],
        "target_type1": df["targtype1_txt"],
        "target_type2": df["targtype2_txt"],
        "target_type3": df["targtype3_txt"],
        "attack_type1": df["attacktype1_txt"],
        "attack_type2": df["attacktype2_txt"],
        "attack_type3": df["attacktype3_txt"]
    })

    normalized_df = normalized_df.replace({np.nan: None})

    return normalized_df

def insert_from_dataframe(df):

    unique_countries = set(dataframe["country"].dropna())
    countries_ids_dict = insert_entities_bulk(Country, unique_countries, "country_name")

    region_names = set(df["region"])  # Extract unique region names from the DataFrame
    region_ids_dict = insert_entities_bulk(Region, region_names, key_column="region_name")

    prov_state_names = set(df["prov_state"])  # Extract unique province/state names
    prov_state_ids_dict = insert_entities_bulk(ProvState, prov_state_names, key_column="prov_state_name")

    group_names = set(df["group1"].dropna().tolist() + df["group2"].dropna().tolist() + df["group3"].dropna().tolist())
    group_ids_dict = insert_entities_bulk(Group, group_names, key_column="name")

    target_types = set(df["target_type1"].dropna().tolist() + df["target_type2"].dropna().tolist() + df["target_type3"].dropna().tolist())
    target_types_ids_dict = insert_entities_bulk(TargetType, target_types, key_column="target_type_name")

    attack_types = set(df["attack_type1"].dropna().tolist() + df["attack_type2"].dropna().tolist() + df["attack_type3"].dropna().tolist())
    attack_types_ids_dict = insert_entities_bulk(AttackType, attack_types, "attack_type_name")

    for _, row in df.iterrows():


        country_id = countries_ids_dict[row["country"]]
        region_id = region_ids_dict[row["region"]]
        prov_state_id = prov_state_ids_dict[row["prov_state"]]

        # Insert city
        city_id = insert_city(
            City(
                city_name=row["city"],
                lat=row["latitude"],
                lon=row["longitude"]
            )
        )

        # Insert location
        location_id = insert_location(
            Location(
                country_id= country_id,
                region_id=region_id,
                prov_state_id=prov_state_id,
                city_id=city_id
            )
        )

        # Insert event
        event_id = insert_model(
            Event(
                location_id=location_id,
                killed=row["killed"],
                injured=row["wounded"],
                terrorists_count=row["terrorists_count"],
                year=row["year"],
                month=row["month"],
                day=row["day"]
            )
        )
        print(f"Inserted event with ID: {event_id}")

        group_names = [row.get("group1"), row.get("group2"), row.get("group3")]
        group_ids = [group_ids_dict[name] for name in group_names if name]


        [insert_event_group(EventGroup(event_id=event_id, group_id=group_id)) for group_id in group_ids]


        target_type_names = [row.get("target_type1"), row.get("target_type2"), row.get("target_type3")]
        target_type_ids = [target_types_ids_dict[name] for name in target_type_names if name]

        [insert_target_type_event(TargetTypeEvent(event_id=event_id, target_type_id=target_type_id))for target_type_id in target_type_ids]


        attack_type_names = [row.get("attack_type1"), row.get("attack_type2"), row.get("attack_type3")]
        attack_type_ids = [attack_types_ids_dict[name] for name in attack_type_names if name]

        [insert_attack_type_event(AttackTypeEvent(event_id=event_id, attack_type_id=attack_type_id)) for attack_type_id in attack_type_ids]

        print(f"Inserted target type event link for event ID: {event_id}")


# Normalize the data
dataframe = normalize_data_to_dataframe(csv_path)
insert_from_dataframe(dataframe)
# # Insert the normalized data into the database
# insert_from_dataframe(dataframe)
# normalized_data_df = normalize_data_to_dataframe(csv_path)