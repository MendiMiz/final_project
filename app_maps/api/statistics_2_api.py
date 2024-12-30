from app_maps.api.statistics_1_api import fetch_url


def fetch_region_or_country_most_attacked_target_type(mode):
    url = f'http://localhost:5000/statistics2/most_attacked_target_type_by_region_or_country/{mode}'
    return fetch_url(url)

def fetch_terror_groups_by_all_locations(region_or_country):
    url = f'http://localhost:5000/statistics2/groups_by_all_locations/{region_or_country}'
    return fetch_url(url)
