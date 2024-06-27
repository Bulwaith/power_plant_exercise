import sqlite3
import logging

logger = logging.getLogger("power_plants")
logger.setLevel(logging.DEBUG)


# This class will handle the DB operations.
# - Creating and dropping the main table
# - Inserting data from an array provided
# - Selecting one or more plants, with the coordinates
class DbService:
    def __init__(self):
        self.con = sqlite3.connect("plants.db")
        self.cur = self.con.cursor()
        self.initialize_db()

    def initialize_db(self):
        self.cur.execute(
            """
            CREATE TABLE power_plants (
                plant_id INTEGER PRIMARY KEY,
                plant_name TEXT,
                state TEXT,
                latitude REAL,
                longitude REAL,
                annual_net_generation REAL,
                state_total_generation REAL,
                percentage_of_state REAL
            );
        """
        )
        logger.debug("DB initialized")

    # def insert_plant(self, state):
    #     self.cur.executemany("REPLACE INTO power_plants VALUES(?, ?)", plant)
    #     self.con.commit()

    def get_plant(self, state: str):
        res = self.cur.execute(
            """
            SELECT 
                plant_id, plant_name, state, latitude, longitude, 
                annual_net_generation, state_total_generation, percentage_of_state 
            FROM power_plants 
            WHERE state = ? """,
            [state],
        )
        result = res.fetchone()
        if result and len(result) > 0:
            return result[1]
        return []

    def get_plants(self, state):
        res = self.cur.execute(
            """
            SELECT 
                plant_id, plant_name, state, latitude, longitude, 
                annual_net_generation, state_total_generation, percentage_of_state 
            FROM power_plants 
            WHERE state = ?""",
            [state],
        )
        return res.fetchall()

    def drop_table(self):
        self.cur.execute("DROP TABLE IF EXISTS power_plants")
