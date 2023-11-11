from database_operations import read_csv, utc_to_local
import pandas as pd

status_csv = 'status.csv'
business_hours_csv = 'Menu hours.csv'
timezone_csv = 'timezone.csv'


def data_init():
    return {"status_data" : read_csv(file_path=status_csv, key_column="store_id"),
    "business_hours_data" : read_csv(file_path=business_hours_csv, key_column="store_id"),
    "timezone_data" : read_csv(file_path=timezone_csv, key_column="store_id")
    }

def combine_data(store_id, status_data, business_hours_data, timezone):
    # Convert status_data to a DataFrame
    status_df = pd.DataFrame(status_data)

    # Convert status_df timestamps to local timezone
    status_df["timestamp_local"] = status_df["timestamp_utc"].apply(lambda x: utc_to_local(x, timezone))

    # Merge business_hours_data and status_df based on the day
    business_hours_df = pd.DataFrame(business_hours_data)
    merged_data = pd.merge(business_hours_df, status_df, left_on=["store_id", "day"], right_on=["store_id", status_df["timestamp_local"].dt.weekday])

    # Select and reorder columns as needed
    merged_data = merged_data[["store_id", "day", "start_time_local", "end_time_local", "status", "timestamp_utc", "timestamp_local"]]

    print(merged_data)
    return merged_data