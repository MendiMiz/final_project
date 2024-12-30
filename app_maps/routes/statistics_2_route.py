from flask import Blueprint, jsonify

from app_maps.api.statistics_2_api import fetch_region_or_country_most_attacked_target_type, \
    fetch_terror_groups_by_all_locations
from app_maps.service.maps_service1 import country_coordinates, region_coordinates, \
    create_map_changes_over_year, create_terror_group_map, create_map_most_attacked_targets, \
    create_map_terror_groups_x_region

statistics_maps_bp2 = Blueprint('statistics_maps2', __name__)


@statistics_maps_bp2.route('/most_attacked_target_type/<string:region_or_country>', methods=['GET'])
def most_attacked_target_type(region_or_country):
    try:
        if region_or_country != 'country' and region_or_country != 'region':
            return jsonify({'message': 'Invalid input. Write "region" or "country"'}), 400

        coordinates = country_coordinates if region_or_country == 'country' else region_coordinates
        data = fetch_region_or_country_most_attacked_target_type(region_or_country)
        html_map = create_map_most_attacked_targets(data, coordinates, region_or_country)
        return html_map

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@statistics_maps_bp2.route('/terror_groups_by_all_locations/<string:region_or_country>', methods=['GET'])
def terror_groups_by_all_locations(region_or_country):
    try:
        if region_or_country != 'country' and region_or_country != 'region':
            return jsonify({'message': 'Invalid input. Write "region" or "country"'}), 400

        coordinates = country_coordinates if region_or_country == 'country' else region_coordinates
        data = fetch_terror_groups_by_all_locations(region_or_country)
        html_map = create_map_terror_groups_x_region(data, coordinates, region_or_country)
        return html_map

    except Exception as e:
        return jsonify({'message': str(e)}), 500