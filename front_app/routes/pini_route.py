from flask import Blueprint, send_file, request, Response, jsonify

from front_app.api.statistics_1_api import fetch_victims_data_by_region, fetch_victims_data_by_country, \
    fetch_region_attacks_percentage_changes_over_years, fetch_top_terror_groups_x_region
from front_app.service.maps_service import create_map, country_coordinates, region_coordinates, \
    create_map_changes_over_year, create_terror_group_map

statistics_maps_bp = Blueprint('statistics_maps', __name__)

@statistics_maps_bp.route('/average-casualties-by/<string:location_type>/<string:mode>', methods=['GET'])
def get_average_casualties_by_region_endpoint(location_type, mode):
    try:
        data = fetch_victims_data_by_region(location_type, mode)
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