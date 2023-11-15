import pandas as pd
from datetime import datetime, timedelta, timezone
from utils import data_init
# server_time = datetime(2023, 1, 25, 0, 56, 23, tzinfo=timezone.utc)
database = data_init('./status.csv', './Menu hours.csv', './timezone.csv')
df_status = database["status_data"]
business_hours_data = database["business_hours_data"]
timezone_data = database["timezone_data"]
business_hours_data['start_time_local'] = pd.to_datetime(business_hours_data['start_time_local'])
business_hours_data['end_time_local'] = pd.to_datetime(business_hours_data['end_time_local'])

def calculate_inactive_active_time_for_last_hour(server_time, store_id):
    """
    Calculate downtime and uptime for the last hour for a specific store.

    Args:
        server_time (datetime): The current server time.
        store_id (int): The ID of the store.

    Returns:
        tuple: A tuple containing downtime and uptime durations.
    """
    print(f"calculate_inactive_active_time_for_last_hour for {store_id}")
    relevant_data = df_status[df_status['store_id'] == store_id].reset_index(drop=True)
    relevant_data['timestamp_utc'] = pd.to_datetime(relevant_data['timestamp_utc'], utc=True)

    last_hour_data = relevant_data[
        (relevant_data['timestamp_utc'] >= server_time - timedelta(hours=1)) &
        (relevant_data['timestamp_utc'] <= server_time)
    ]

    inactive_mask = last_hour_data['status'].shift(-1) == 'inactive'
    uptime_mask = last_hour_data['status'].shift(-1) == 'active'

    downtime = last_hour_data.loc[inactive_mask, 'timestamp_utc'].diff().sum()
    uptime = last_hour_data.loc[uptime_mask, 'timestamp_utc'].diff().sum()

    return downtime, uptime

def calculate_inactive_active_time_for_last_day(server_time, store_id, current_day_in_server=None):
    """
    Calculate downtime and uptime for the last day for a specific store.

    Args:
        server_time (datetime): The current server time.
        store_id (int): The ID of the store.
        current_day_in_server (int, optional): The current day of the week (0 for Monday, 6 for Sunday).

    Returns:
        tuple: A tuple containing downtime and uptime durations.
    """
    print(f"calculate_inactive_active_time_for_last_day for {store_id}")

    if current_day_in_server is None:
        current_day_in_server = server_time.weekday()

    relevant_data = df_status.loc[df_status['store_id'] == store_id].reset_index(drop=True)
    relevant_data['timestamp_utc'] = pd.to_datetime(relevant_data['timestamp_utc'], utc=True)

    last_day_data = relevant_data[
        (relevant_data['timestamp_utc'] >= server_time - timedelta(days=1)) &
        (relevant_data['timestamp_utc'] <= server_time)
    ]

    downtime = last_day_data.loc[last_day_data['status'].shift(-1) == 'inactive', 'timestamp_utc'].diff().sum()
    uptime = last_day_data.loc[last_day_data['status'].shift(-1) == 'active', 'timestamp_utc'].diff().sum()

    return downtime, uptime

def calculate_inactive_active_time_for_last_week(server_time, store_id):
    """
    Calculate downtime and uptime for the last week for a specific store.

    Args:
        server_time (datetime): The current server time.
        store_id (int): The ID of the store.

    Returns:
        tuple: A tuple containing downtime and uptime durations.
    """
    downtime, uptime = 0, 0
    print(f"calculate_inactive_active_time_for_last_week for {store_id}")

    for i in range(0, 7):
        times = calculate_inactive_active_time_for_last_day(server_time, store_id, current_day_in_server=i)
        downtime += times[0].total_seconds()
        uptime += times[1].total_seconds() / 60

    return downtime, uptime

if __name__ == "__main__":
    store_id = 3483930781272060942  # Replace with the desired store_id
    res_day, res_hour, res_week = calculate_inactive_active_time_for_last_day(server_time, store_id), calculate_inactive_active_time_for_last_hour(server_time, store_id), calculate_inactive_active_time_for_last_week(server_time, store_id)

    print("Last Hour - Downtime: {} minutes, Uptime: {} minutes".format(res_hour[0].total_seconds() / 3600, res_hour[1].total_seconds() / 60))
    print("Last Day - Downtime: {} hours, Uptime: {} minutes".format(res_day[0].total_seconds() / 3600, res_day[1].total_seconds() / 60))
    print("Last Week - Downtime: {} hours, Uptime: {} minutes".format(res_week[0] / 3600, res_week[1] / 60))
