from utils.database_operations import read_csv, utc_to_local
import pandas as pd

def data_init(csv_file1, csv_file2, csv_file3):
    """
    Initialize data from three CSV files.

    Args:
        csv_file1 (str): Path to the first CSV file.
        csv_file2 (str): Path to the second CSV file.
        csv_file3 (str): Path to the third CSV file.

    Returns:
        dict: A dictionary containing data read from the three CSV files.
            Keys: 'status_data', 'business_hours_data', 'timezone_data'.
    """
    return {
        "status_data": read_csv(file_path=csv_file1, key_column="store_id"),
        "business_hours_data": read_csv(file_path=csv_file2, key_column="store_id"),
        "timezone_data": read_csv(file_path=csv_file3, key_column="store_id")
    }
