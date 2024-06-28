import sqlite3
import logging
import pandas as pd

logger = logging.getLogger("power_plants")


# This class will handle the DB operations.
# - Creating and dropping the main table
# - Inserting data from a dataaset provided
# - Selecting one or more plants, based on the state, the plant_id or coordinates
class DbService:
    def __init__(self):
        self.con = sqlite3.connect("power_plants.db")
        self.cur = self.con.cursor()
        self.clean_db()
        self.initialize_db()

    def initialize_db(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS power_plants (
                plant_id INTEGER PRIMARY KEY,
                plant_name TEXT,
                state TEXT,
                latitude REAL,
                longitude REAL,
                annual_net_generation REAL,
                annual_net_generation_percentage REAL
            );
        """
        )
        logger.debug("DB initialized")

    def clean_db(self):
        self.cur.execute("DROP TABLE IF EXISTS power_plants")
        logger.debug("DB cleaned")

    def insert_plants(self, plants_data):
        """
        Insert the plant data into the DB
        Args:
            plants_data (DataFrame): The plant data to be inserted
        """
        plants_data.to_sql("power_plants", self.con, if_exists="append", index=False)

    def get_plant(self, plant_id: int) -> dict:
        """
        Get the plant data for the given plant_id
        Args:
            plant_id (str): The plant_id to search for
        Returns:
            dict: The plant data
        """
        query = """
            SELECT 
                plant_id, plant_name, state, latitude, longitude, 
                annual_net_generation, annual_net_generation_percentage 
            FROM power_plants 
            WHERE plant_id = ? """
        results = pd.read_sql_query(query, self.con, params=[plant_id])
        logger.info(f"{len(results)} results found for plant_id: {plant_id}")
        return results.to_dict(orient="records")

    def get_plants(self, state) -> dict:
        """
        Get the plant data for the given state
        Args:
            state (str): The state to search for
        Returns:
            dict: The plants data
        """
        query = """
            SELECT 
                plant_id, plant_name, state, latitude, longitude, 
                annual_net_generation, annual_net_generation_percentage
            FROM power_plants 
            WHERE state = ?"""
        results = pd.read_sql_query(query, self.con, params=[state])
        logger.info(f"{len(results)} results found for state: {state}")
        return results.to_dict(orient="records")

    def get_plants_in_area(self, latitude, longitude, radius) -> dict:
        """
        Get the plant data for the given latitude, longitude, and radius
        Args:
            latitude (str): The latitude to search for
            longitude (str): The longitude to search for
            radius (str): The radius to search for
        Returns:
            dict: The plants data
        """
        query = """
            SELECT 
                plant_id, plant_name, state, latitude, longitude, 
                annual_net_generation, annual_net_generation_percentage
            FROM power_plants 
            WHERE 
                latitude BETWEEN ? AND ? AND 
                longitude BETWEEN ? AND ?"""
        results = pd.read_sql_query(
            query,
            self.con,
            params=[
                float(latitude) - float(radius),
                float(latitude) + float(radius),
                float(longitude) - float(radius),
                float(longitude) + float(radius),
            ],
        )
        logger.info(
            f"{len(results)} results found for latitude: {latitude}, longitude: {longitude}, and radius: {radius}"
        )
        return results.to_dict(orient="records")
