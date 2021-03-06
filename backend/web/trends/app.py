import logging
import os
from logging.config import dictConfig

import yaml
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from trends.collectors.efir import EfirCollector
from trends.collectors.google import GoogleCollector
from trends.collectors.videos import VideosCollector
from trends.db import create_engine
from trends.handlers.trends import trends
from trends.models.trends_repo import Repository
from trends.utils.get_db_environ import get_environ_or_default

my_ip = "127.0.0.1"
CURRENT_DIR = os.path.dirname(__file__)
SWAGGER_URL = "/swagger"

API_URL = "/static/swagger.yaml"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Efir Trends"}
)


def setup_logging(path=os.path.join(CURRENT_DIR, "logging.yaml")):
    try:
        with open(path, "rt") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

    except FileNotFoundError as e:
        logging.warning(e)
        logging.warning("Error in logging configuration. Using default")
        logging.basicConfig(level=logging.INFO)


def create_app(db_url):
    setup_logging()
    logger = logging.getLogger("trends")
    logger.debug("About to create service mixer")
    app = Flask(__name__)
    CORS(app)

    app.db = create_engine(db_url)
    app.register_blueprint(trends, url_prefix="/")
    return app


if __name__ == "__main__":
    # export DATABASE_URL=postgresql://me:hackme@0.0.0.0/trends
    db_url = get_environ_or_default(
        "DATABASE_URL", "postgresql://me:hackme@0.0.0.0/trends"
    )
    print("DATABASE_URL", db_url)

    app = create_app(db_url)
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    repo = Repository(app.db)
    collectors = [
        EfirCollector(
            repo,
            get_environ_or_default(
                "EFIR_URL", "http://{0}:8081/fetch/themes".format(my_ip)
            ),
        ),
        GoogleCollector(
            repo,
            get_environ_or_default("GOOGLE_URL", "http://{0}:8082/fetch".format(my_ip)),
        ),
        VideosCollector(
            repo,
            get_environ_or_default(
                "VIDEOS_URL", "http://{0}:8081/fetch/videos".format(my_ip)
            ),
        ),
    ]
    for c in collectors:
        c.start()

    app.run(host="0.0.0.0", port=8080)
