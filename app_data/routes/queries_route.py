from datetime import datetime
from flask import Blueprint, send_file, request, Response, jsonify

from app_data.repository.queries import get_deadliest_attack_types, get_top_terror_groups

statistics_bp = Blueprint('statistics', __name__)


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