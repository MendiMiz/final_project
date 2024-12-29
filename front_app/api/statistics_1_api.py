import requests

def fetch_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def fetch_victims_data_by_region(location_type, mode):
    url = f'http://localhost:5000/statistics/avg_victims_by_{location_type}/{mode}'
    return fetch_url(url)

def fetch_top_terror_groups_x_region():
    url = 'http://localhost:5000/statistics/get_terrorist_groups_by_region'
    return fetch_url(url)

def fetch_victims_data_by_country():
    url = 'http://localhost:5000/statistics/avg_victims_by_country'
    return fetch_url(url)

def fetch_region_attacks_percentage_changes_over_years(mode):
    url = f'http://localhost:5000/statistics/years_percentage_change/{mode}'
    return fetch_url(url)

