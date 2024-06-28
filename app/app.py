from flask import Flask, jsonify, request
import logging
import sys
import os
import colorlog

from services.database_service import DbService
from services.file_service import FileService

logger = logging.getLogger("power_plants")

# Some standard logger formatting and customization
# create logger
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = colorlog.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = colorlog.ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

app = Flask(__name__)
db_service = DbService()

# Load the environment variables to get the file name and tab name
PLANT_FILENAME = os.getenv("PLANT_FILENAME", "egrid2022_data.xlsx")
TAB_NAME = os.getenv("TAB_NAME", "PLNT22")
IGNORE_HEALTH_CHECKS = os.getenv("IGNORE_HEALTH_CHECKS", True)


try:
    logger.info("Starting the application")
    file_service = FileService(PLANT_FILENAME, TAB_NAME)
    file_service.read_and_process()
    file_service.caldculate_percentages()

    health_checks = file_service.health_checks()

    if not IGNORE_HEALTH_CHECKS and health_checks:
        logger.error("Health checks failed")
        raise Exception("Health checks failed")

    db_service.insert_plants(file_service.get_plant_data())

    logger.info("Data inserted successfully. Waiting for requests ✅")
except Exception as e:
    logger.error(f"Error: {e}")
    raise e


@app.route("/")
def hello_world():
    """
    A simple hello world endpoint, with the list of available queries
    """
    queries = {
        "get_plants": "/get-plants/<state>",
        "get_plant": "/get-plant/<plant_id>",
        "get_plants_in_area": "/get-plants-in-area?latitude=<latitude>&longitude=<longitude>&radius=<radius>",
    }
    return jsonify(queries)


@app.route("/get-plants/<state>")
def get_plants(state):
    """
    Get the plant data for the given state
    Args:
        state (str): The state to search for
    Example: http://localhost:8000/get-plants/CA
    """
    logger.info(f"Getting plants for the state: {state.upper()}")
    data = db_service.get_plants(state)

    results = {
        "plants_data": data,
        "total_plants": len(data),
        "state": state,
    }
    return jsonify(results)


@app.route("/get-plant/<plant_id>")
def get_plant(plant_id):
    """
    Get the plant data for the given plant_id
    Args:
        plant_id (str): The plant_id to search for
    Example: http://localhost:8000/get-plant/300
    """
    logger.info(f"Getting plant for the plant_id: {plant_id}")
    data = db_service.get_plant(plant_id)

    results = {
        "plant_data": data,
        "total_plants": len(data),
        "plant_id": plant_id,
    }
    return jsonify(results)


@app.route("/get-plants-in-area")
def get_plants_in_area():
    """
    Get the plant data for the given latitude, longitude, and radius.
    Example: http://localhost:8000/get-plants-in-area?latitude=32&longitude=-111&radius=2
    """
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    radius = request.args.get("radius")

    logger.info(
        f"Getting plants in the area with latitude: {latitude}, longitude: {longitude}, and radius: {radius}"
    )
    data = db_service.get_plants_in_area(latitude, longitude, radius)

    results = {
        "plants_data": data,
        "total_plants": len(data),
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
    }
    return jsonify(results)
