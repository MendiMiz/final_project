import os
from dotenv import load_dotenv
from flask import Flask
from front_app.routes.pini_route import statistics_maps_bp

load_dotenv(verbose=True)

app = Flask(__name__)

app.register_blueprint(statistics_maps_bp, url_prefix='/statistics_maps')

if __name__ == '__main__':
        app.run(port=5010, debug=True)