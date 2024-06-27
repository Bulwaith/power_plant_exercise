import pandas as pd
import logging

pd.set_option("future.no_silent_downcasting", True)

logger = logging.getLogger("power_plants")


class FileService:
    def __init__(self, file_path, tab_name):
        self.file_path = f"app/{file_path}"
        self.tab_name = tab_name
        self.plants_data = None

    def read_and_process(self):
        """
        Read the file and process the data
        """

        logger.info(f"Reading the file {self.file_path} abd tab {self.tab_name}")
        # Load the provided Excel file
        self.plants_data = pd.ExcelFile(self.file_path)
        # Get the required tab from the file
        self.plants_data = self.plants_data.parse(self.tab_name)
        logger.info(f"Reading the file {self.file_path} abd tab {self.tab_name} - ✅")

        logger.info(f"Extracting and cleaning the data")
        logger.debug(
            f" ↪ Assuming the column 'Plant file sequence number' to be unique"
        )

        # Extract relevant columns and rename them for clarity
        relevant_columns = {
            "Plant file sequence number": "plant_id",
            "Plant name": "plant_name",
            "Plant state abbreviation": "state",
            "Plant latitude": "latitude",
            "Plant longitude": "longitude",
            "Plant annual net generation (MWh)": "annual_net_generation",
        }

        # Filter the columns
        self.plants_data = self.plants_data[relevant_columns.keys()]

        # Drop the first row, with the column name
        self.plants_data.drop(0, inplace=True)

        # Renaming with the better column names
        self.plants_data.columns = relevant_columns.values()

        # We do this later, after filtering on the columns
        self.plants_data.fillna(0, inplace=True)
        # Infer the data types - this is a performance optimization to avoid the warning
        self.plants_data = self.plants_data.infer_objects(copy=False)

        logger.info(f"Extracting and cleaning the data - ✅")

    def caldculate_percentages(self):
        """
        Calculate the annual net generation percentage for each plant
        """

        logger.info(f"Calculating the annual net generation percentage for each plant")
        total_annual_net_generation = self.plants_data["annual_net_generation"].sum()

        # Calculate the annual net generation percentage for each plant
        self.plants_data["annual_net_generation_percentage"] = (
            self.plants_data["annual_net_generation"]
            * 100
            / total_annual_net_generation
        )
        logger.info(
            f"Calculating the annual net generation percentage for each plant - ✅"
        )

    def health_checks(self) -> bool:
        """
        Run health checks on the data
            1) Check the total annual net generation % = 100
            2) Check the number of duplicates in the plant_id column to ensure they are unique
        """
        total_annual_percentage = self.plants_data[
            "annual_net_generation_percentage"
        ].sum()
        duplicates = self.plants_data.duplicated(subset=["plant_id"]).sum()
        logger.info("Health checks:")
        if round(total_annual_percentage) != 100:
            logger.warning(
                f"Total annual net generation percentage is not equal to 100, it is {round(total_annual_percentage)}"
            )
            return False
        logger.info(f"✸ Total percentage: {round(total_annual_percentage)}% - OK")

        if duplicates:
            logger.warning(
                f"Number of duplicates in the plant_id column: {duplicates}, they should be unique"
            )
            return False
        logger.info(f"✸ Duplicates in the plant_id column: {duplicates} - OK")

        logger.info("Health checks passed. Move on. ✅")
        return True
