from flask import Blueprint, jsonify

from app_data.repository.event_repository import get_all_countries_from_db

countries_bp = Blueprint('countries', __name__)


@countries_bp.route('/countries', methods=['GET'])
def get_all_countries_api():
    # Get all countries from the database
    countries = get_all_countries_from_db()

    # Convert countries to a list of dictionaries
    countries_list = [country.country_name for country in countries]

    # Return the countries as JSON
    return jsonify(countries_list), 200