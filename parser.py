from typing import List
import pandas as pd
import logging

# Configuring the logging module to log messages to a file named 'logfile.log'
# with a DEBUG level of logging and the log message format
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class XMLParser:
    def __init__(self, file_path: str, xpath: str):
        self.file_path = file_path
        self.xpath = xpath

    def get_XMLtree(self, columns: List[str] = None) -> pd.DataFrame:
        """
        Return the specified columns of the pandas dataframe from the XML content using the xpath
        """
        try:
            # Reading the XML file and creating a DataFrame
            df = pd.read_xml(self.file_path, xpath=self.xpath)
            if columns:
                # Selecting only the specified columns from the DataFrame
                df = df[columns]
            logging.debug("Dataframe generated successfully")
            return df
        except FileNotFoundError as e:
            # Handle the FileNotFoundError
            logging.exception("File not found: %s" % str(e))
            raise e
        except Exception as e:
            logging.exception(
                "An error occurred while getting the XML tree: %s. Inputs: file: %s, xpath: %s, columns: %s" % (
                    str(e), self.file_path, self.xpath, columns))
            raise e


class ExcelExporter:
    def __init__(self, dataframe: pd.DataFrame, export_path: str):
        self.dataframe = dataframe
        self.export_path = export_path

    def export_columns_to_xlsx(self):
        """
        Exports the XML data to an Excel file at the specified location.
        """
        try:
            # Removing any columns with all NaN values and saving the DataFrame to an Excel file
            df = self.dataframe
            df = df.dropna(axis=1, how='all')
            with pd.ExcelWriter(self.export_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                logging.debug("File exported successfully")
        except Exception as e:
            logging.exception("An error occurred while exporting columns to xlsx: %s with export_path: %s" %
                              (str(e), self.export_path))
            raise e


class DataFrameColumnRenamer:
    @staticmethod
    def rename_columns(df: pd.DataFrame, columns_map: dict, inplace: bool = True) -> None:
        """
        Renames columns in the dataframe by mapping old column names to new column names.
        :param df: DataFrame containing columns to be renamed
        :param columns_map: Dictionary with keys as old column names and values as new column names
        :param inplace: Boolean indicating whether to update the dataframe in place or return a new
        dataframe. Default is True.
        """
        try:
            if not isinstance(df, pd.DataFrame):
                raise TypeError("Input df should be a pandas DataFrame.")

            if not isinstance(columns_map, dict):
                raise TypeError("Input columns_map should be a dictionary.")

            if not all(isinstance(k, str) and isinstance(v, str) for k, v in columns_map.items()):
                raise ValueError("All keys and values in columns_map should be strings.")

            if not all(col in df.columns for col in columns_map.keys()):
                raise KeyError("All keys in columns_map should correspond to column names in df.")

            if not isinstance(inplace, bool):
                raise TypeError("inplace parameter should be boolean.")

            # Renaming the columns with the desired values
            df.rename(columns=columns_map, inplace=inplace)
            logging.debug("Columns renamed successfully")
        except Exception as e:
            logging.exception("Failed to rename columns with parameters: df: %s, columns_map: %s, inplace: %s. Error: "
                              "%s" % (df, columns_map, inplace, str(e)))
            raise e


class DataFrameProcessor:
    @staticmethod
    def populate_used_ports_column(df: pd.DataFrame, column_name: str = 'encapsulation',
                                   empty_values: str = 'Yes', non_empty_values: str = 'No'):
        """
            This function adjusts the rows of the 'encapsulation' column in the DataFrame returned by the
            get_XMLtree_for_second() function.
            It creates a boolean mask of non-null values and replaces the values in the 'encapsulation' column with
            'Yes' for non-null values and 'No' for null values.
            :param df: DataFrame containing columns to be modified
            :param column_name: Name of the column to be modified.
            :param empty_values: Value to be replaced with if the cell is empty.
            :param non_empty_values: Value to be replaced with if the cell is not empty.
            """
        try:
            if column_name not in df.columns:
                raise ValueError(f'{column_name} column not found in DataFrame.')
            df['Services on port'] = df[column_name]
            mask = df[column_name].notna()
            # Applying the mask
            df[column_name] = df[column_name].where(mask, other=empty_values)
            df[column_name] = df[column_name].where(~mask, other=non_empty_values)
            logging.debug("Dataframe returned successfully")
        except Exception as e:
            logging.exception(
                "An error occurred while populating used ports column: column_name: %s, empty_values: %s, "
                "non_empty_values: %s, %s'" % (column_name, empty_values, non_empty_values, str(e)))
            raise e

