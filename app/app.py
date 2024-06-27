from flask import Flask
import logging
import sys
import os

# from services.database_service import DbService
from services.file_service import FileService

logger = logging.getLogger("power_plants")

# Some standard logger formatting and customization
# create logger
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

app = Flask(__name__)

# Load the environment variables to get the file name and tab name
PLANT_FILENAME = os.getenv("PLANT_FILENAME", "egrid2022_data.xlsx")
TAB_NAME = os.getenv("TAB_NAME", "PLNT22")
IGNORE_HEALTH_CHECKS = os.getenv("IGNORE_HEALTH_CHECKS", False)


@app.route("/")
def hello_world():
    logger.info("Hello, World!!")
    return "Hello, World!!"


try:
    print("Starting the application")
    logger.info("Starting the application")
    file_service = FileService(PLANT_FILENAME, TAB_NAME)
    file_service.read_and_process()
    file_service.caldculate_percentages()

    health_checks = file_service.health_checks()

    if not IGNORE_HEALTH_CHECKS and health_checks:
        logger.error("Health checks failed")
        raise Exception("Health checks failed")

    # db_service = DbService()
    # db_service.insert_plant(file_service.plants_data.values)
except Exception as e:
    logger.error(f"Error: {e}")
    raise e
