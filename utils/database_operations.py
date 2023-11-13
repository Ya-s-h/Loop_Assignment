import pandas as pd
from datetime import datetime
import pytz
from collections import defaultdict


def utc_to_local(utc_datetime_str, local_timezone_str):
    utc_datetime = datetime.strptime(utc_datetime_str, "%Y-%m-%d %H:%M:%S.%f %Z")
    utc_timezone = pytz.utc

    # Desired timezone
    desired_timezone = pytz.timezone(local_timezone_str)

    # Convert to the desired timezone
    converted_datetime = utc_timezone.localize(utc_datetime).astimezone(desired_timezone)

    return converted_datetime

def read_csv(file_path, key_column=None):
    """
    Read CSV data from the specified file.

    Args:
        file_path (str): The path to the CSV file.
        key_column (str, optional): The column to use as keys in the dictionary.

    Returns:
        pd.DataFrame or None: If key_column is provided, a DataFrame with filtered data.
                              If record_value is provided, a DataFrame with a single record.
                              Otherwise, the entire DataFrame.
    """
    try:
        data = pd.read_csv(file_path)

        if key_column:
                # Returning DataFrame grouped by specific key_column
                return data.groupby(key_column).apply(lambda x: x).reset_index(drop=True)
        else:
            # Returning the entire DataFrame
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading CSV: {e}")

    return pd.DataFrame() if key_column else pd.DataFrame()


# Example usage:
store_id_to_check = 1371971221718848145

# print(data_initialization()["status_data"][0])
