from dotenv import load_dotenv
from flask import Flask

from app_data.routes.countries_route import countries_bp
from app_data.routes.queries2_route import statistics_bp2
from app_data.routes.queries1_route import statistics_bp
from app_data.service.data_normalization_and_concat_service import normalize_and_concat
from app_data.service.insertion_service import insert_from_dataframe, main_csv_path, csv_to_merge

load_dotenv(verbose=True)

app = Flask(__name__)
app.register_blueprint(statistics_bp, url_prefix='/statistics')
app.register_blueprint(statistics_bp2, url_prefix='/statistics2')
app.register_blueprint(countries_bp, url_prefix='/countries')


if __name__ == '__main__':
        app.run(debug=True)
        concat_data = normalize_and_concat(main_csv_path, csv_to_merge)
        insert_from_dataframe(concat_data)