from flask import Blueprint, jsonify
from app_data.repository.queries2 import get_top_targets_per_country, get_most_attacked_target_type_per_region, \
    get_groups_by_all_locations, get_group_cooperation, get_groups_with_common_targets_by_years

statistics_bp2 = Blueprint('statistics2', __name__)





@statistics_bp2.route('/most_attacked_target_type_by_region_or_country/<string:mode>', methods=['GET'])
def most_attacked_target_type_by_region_or_country(mode):
    if mode == 'country':
        data = get_top_targets_per_country()
    elif mode == 'region':
        data = get_most_attacked_target_type_per_region()
    else:
        return jsonify({"error": "Invalid mode. Please use 'country' or 'region'."}), 400

    return jsonify(data), 200

@statistics_bp2.route('/groups_by_all_locations/<string:region_or_country>', methods=['GET'])
def groups_by_all_locations(region_or_country):
    if region_or_country != 'region' and region_or_country != 'country':
        return jsonify({"error": "Invalid mode. Please use 'country' or 'region'."}), 400

    data = get_groups_by_all_locations(region_or_country)


    return jsonify(data), 200

@statistics_bp2.route('/groups_cooperation/', methods=['GET'])
def groups_cooperation():
    data = get_group_cooperation()
    return jsonify(data), 200

@statistics_bp2.route('/get_groups_with_common_targets/', methods=['GET'])
def get_groups_with_common_targets():
    data = get_groups_with_common_targets_by_years()
    return jsonify(data), 200



