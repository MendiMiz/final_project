import os
from dotenv import load_dotenv
from flask import Flask

from app_maps.routes.principal_route import main_page_bp
from app_maps.routes.statistics_1_route import statistics_maps_bp
from app_maps.routes.statistics_2_route import statistics_maps_bp2

load_dotenv(verbose=True)

app = Flask(__name__)

app.register_blueprint(statistics_maps_bp, url_prefix='/statistics_maps')
app.register_blueprint(statistics_maps_bp2, url_prefix='/statistics_maps2')
app.register_blueprint(main_page_bp, url_prefix='/main')

if __name__ == '__main__':
        app.run(port=5010, debug=True)