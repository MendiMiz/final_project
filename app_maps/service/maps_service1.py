import folium

region_coordinates = {
    "East Asia": (35.0, 105.0),
    "Sub-Saharan Africa": (-3.0, 30.0),
    "South Asia": (20.0, 80.0),
    "North America": (37.0, -100.0),
    "Central Asia": (39.0, 65.0),
    "Middle East & North Africa": (25.0, 45.0),
    "Central America & Caribbean": (13.0, -83.0),
    "Southeast Asia": (10.0, 105.0),
    "Eastern Europe": (50.0, 30.0),
    "South America": (-15.0, -60.0),
    "Australasia & Oceania": (-25.0, 135.0),
    "Western Europe": (50.0, -10.0)
}


country_coordinates = {
    'Sri Lanka (Ceylon)': (7.8731, 80.7718),
    'South Vietnam': (10.8231, 106.6297),
    'Barbados': (13.1939, -59.5432),
    'Serbia': (44.016521, 21.005859),
    'Brunei': (4.535277, 114.727669),
    'New Zealand': (-40.900557, 174.885971),
    'Poland': (51.919438, 19.145136),
    'Turkey': (38.963745, 35.243322),
    'Philippines': (12.8797, 121.774),
    'Egypt': (26.820553, 30.802498),
    'Iraq': (33.223191, 43.679291),
    'Argentina': (-38.416097, -63.616672),
    'Ethiopia': (9.145, 40.489673),
    'Austria': (47.516231, 14.550072),
    'Yemen': (15.552067, 48.516388),
    'Georgia': (42.315407, 43.356892),
    'Haiti': (18.971187, -72.285215),
    'Macedonia': (41.608635, 21.745275),
    'Taiwan': (23.6978, 120.9605),
    'Dominican Republic': (18.735693, -70.162651),
    'Cambodia': (12.565679, 104.990963),
    'Nicaragua': (12.865416, -85.207229),
    'French Guiana': (3.9339, -53.1258),
    'Czech Republic': (49.817492, 15.472962),
    'Guinea-Bissau': (11.803749, -15.180413),
    'Burkina Faso': (12.238333, -1.561593),
    'Soviet Union': (55.7558, 37.6176),  # Approximate center of former USSR
    'Kazakhstan': (48.019573, 66.923684),
    'West Bank and Gaza Strip': (31.943, 35.3105),
    'New Caledonia': (-20.904305, 165.618042),
    'Somalia': (5.152149, 46.199616),
    'Kyrgyzstan': (41.20438, 74.766098),
    'Japan': (36.204824, 138.252924),
    'Mauritius': (-20.348404, 57.552152),
    'Indonesia': (-0.7893, 113.9213),
    'Montenegro': (42.708678, 19.37439),
    'Gambia': (13.4432, -15.3102),
    'Falkland Islands': (-51.7963, -59.5236),
    'Seychelles': (-4.679574, 55.491977),
    'Sierra Leone': (8.460555, -11.779889),
    'Nigeria': (9.082, 8.6753),
    'Bolivia': (-16.290154, -63.588653),
    'Netherlands': (52.3784, 4.9009),
    'Chad': (15.4542, 18.7322),
    'Chile': (-35.675147, -71.542969),
    'Zaire': (-4.038333, 21.758664),  # Now the DRC, known as Zaire in past
    'Bahrain': (25.9304, 50.6378),
    'United States': (37.0902, -95.7129),
    'Australia': (-25.274398, 133.775136),
    'International': (0, 0),  # No specific location
    'Sri Lanka': (7.8731, 80.7718),
    'Togo': (8.6195, 0.8248),
    'South Korea': (35.907757, 127.766922),
    'Bangladesh': (23.685, 90.3563),
    'Albania': (41.1533, 20.1683),
    'Benin': (9.3075, 2.3158),
    'North Korea': (40.3399, 127.5101),
    'Venezuela': (6.4238, -66.5897),
    'Bahamas': (25.0343, -77.3963),
    'Iceland': (64.9631, -19.0208),
    'French Polynesia': (-17.6797, -149.4068),
    'Ivory Coast': (7.539989, -5.54708),
    'Yugoslavia': (44.016521, 21.005859),  # Former Yugoslavia region (Serbia as center)
    'Tajikistan': (38.861034, 71.276093),
    'Solomon Islands': (-29.1584, 152.2683),
    'Turkmenistan': (38.9697, 59.5563),
    'Jordan': (30.802498, 36.16589),
    'Switzerland': (46.8182, 8.2275),
    'Papua New Guinea': (-6.314993, 143.95555),
    'Canada': (56.1304, -106.3468),
    'Vatican City': (41.9029, 12.4534),
    'Ireland': (53.1424, -7.6921),
    'France': (46.603354, 1.888334),
    'Cyprus': (35.126413, 33.429859),
    'Guyana': (4.860416, -58.93018),
    'Portugal': (39.399872, -8.224454),
    'Thailand': (15.870032, 100.992541),
    'Republic of the Congo': (-4.4384, 15.2663),
    'Iran': (32.427908, 53.688046),
    'Senegal': (14.4974, -14.4524),
    'Laos': (19.85627, 102.495496),
    'Hungary': (47.1625, 19.5033),
    "People's Republic of the Congo": (-4.4384, 15.2663),
    'Spain': (40.463667, -3.74922),
    'Colombia': (4.570868, -74.297333),
    'St. Lucia': (13.9094, -60.9789),
    'Jamaica': (18.1096, -77.2975),
    'Kenya': (-0.0236, 37.9062),
    'Moldova': (47.0105, 28.8638),
    'St. Kitts and Nevis': (17.357822, -62.7837),
    'Russia': (55.7558, 37.6176),
    'Rwanda': (-1.9403, 29.8739),
    'Qatar': (25.3548, 51.1839),
    'Lebanon': (33.8547, 35.8623),
    'Kuwait': (29.3759, 47.9774),
    'Malaysia': (4.2105, 101.9758),
    'Dominica': (15.415, -61.371),
    'Algeria': (28.0339, 1.6596),
    'Afghanistan': (33.93911, 67.709953),
    'Uruguay': (-32.522779, -55.765832),
    'Eritrea': (15.1794, 39.7823),
    'Djibouti': (11.8251, 42.5903),
    'Fiji': (-16.578193, 179.414413),
    'Mozambique': (-18.665695, 35.529562),
    'Guadeloupe': (16.995, -62.0677),
    'Hong Kong': (22.3193, 114.1694),
    'Macau': (22.1987, 113.5439),
    'Western Sahara': (24.2155, -12.885),
    'South Yemen': (12.8654, 44.2075),  # Former Yemen (South Yemen part)
    'Lithuania': (55.1694, 23.8813),
    'Ecuador': (-1.8312, -78.1834),
    'Tunisia': (33.8869, 9.5375),
    'Belgium': (50.8503, 4.3517),
    'Peru': (-9.19, -75.0152),
    'Mali': (17.570692, -3.996166),
    'Czechia': (49.817492, 15.472962),
    'South Africa': (-30.5595, 22.9375),
    'Cuba': (21.521757, -77.781167),
    'Malta': (35.9375, 14.3754),
    'Angola': (-11.2027, 17.8739),
    'Tanzania': (-6.369028, 34.888822),
    'Liberia': (6.4281, -9.4295),
    'Uganda': (1.3733, 32.2903),
    'Syria': (34.802075, 38.996815),
    'Gabon': (-0.803689, 11.609444),
    'Cameroon': (5.938, 10.1591),
    'Burundi': (-3.3731, 29.9189),
    'Guatemala': (15.7835, -90.2308),
    'South Sudan': (6.877, 31.307),
    'Nepal': (28.3949, 84.124),
    'Israel': (31.9686, 35.8497),
    'Honduras': (13.9094, -83.4247),
    'Malawi': (-13.254308, 34.301525),
    'Singapore': (1.3521, 103.8198),
    'Mexico': (23.6345, -102.5528),
    'Vietnam': (14.0583, 108.2772),
    'Sudan': (12.8628, 30.802498),
    'Guinea': (9.9456, -9.6966),
    'Belize': (17.189877, -88.49765),
    'Norway': (60.472, 8.4689),
    'Greece': (39.0742, 21.8243),
    'Bulgaria': (42.733883, 25.48583),
    'Denmark': (56.2639, 9.5018),
    'Finland': (61.9241, 25.7482)
}

def create_map(data, city_coords, region_coords):
    print("Preparing the HTML map...")

    # Initialize the map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define a function to determine the color based on casualties_average
    def get_color(average):
        if average < 10:
            return 'green'
        elif average < 30:
            return 'orange'
        return 'red'

    # Check if data contains 'region' or 'country'
    location_type = 'region' if 'region' in data[0] else 'country'

    # Add Markers with custom icons
    [
        folium.Marker(
            location=(region_coords.get(row.get(location_type), (None, None)) if location_type == 'region' else city_coords.get(row.get(location_type), (None, None))),
            icon=folium.Icon(
                color=get_color(float(row['avg_victims'])),
                icon='info-sign'  # Use a nice marker icon
            ),
            popup=folium.Popup(
                f"<b>{row[location_type]}</b><br>"
                f"Average Casualties: {float(row['avg_victims'])}",
                max_width=300
            )
        ).add_to(m)
        for row in data if city_coords.get(row.get(location_type)) or region_coords.get(row.get(location_type))  # Ensure valid coordinates
    ]

    return m._repr_html_()


def create_map_changes_over_year(data, region_coords):
    print("Preparing the HTML map with percentage changes...")

    # Initialize the map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define a function to determine the marker color
    def get_color(percentage_change):
        if percentage_change is None:
            return 'gray'  # Unknown data
        elif percentage_change < 0:
            return 'blue'  # Decrease in attacks
        elif percentage_change < 10:
            return 'green'  # Small increase
        elif percentage_change < 30:
            return 'orange'  # Moderate increase
        return 'red'  # Significant increase

    # Iterate over regions in the data
    for region_data in data:
        region_name = region_data['region']
        changes = region_data['changes']

        # Build popup content
        popup_content = f"<b>{region_name}</b><br>"
        for change in changes:
            year = change['year']
            percentage_change = change['percentage_change']
            if percentage_change is not None:
                popup_content += f"Year: {year}, Change: {percentage_change:.2f}%<br>"
            else:
                popup_content += f"Year: {year}, Change: N/A<br>"

        # Get region coordinates
        coords = region_coords.get(region_name, (None, None))

        # Add marker if coordinates are valid
        if coords != (None, None):
            folium.Marker(
                location=coords,
                icon=folium.Icon(
                    color=get_color(changes[-1]['percentage_change']),  # Color based on the latest year's change
                    icon='info-sign'
                ),
                popup=folium.Popup(popup_content, max_width=300)
            ).add_to(m)

    return m._repr_html_()


def create_terror_group_map(data, region_coords):
    print("Preparing the HTML map for terror group attack quantities...")

    # Initialize the map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define a function to determine the marker color based on attack quantity
    def get_color(attacks_quantity):
        if attacks_quantity < 500:
            return 'blue'  # Low number of attacks
        elif attacks_quantity < 1000:
            return 'green'  # Moderate number of attacks
        elif attacks_quantity < 2000:
            return 'orange'  # High number of attacks
        return 'red'  # Very high number of attacks

    # Iterate over regions in the data
    for region_data in data:
        region_name = region_data['region']
        terror_groups = region_data['terror_groups']

        # Build popup content
        popup_content = f"<b>{region_name}</b><br>"
        for group in terror_groups:
            name = group['name']
            attacks_quantity = group['attacks_quantity']
            popup_content += f"{name}: {attacks_quantity} attacks<br>"

        # Get region coordinates
        coords = region_coords.get(region_name, (None, None))

        # Add marker if coordinates are valid
        if coords != (None, None):
            folium.Marker(
                location=coords,
                icon=folium.Icon(
                    color=get_color(terror_groups[0]['attacks_quantity']),  # Color based on the highest attack quantity in the region
                    icon='info-sign'
                ),
                popup=folium.Popup(popup_content, max_width=300)
            ).add_to(m)

    return m._repr_html_()


def create_map_most_attacked_targets(data, location_coords, mode="region"):
    """
    Creates a folium map for visualizing terrorist activity data based on regions or countries.

    Parameters:
    - data: List of dictionaries containing "region" or "country", "target_type_name", and "groups_involved".
    - location_coords: Dictionary mapping regions or countries to their coordinates.
    - mode: "region" or "country" to specify the level of visualization.
    """
    print(f"Preparing the HTML map for {mode}-level terrorist activity...")

    # Initialize the map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define a function to determine marker color based on the number of groups
    def get_color(num_groups):
        if num_groups < 10:
            return 'blue'  # Few groups
        elif num_groups < 30:
            return 'green'  # Moderate groups
        elif num_groups < 50:
            return 'orange'  # Many groups
        return 'red'  # Very high groups

    # Iterate over each location in the data
    for entry in data:
        location_name = entry[mode]
        target_type = entry['target_type_name']
        groups_involved = entry['groups_involved']
        num_groups = len(groups_involved)

        # Build popup content
        popup_content = f"<b>{location_name}</b><br>"
        popup_content += f"<b>Target Type:</b> {target_type}<br>"
        popup_content += f"<b>Groups Involved:</b> {num_groups}<br>"
        popup_content += "<ul>"
        for group in groups_involved:
            popup_content += f"<li>{group}</li>"
        popup_content += "</ul>"

        # Get coordinates for the location
        coords = location_coords.get(location_name, (None, None))

        # Add marker if coordinates are valid
        if coords != (None, None):
            folium.Marker(
                location=coords,
                icon=folium.Icon(color=get_color(num_groups), icon='info-sign'),
                popup=folium.Popup(popup_content, max_width=300, max_height=300)
            ).add_to(m)

    return m._repr_html_()


def create_map_terror_groups_x_region(data, location_coords, mode="region"):
    """
    Creates a folium map for visualizing terrorist activity data based on regions or countries.

    Parameters:
    - data: List of dictionaries containing "region" or "country", "target_type_name", and "groups_involved".
    - location_coords: Dictionary mapping regions or countries to their coordinates.
    - mode: "region" or "country" to specify the level of visualization.
    """
    print(f"Preparing the HTML map for {mode}-level terrorist activity...")

    # Initialize the map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define a function to determine marker color based on the number of groups
    def get_color(num_groups):
        if num_groups < 10:
            return 'blue'  # Few groups
        elif num_groups < 30:
            return 'green'  # Moderate groups
        elif num_groups < 50:
            return 'orange'  # Many groups
        return 'red'  # Very high groups

    # Iterate over each location in the data
    for entry in data:
        location_name = entry["location_name"]
        group_count = entry["group_count"]
        group_names = entry["group_names"]
        num_groups = len(group_names)

        # Build popup content
        popup_content = f"<b>{location_name}</b><br>"
        popup_content += f"<b>Group Count:</b> {group_count}<br>"
        popup_content += "<ul>"
        for group in group_names:
            popup_content += f"<li>{group}</li>"
        popup_content += "</ul>"

        # Get coordinates for the location
        coords = location_coords.get(location_name, (None, None))

        # Add marker if coordinates are valid
        if coords != (None, None):
            folium.Marker(
                location=coords,
                icon=folium.Icon(color=get_color(num_groups), icon='info-sign'),
                popup=folium.Popup(popup_content, max_width=300, max_height=300)
            ).add_to(m)

    return m._repr_html_()