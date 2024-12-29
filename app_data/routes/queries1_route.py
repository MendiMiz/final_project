from flask import Blueprint, send_file, request, Response, jsonify

from app_data.repository.queries1 import get_deadliest_attack_types, get_top_terror_groups, \
    get_most_active_groups_by_area, get_avg_victims_per_attack_by_region_try_map, \
    get_avg_victims_per_attack_by_country_try_map, get_percentage_change_in_attacks_by_region, \
    get_top5_terror_groups_by_region, get_top_5_active_groups_by_country

statistics_bp = Blueprint('statistics', __name__)


@statistics_bp.route('/avg_victims_by_region/<string:mode>', methods=['GET'])
def avg_victims_by_region(mode):
    data = get_avg_victims_per_attack_by_region_try_map(mode)
    return jsonify(data), 200


@statistics_bp.route('/avg_victims_by_country/<string:mode>', methods=['GET'])
def avg_victims_by_country(mode):
    data = get_avg_victims_per_attack_by_country_try_map(mode)
    return jsonify(data), 200


@statistics_bp.route('/years_percentage_change/<string:calc_type>', methods=['GET'])
def years_percentage_change(calc_type):
    data = get_percentage_change_in_attacks_by_region(calc_type)
    return jsonify(data), 200

@statistics_bp.route('/get_terrorist_groups_by_region', methods=['GET'])
def get_terrorist_groups_by_region():
    data = get_top5_terror_groups_by_region()
    return jsonify(data), 200


@statistics_bp.route('/deadliest_attack_types', methods=['GET'])
def deadliest_attack_types():
    try:
        deadliest_attack_types_list = get_deadliest_attack_types()

        if not deadliest_attack_types_list:
            return jsonify({"message": "No data found"}), 404

        formatted_result = [
            {"target_type": target, "attack_count": count} for target, count in deadliest_attack_types_list
        ]

        return jsonify(formatted_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@statistics_bp.route('/deadliest_attack_types/top5', methods=['GET'])
def top5_deadliest_attack_types():
    try:
        deadliest_attack_types_list_top5 = get_deadliest_attack_types()[0:5]

        if not deadliest_attack_types_list_top5:
            return jsonify({"message": "No data found"}), 404

        formatted_result = [
            {"target_type": target, "attack_count": count} for target, count in deadliest_attack_types_list_top5
        ]

        return jsonify(formatted_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@statistics_bp.route('/top_terror_groups', methods=['GET'])
def top_terror_groups():
    try:
        top_terror_groups_list = get_top_terror_groups()

        if not top_terror_groups_list:
            return jsonify({"message": "No data found"}), 404

        return jsonify(top_terror_groups_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@statistics_bp.route('/active_groups_by_area', methods=['GET'])
def active_groups_by_area():
    area_id = request.args.get('area_id')
    if not area_id:
        return jsonify({"error": "area_id is required"}), 400

    try:
        active_groups = get_most_active_groups_by_area(area_id)

        return jsonify(active_groups), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@statistics_bp.route('/top_5_active_groups_by_country', methods=['GET'])
def top_5_active_groups_by_country():
    top_groups = get_top_5_active_groups_by_country()

    return jsonify(top_groups), 200