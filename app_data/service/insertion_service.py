import pandas as pd
from typing import Dict, List
from app_data.db.psql.models import Country, Region, ProvState, City, Event, Location, Group, EventGroup, \
    TargetTypeEvent, TargetType
from app_data.db.psql.models.attack_type import AttackType
from app_data.db.psql.models.attack_type_event import AttackTypeEvent
from app_data.repository.insertion_repository import insert_entities_bulk, insert_cities_bulk, insert_location_bulk, \
    insert_event_bulk, insert_event_group_bulk, insert_target_type_event_bulk
from app_data.service.data_normalization_and_concat_service import normalize_and_concat

def analyze_data_quality(df):
    print("Missing values analysis:")
    for col in ['country', 'region', 'prov_state', 'city']:
        null_count = df[col].isnull().sum()
        total = len(df)
        print(f"{col}: {null_count} nulls out of {total} ({(null_count/total)*100:.2f}%)")


main_csv_path = "C:/Users/INTERNET/PycharmProjects/Global_Terror_Radar/data/globalterrorismdb_0718dist.csv"
csv_to_merge = "C:/Users/INTERNET/PycharmProjects/Global_Terror_Radar/data/RAND_Database_of_Worldwide_Terrorism_Incidents.csv"

def countries_sort_insertion_return_ids_dict(df):
    unique_countries = set(df["country"].dropna())
    countries_ids_dict = insert_entities_bulk(Country, unique_countries, "country_name")
    return countries_ids_dict

def regions_sort_insertion_return_ids_dict(df):
    region_names = set(df["region"])  # Extract unique region names from the DataFrame
    region_ids_dict = insert_entities_bulk(Region, region_names, key_column="region_name")
    return region_ids_dict

def prov_states_sort_insertion_return_ids_dict(df):
    prov_state_names = set(df["prov_state"])  # Extract unique province/state names
    prov_state_ids_dict = insert_entities_bulk(ProvState, prov_state_names, key_column="prov_state_name")
    return prov_state_ids_dict

def terror_groups_sort_insertion_return_ids_dict(df):
    group_names = set(df["group1"].dropna().tolist() + df["group2"].dropna().tolist() + df["group3"].dropna().tolist())
    group_ids_dict = insert_entities_bulk(Group, group_names, key_column="name")
    return group_ids_dict

def target_types_sort_insertion_return_ids_dict(df):
    target_types = set(df["target_type1"].dropna().tolist() + df["target_type2"].dropna().tolist() + df["target_type3"].dropna().tolist())
    target_types_ids_dict = insert_entities_bulk(TargetType, target_types, key_column="target_type_name")
    return target_types_ids_dict

def attack_types_sort_insertion_return_ids_dict(df):
    attack_types = set(df["attack_type1"].dropna().tolist() + df["attack_type2"].dropna().tolist() + df["attack_type3"].dropna().tolist())
    attack_types_ids_dict = insert_entities_bulk(AttackType, attack_types, "attack_type_name")
    return attack_types_ids_dict

def cities_sort_insertion_return_ids_dict(df):
    unique_cities = df.drop_duplicates(subset=["city"])[["city", "latitude", "longitude"]]

    city_list = [
        {"city_name": row["city"], "lat": row["latitude"], "lon": row["longitude"]}
        for _, row in unique_cities.iterrows()
    ]

    city_ids_dict = insert_cities_bulk(city_list)

    return city_ids_dict






def batch_process_dataframe(df: pd.DataFrame, batch_size: int = 1000):
    for start in range(0, len(df), batch_size):
        yield df.iloc[start:start + batch_size]



def insert_from_dataframe(df: pd.DataFrame, batch_size: int = 1000):
    analyze_data_quality(df)

    lookup_dicts = {
        'countries': countries_sort_insertion_return_ids_dict(df),
        'regions': regions_sort_insertion_return_ids_dict(df),
        'prov_states': prov_states_sort_insertion_return_ids_dict(df),
        'groups': terror_groups_sort_insertion_return_ids_dict(df),
        'target_types': target_types_sort_insertion_return_ids_dict(df),
        'attack_types': attack_types_sort_insertion_return_ids_dict(df),
        'cities': cities_sort_insertion_return_ids_dict(df)
    }

    total_processed = 0

    for batch_df in batch_process_dataframe(df, batch_size):
        try:
            locations_batch = prepare_locations_batch(batch_df, lookup_dicts)
            events_batch = prepare_events_batch(batch_df)

            location_ids = insert_location_bulk(locations_batch)

            for event, location_id in zip(events_batch, location_ids):
                event.location_id = location_id

            event_ids = insert_event_bulk(events_batch)

            group_events = prepare_group_events(batch_df, event_ids, lookup_dicts['groups'])
            target_events = prepare_target_events(batch_df, event_ids, lookup_dicts['target_types'])
            attack_events = prepare_attack_events(batch_df, event_ids, lookup_dicts['attack_types'])

            insert_event_group_bulk(group_events)
            insert_target_type_event_bulk(target_events)
            insert_target_type_event_bulk(attack_events)

            total_processed += len(batch_df)
            print(f"Successfully processed {total_processed} records")

        except Exception as e:
            print(f"Error processing batch: {e}")
            continue




def prepare_locations_batch(df: pd.DataFrame, lookup_dicts: Dict) -> List[Location]:
    locations = []
    for _, row in df.iterrows():
        try:
            location = Location(
                country_id=lookup_dicts['countries'].get(row["country"]),
                region_id=lookup_dicts['regions'].get(row["region"]),
                prov_state_id=lookup_dicts['prov_states'].get(row["prov_state"]),
                city_id=lookup_dicts['cities'].get(row["city"])
            )
            locations.append(location)
        except Exception as e:
            print(f"Error creating location for row: {row}")
            print(f"Error: {e}")
            continue
    return locations

def prepare_events_batch(df: pd.DataFrame) -> List[Event]:
    return [
        Event(
            killed=row["killed"],
            injured=row["wounded"],
            terrorists_count=row["terrorists_count"],
            year=row["year"],
            month=row["month"],
            day=row["day"]
        )
        for _, row in df.iterrows()
    ]


def prepare_group_events(df: pd.DataFrame, event_ids: List[int], group_dict: Dict) -> List[EventGroup]:
    group_events = []
    for event_id, row in zip(event_ids, df.iterrows()):
        for group_col in ["group1", "group2", "group3"]:
            if row[1][group_col]:
                group_events.append(
                    EventGroup(
                        event_id=event_id,
                        group_id=group_dict[row[1][group_col]]
                    )
                )
    return group_events

def prepare_target_events(df: pd.DataFrame, event_ids: List[int], target_dict: Dict) -> List[TargetTypeEvent]:
    target_events = []
    for event_id, row in zip(event_ids, df.iterrows()):
        for target_col in ["target_type1", "target_type2", "target_type3"]:
            if row[1][target_col]:
                target_events.append(
                    TargetTypeEvent(
                        event_id=event_id,
                        target_type_id=target_dict[row[1][target_col]]
                    )
                )
    return target_events

def prepare_attack_events(df: pd.DataFrame, event_ids: List[int], attack_dict: Dict) -> List[AttackTypeEvent]:
    attack_events = []
    for event_id, row in zip(event_ids, df.iterrows()):
        for attack_col in ["attack_type1", "attack_type2", "attack_type3"]:
            if row[1][attack_col]:
                attack_events.append(
                    AttackTypeEvent(
                        event_id=event_id,
                        attack_type_id=attack_dict[row[1][attack_col]]
                    )
                )
    return attack_events






