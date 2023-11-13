import pandas as pd
from datetime import datetime, timedelta, timezone
from utils import data_init

database = data_init('../status.csv', '../Menu hours.csv', '../timezone.csv')
df_status = database["status_data"]
business_hours_data = database["business_hours_data"]
timezone_data = database["timezone_data"]
business_hours_data['start_time_local'] = pd.to_datetime(business_hours_data['start_time_local'])
business_hours_data['end_time_local'] = pd.to_datetime(business_hours_data['end_time_local'])

def filter_data_within_business_hours(store_id, data, business_hours):
    relevant_data = business_hours_data[business_hours_data['store_id'] == store_id].copy()

    # Sort the business_hours DataFrame based on the key for merging
    relevant_data = relevant_data.sort_values(by='store_id')

    # Sort the data DataFrame based on the key for merging
    data = data.sort_values(by='store_id')

    # Merge data with business_hours
    merged_data = pd.merge_asof(data, relevant_data, on='store_id')
    merged_data['timestamp_day_of_week'] = merged_data['timestamp_utc'].dt.dayofweek

    # Filter data within business hours for the corresponding day
    filtered_data = merged_data[
        (merged_data['timestamp_utc'].dt.time >= merged_data['start_time_local'].dt.time) &
        (merged_data['timestamp_utc'].dt.time <= merged_data['end_time_local'].dt.time) &
        (merged_data['timestamp_day_of_week'] == merged_data['day'])
        ]

    return merged_data

def calculate_inactive_active_time_for_last_hour(server_time, store_id):
    relevant_data = df_status[df_status['store_id'] == store_id].copy()
    relevant_data['timestamp_utc'] = pd.to_datetime(relevant_data['timestamp_utc'])

    # Filter status data for the last day within business hours for a specific store
    last_day_data = relevant_data[
        (relevant_data['timestamp_utc'] >= server_time - timedelta(hours=1)) &
        (relevant_data['timestamp_utc'] <= server_time)
        ]
    # last_day_data = filter_data_within_business_hours(store_id, last_day_data, business_hours_data)

    # Calculate downtime as the sum of time differences where the status is inactive
    downtime = last_day_data['timestamp_utc'].diff().where(last_day_data['status'].shift(-1) == 'inactive').sum()
    uptime = last_day_data['timestamp_utc'].diff().where(last_day_data['status'].shift(-1) == 'active').sum()

    return downtime, uptime


def calculate_inactive_active_time_for_last_day(server_time, store_id, current_day_in_server = None):
    if current_day_in_server is None:
        current_day_in_server = server_time.weekday()
    relevant_data = df_status[df_status['store_id'] == store_id].copy()
    relevant_data['timestamp_utc'] = pd.to_datetime(relevant_data['timestamp_utc'])

    # Filter status data for the last day within business hours for a specific store
    last_day_data = relevant_data[
        (relevant_data['timestamp_utc'] >= server_time - timedelta(days=1)) &
        (relevant_data['timestamp_utc'] <= server_time)
        ]
    # last_day_data = filter_data_within_business_hours(store_id, last_day_data, business_hours_data)
    last_day_data.sort_values(by="timestamp_utc")
    # print(current_day_in_server , "\n", last_day_data['status'])
    # Calculate downtime as the sum of time differences where the status is inactive
    downtime = last_day_data['timestamp_utc'].diff().where(last_day_data['status'].shift(-1) == 'inactive').sum()
    uptime = last_day_data['timestamp_utc'].diff().where(last_day_data['status'].shift(-1) == 'active').sum()

    return downtime, uptime


def calculate_inactive_active_time_for_last_week(server_time, store_id):
    downtime, uptime = 0, 0
    for i in range(0, 7):
        times = calculate_inactive_active_time_for_last_day(server_time, store_id, current_day_in_server=i)
        downtime += times[0].total_seconds()
        uptime += times[1].total_seconds()/60
    return downtime, uptime

if __name__ == "__main__":
    server_time = datetime(2023, 1, 25, 0, 56, 23, tzinfo=timezone.utc)
    store_id = 3483930781272060942  # Replace with the desired store_id
    res_day = calculate_inactive_active_time_for_last_day(server_time, store_id)
    res_hour = calculate_inactive_active_time_for_last_hour(server_time, store_id)
    res_week = calculate_inactive_active_time_for_last_week(server_time, store_id)
    #
    print("Last Hour - Downtime: {} minutes, Uptime: {} minutes".format(res_hour[0].total_seconds() / 3600, res_hour[1].total_seconds() / 60))
    print("Last Day - Downtime: {} hours, Uptime: {} minutes".format(res_day[0].total_seconds() / 3600, res_day[1].total_seconds() / 60))
    print("Last Week - Downtime: {} hours, Uptime: {} minutes".format(res_week[0] / 3600, res_week[1] / 60))