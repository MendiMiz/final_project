from flask import Blueprint, jsonify

from app_maps.api.statistics_1_api import fetch_victims_data_by_region, \
    fetch_region_attacks_percentage_changes_over_years, fetch_top_terror_groups_x_region
from app_maps.service.maps_service1 import create_map, country_coordinates, region_coordinates, \
    create_map_changes_over_year, create_terror_group_map, create_map_most_attacked_targets

statistics_maps_bp = Blueprint('statistics_maps', __name__)

@statistics_maps_bp.route('/average-casualties-by/<string:location_type>/<string:mode>', methods=['GET'])
def get_average_casualties_by_region_endpoint(location_type, mode):
    try:
        data = fetch_victims_data_by_region(location_type, mode)
        print(data)
        html_map = create_map(data, country_coordinates, region_coordinates)
        return html_map

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@statistics_maps_bp.route('/region_attacks_percentage_changes/<string:top_or_all>', methods=['GET'])
def region_attacks_percentage_changes(top_or_all):
    try:
        data = fetch_region_attacks_percentage_changes_over_years(top_or_all)
        html_map = create_map_changes_over_year(data, region_coordinates)
        return html_map

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@statistics_maps_bp.route('/top5_terror_groups_x_region', methods=['GET'])
def top5_terror_groups_x_region():
    try:
        data = fetch_top_terror_groups_x_region()
        html_map = create_terror_group_map(data, region_coordinates)
        return html_map

    except Exception as e:
        return jsonify({'message': str(e)}), 500

