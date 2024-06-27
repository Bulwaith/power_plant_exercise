import pandas as pd
import logging
import sys

pd.set_option("future.no_silent_downcasting", True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a StreamHandler for outputting to the console
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)

# Optional: Format the log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

SHEET_NAME = "PLNT22"

logger.info("Starting the application")
# Load the provided Excel file
file_path = "app/egrid2022_data.xlsx"
logger.info(f"Extracting the data from the sheet: {SHEET_NAME}, file: {file_path}")
excel_data = pd.ExcelFile(file_path)

# Get the required sheet from the file
df = excel_data.parse(SHEET_NAME)

logger.info(f"Assuming the column 'Plant file sequence number' to be unique")

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
df = df[relevant_columns.keys()]

# Drop the first row, with the column name
df = df.drop(0)

# Renaming with the better column names
df.columns = relevant_columns.values()


# We do this later, after filtering on the columns
df.fillna(0, inplace=True)
df = df.infer_objects(copy=False)

total_annual_net_generation = df["annual_net_generation"].sum()

# Calculate the annual net generation percentage for each plant
df["annual_net_generation_percentage"] = (
    df["annual_net_generation"] * 100 / total_annual_net_generation
)

# Health checks:
# 1) Check the total annual net generation % = 100
# 2) Check the number of duplicates in the plant_id column to ensure they are unique
total_annual_percentage = df["annual_net_generation_percentage"].sum()
duplicates = df.duplicated(subset=["plant_id"]).sum()
logger.info("⛑️ Health checks:")
if round(total_annual_percentage) != 100:
    logger.warning(
        f"Total annual net generation percentage is not equal to 100, it is {round(total_annual_percentage)}"
    )
logger.info(f"✸ Total percentage: {round(total_annual_percentage)}% ✅")
if duplicates:
    logger.warning(
        f"Number of duplicates in the plant_id column: {duplicates}, they should be unique"
    )
logger.info(f"✸ Duplicates in the plant_id column: {duplicates} ✅")
logger.info("✅ Health checks passed. Moving on.")
