import os
from dotenv import load_dotenv
from flask import Flask
from app_data.routes.queries_route import statistics_bp

load_dotenv(verbose=True)

app = Flask(__name__)
app.register_blueprint(statistics_bp, url_prefix='/statistics')


if __name__ == '__main__':
        app.run()