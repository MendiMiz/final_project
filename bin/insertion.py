
# def insert_from_dataframe(df):
#
#     countries_ids_dict = countries_sort_insertion_return_ids_dict(df)
#     region_ids_dict = regions_sort_insertion_return_ids_dict(df)
#     prov_state_ids_dict = prov_states_sort_insertion_return_ids_dict(df)
#     group_ids_dict = terror_groups_sort_insertion_return_ids_dict(df)
#     target_types_ids_dict = target_types_sort_insertion_return_ids_dict(df)
#     attack_types_ids_dict = attack_types_sort_insertion_return_ids_dict(df)
#     city_ids_dict = cities_sort_insertion_return_ids_dict(df)
#
#     batch_size = 1000
#     locations_batch = []
#     events_batch = []
#     group_event_batch = []
#     target_event_batch = []
#     attack_event_batch = []
#
#
#     inserted = 0
#     for _, row in df.iterrows():
#
#
#         country_id = countries_ids_dict[row["country"]]
#         region_id = region_ids_dict[row["region"]]
#         prov_state_id = prov_state_ids_dict[row["prov_state"]]
#         city_id = city_ids_dict[row["city"]]
#
#
#         # Insert location
#         locations_batch.append(
#             Location(
#                 country_id= country_id,
#                 region_id=region_id,
#                 prov_state_id=prov_state_id,
#                 city_id=city_id
#             )
#         )
#
#         # Insert event
#         events_batch.append(
#             Event(
#                 killed=row["killed"],
#                 injured=row["wounded"],
#                 terrorists_count=row["terrorists_count"],
#                 year=row["year"],
#                 month=row["month"],
#                 day=row["day"]
#             )
#         )
#
#         group_names = [row.get("group1"), row.get("group2"), row.get("group3")]
#         group_event_batch.append([EventGroup(group_id=group_ids_dict[name]) for name in group_names if name])
#
#
#
#
#         target_type_names = [row.get("target_type1"), row.get("target_type2"), row.get("target_type3")]
#         target_event_batch.append([TargetTypeEvent(target_type_id=target_types_ids_dict[name]) for name in target_type_names if name])
#
#
#
#         attack_type_names = [row.get("attack_type1"), row.get("attack_type2"), row.get("attack_type3")]
#         attack_event_batch.append([AttackTypeEvent(attack_type_id=attack_types_ids_dict[name]) for name in attack_type_names if name])
#
#
#         if batch_size >= len(events_batch):
#             location_ids = insert_location_bulk(locations_batch)
#
#             for event, location_id in zip(events_batch, location_ids):
#                 event.location_id = location_id
#             event_ids = insert_event_bulk(events_batch)
#
#             updated_group_event = []
#             for event_id, group_events in zip (event_ids, group_event_batch):
#                 for group_event in group_events:
#                     group_event.event_id = event_id
#                     updated_group_event.append(group_event)
#             insert_event_group_bulk(updated_group_event)
#
#             updated_target_type_event = []
#             for event_id, target_events in zip(event_ids, target_event_batch):
#                 for target_event in target_events:
#                     target_event.event_id = event_id
#                     updated_target_type_event.append(target_event)
#             insert_target_type_event_bulk(updated_group_event)
#
#
#             updated_attack_type_event = []
#             for event_id, attacks_event in zip(event_ids, attack_event_batch):
#                 for attack_event in attacks_event:
#                     attack_event.event_id = event_id
#                     updated_target_type_event.append(attack_event)
#             insert_target_type_event_bulk(updated_attack_type_event)
#
#             events_batch.clear()
#             locations_batch.clear()
#             events_batch.clear()
#             group_event_batch.clear()
#             target_event_batch.clear()
#             attack_event_batch.clear()
#
#         inserted += 1000
#         print(f"{inserted} events inserted.")


# Function to normalize the data into a pandas DataFrame
# def normalize_data_to_dataframe(csv_path):
#     # Load the CSV into a pandas DataFrame with low_memory=False
#     df = pd.read_csv(csv_path, encoding='iso-8859-1', low_memory=False)
#
#     normalized_df = pd.DataFrame({
#         "year": df["iyear"].apply(safe_int),
#         "month": df["imonth"].apply(safe_int),
#         "day": df["iday"].apply(safe_int),
#         "country": df["country_txt"],
#         "region": df["region_txt"],
#         "prov_state": df["provstate"],
#         "city": df["city"].fillna("unknown"),  # Changed to avoid inplace warning
#         "latitude": df["latitude"].apply(safe_float),
#         "longitude": df["longitude"].apply(safe_float),
#         "killed": df["nkill"].apply(safe_int),
#         "wounded": df["nwound"].apply(safe_int),
#         "terrorists_count": df["nperps"].apply(safe_int),
#         "group1": df["gname"],
#         "group2": df["gname2"],
#         "group3": df["gname3"],
#         "target_type1": df["targtype1_txt"],
#         "target_type2": df["targtype2_txt"],
#         "target_type3": df["targtype3_txt"],
#         "attack_type1": df["attacktype1_txt"],
#         "attack_type2": df["attacktype2_txt"],
#         "attack_type3": df["attacktype3_txt"]
#     })
#
#     normalized_df = normalized_df.replace({np.nan: None})
#     return normalized_df


