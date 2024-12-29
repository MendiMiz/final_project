from flask import Blueprint, jsonify
from app_data.repository.insertion_repository import get_all_countries_from_db

countries_bp = Blueprint('countries', __name__)

@countries_bp.route('/countries', methods=['GET'])
def get_all_countries_api():
    countries = get_all_countries_from_db()

    countries_list = [country.country_name for country in countries]

    return jsonify(countries_list), 200