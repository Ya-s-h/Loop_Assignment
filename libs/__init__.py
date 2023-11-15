# from logic import *
from libs.logic import *
from concurrent.futures import ProcessPoolExecutor, wait
from datetime import datetime, timezone

# server_time = datetime(2023, 1, 25, 0, 56, 23, tzinfo=timezone.utc)

# Move calculate_store_time to a module-level function
def calculate_store_time(server_time, store_id):
    """
    Calculate downtime and uptime for different time intervals for a specific store.

    Args:
        server_time (datetime): The current server time.
        store_id (int): The ID of the store.

    Returns:
        tuple: A tuple containing downtime and uptime durations for the last hour, last day, and last week.
    """
    # print(store_id, server_time, "in lib __init__")
    res_hour = calculate_inactive_active_time_for_last_hour(server_time, store_id)
    res_day = calculate_inactive_active_time_for_last_day(server_time, store_id, current_day_in_server=server_time.weekday())
    res_week = calculate_inactive_active_time_for_last_week(server_time, store_id)
    # print((res_hour, res_day, res_week))
    return (res_hour, res_day, res_week)

# This function was intended for parallel execution but was taking too much time
# Keeping it as a reference and indicating its purpose
# def calculating_time_for_each_store(executor, batch_size=10000):
#     server_time = datetime(2023, 1, 25, 0, 56, 23, tzinfo=timezone.utc)
#
#     store_ids_list = df_status['store_id'].unique()
#
#     with executor as pool:
#         batches = [store_ids_list[i:i + batch_size] for i in range(0, len(store_ids_list), batch_size)]
#         futures = {pool.submit(calculate_store_time, store_id): store_id for store_id in store_ids_list}
#
#     # Wait for all tasks to complete
#     done, not_done = wait(futures)
#
#     # Retrieve results from completed tasks
#     results = {store_id: result for store_id, result in [future.result() for future in done]}
#     return results

if __name__ == '__main__':
    calculate_store_time(3483930781272060942, server_time)
