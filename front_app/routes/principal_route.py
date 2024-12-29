from flask import Blueprint, render_template

main_page_bp = Blueprint('main', __name__)

@main_page_bp.route('/maps', methods=['GET'])
def show_maps():
    return render_template("index.html")
