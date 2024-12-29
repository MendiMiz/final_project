import pandas as pd
import numpy as np
from app_data.utils.safe_values import safe_int, safe_float


def load_and_normalize_main_csv(csv_path):
    df = pd.read_csv(csv_path, encoding='iso-8859-1', low_memory=False)
    normalized_df = pd.DataFrame({
        "year": df["iyear"].apply(safe_int),
        "month": df["imonth"].apply(safe_int),
        "day": df["iday"].apply(safe_int),
        "country": df["country_txt"],
        "region": df["region_txt"],
        "prov_state": df["provstate"],
        "city": df["city"].fillna("unknown"),
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
    return normalized_df

def load_and_preprocess_new_csv(new_csv_path):
    new_df = pd.read_csv(new_csv_path, encoding='iso-8859-1', low_memory=False)
    new_df.rename(columns={
        "Date": "date",
        "City": "city",
        "Country": "country",
        "Perpetrator": "group1",
        "Weapon": "attack_type1",
        "Injuries": "wounded",
        "Fatalities": "killed",
        "Description": "description"
    }, inplace=True)

    new_df['date'] = pd.to_datetime(new_df['date'], format='%d-%b-%y', errors='coerce')
    new_df['date'] = new_df['date'].apply(lambda x: x - pd.DateOffset(years=100) if x.year > 2024 else x)
    new_df['year'] = new_df['date'].dt.year
    new_df['month'] = new_df['date'].dt.month
    new_df['day'] = new_df['date'].dt.day

    return new_df[["year", "month", "day", "city", "country", "group1", "attack_type1", "wounded", "killed"]]


def concatenate_dataframes(normalized_df, new_df):
    concatenated_df = pd.concat([normalized_df, new_df], ignore_index=True)


    concatenated_df = concatenated_df.drop_duplicates(subset=["year", "month", "day", "city", "country"], keep='first')

    concatenated_df.reset_index(drop=True, inplace=True)

    for column in ["killed", "wounded", "group1", "attack_type1"]:
        if f"{column}_x" in concatenated_df.columns and f"{column}_y" in concatenated_df.columns:
            concatenated_df[column] = concatenated_df[f"{column}_x"].fillna(concatenated_df[f"{column}_y"])
            concatenated_df.drop(columns=[f"{column}_x", f"{column}_y"], inplace=True)
        elif f"{column}_x" in concatenated_df.columns:
            concatenated_df.rename(columns={f"{column}_x": column}, inplace=True)
        elif f"{column}_y" in concatenated_df.columns:
            concatenated_df.rename(columns={f"{column}_y": column}, inplace=True)

    concatenated_df["city"] = concatenated_df["city"].fillna("unknown")
    concatenated_df["region"] = concatenated_df["region"].fillna("unknown")
    concatenated_df["prov_state"] = concatenated_df["prov_state"].fillna("unknown")
    concatenated_df[['latitude', 'longitude']] = concatenated_df[['latitude', 'longitude']].fillna(0)
    concatenated_df = concatenated_df.replace({np.nan: None})
    return concatenated_df


def normalize_and_concat(csv_path, new_csv_path):
    normalized_df = load_and_normalize_main_csv(csv_path)
    new_df = load_and_preprocess_new_csv(new_csv_path)
    concat_dfs = concatenate_dataframes(normalized_df, new_df)
    return concat_dfs
