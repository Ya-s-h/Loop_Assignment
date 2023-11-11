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
    
def read_csv(file_path, key_column=None, record_value=None):
    """
    Read CSV data from the specified file.

    Args:
        file_path (str): The path to the CSV file.
        key_column (str, optional): The column to use as keys in the dictionary.
        record_value (str, optional): The value to use for retrieving a specific record.

    Returns:
        pd.DataFrame or None: If key_column is provided, a DataFrame with filtered data.
                              If record_value is provided, a DataFrame with a single record.
                              Otherwise, the entire DataFrame.
    """
    try:
        data = pd.read_csv(file_path)

        if key_column:
            if record_value:
                # Returning all occurrences of record_value in key_column
                return data[data[key_column] == record_value]
            else:
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

def combine_data(store_id, status_data, business_hours_data, timezone_data):
    # Convert status_data to a DataFrame
    status_df = pd.DataFrame(status_data)

    # Getting timezone else setting timezone to America/Chicago as default
    timezone = timezone_data[0]['timezone_str'] if len(timezone_data) else "America/Chicago"

    # If business hours are empty, then consider the store open 24/7
    if len(business_hours_data) == 0:
        business_hours_data = [{"store_id": store_id, "day": day, 'start_time_local': '00:00:00', 'end_time_local': '23:59:59'} for day in range(7)]

    # Convert status_df timestamps to local timezone
    status_df["timestamp_local"] = status_df["timestamp_utc"].apply(lambda x: utc_to_local(x, timezone))

    # Merge business_hours_data and status_df based on the day
    business_hours_df = pd.DataFrame(business_hours_data)
    merged_data = pd.merge(business_hours_df, status_df, left_on=["store_id", "day"], right_on=["store_id", status_df["timestamp_local"].dt.weekday])

    # Select and reorder columns as needed
    merged_data = merged_data[["store_id", "day", "start_time_local", "end_time_local", "status", "timestamp_utc", "timestamp_local"]]

    print(merged_data)
    return merged_data

# Example usage:
store_id_to_check = 1371971221718848145
status_csv = 'status.csv'
business_hours_csv = 'Menu hours.csv'
timezone_csv = 'timezone.csv'

status_data = read_csv(file_path=status_csv, key_column="store_id", record_value=store_id_to_check)
business_hours_data = read_csv(file_path=business_hours_csv, key_column="store_id", record_value=store_id_to_check)
timezone_data = read_csv(file_path=timezone_csv, key_column="store_id", record_value=store_id_to_check)

# print(utc_to_local("2023-01-24 13:01:02.587792 UTC", "Asia/Kolkata"))
# print(read_csv(business_hours_csv, "store_id", 4229534553524953507))
combine_data(store_id_to_check, status_data, business_hours_data, timezone_data)
