import pandas as pd
from parser import XMLParser, DataFrameColumnRenamer, DataFrameProcessor, ExcelExporter
import os
from datetime import datetime

# The path from where we get the config data
FOLDER_PATH = '/Users/aleksandarmatev/Desktop/Configurations'

# Dictionary that stores columns mapping. Keys are the old column names; Values are the new column names.
COLUMNS_MAP = {'description': 'Device Name', 'name': 'Port ID', 'encapsulation': 'Is the port available?'}

# Xpath to query the xml tree
XPATHS = '/configuration/interfaces/interface'

# Export path for the .xlsx file
EXPORT_PATH = '/Users/aleksandarmatev/Desktop'

# Columns that we want to process
COLUMNS = ['name', 'description', 'encapsulation']


def process_file(file_path: str):
    """
    Process a file and returns a DataFrame with the processed data.

    Parameters:
        file_path (str): The path of the file to be processed.

    Returns:
        DataFrame: The processed dataframe.

    Raises:
        ValueError: If the file path is not a string.
        FileNotFoundError: If the file does not exist at the specified path.
    """
    # Check if the file_path is a string
    if not isinstance(file_path, str):
        raise ValueError("file_path must be a string.")

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Create an XMLParser object and get the XML tree of the file
    parser = XMLParser(file_path, XPATHS).get_XMLtree(COLUMNS)

    # Create a DataFrameProcessor object and populate the used_ports column
    df_processor = DataFrameProcessor()
    df_processor.populate_used_ports_column(parser)

    # Create a DataFrameColumnRenamer object and rename the columns
    renamer = DataFrameColumnRenamer()
    renamer.rename_columns(parser, COLUMNS_MAP)

    return parser


if __name__ == '__main__':
    # Get the current date and time
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y-%H-%M-%S")

    # Create the file name for the exported xlsx file
    file_name = date_time + ".xlsx"
    export_path = os.path.join(EXPORT_PATH, file_name)

    # Create an empty dataframe
    final_df = pd.DataFrame()

    # Loop through all files in the FOLDER_PATH
    for filename in os.listdir(FOLDER_PATH):
        # Check if the file has the .txt or .xml extension
        if filename.endswith(".txt") or filename.endswith(".xml"):
            # Create the filepath by joining the FOLDER_PATH and the filename
            filepath = os.path.join(FOLDER_PATH, filename)
            # Process the file and concatenate it with the final dataframe
            final_df = pd.concat([final_df, process_file(filepath)], ignore_index=True)

    # Create an ExcelExporter object and export the final dataframe to the specified xlsx file
    exporter = ExcelExporter(final_df, export_path)
    exporter.export_columns_to_xlsx()
