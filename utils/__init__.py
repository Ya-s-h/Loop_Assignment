from utils.database_operations import read_csv, utc_to_local
import pandas as pd



def data_init(status_csv, business_hours_csv, timezone_csv):
    return {"status_data": read_csv(file_path=status_csv, key_column="store_id"),
            "business_hours_data": read_csv(file_path=business_hours_csv, key_column="store_id"),
            "timezone_data": read_csv(file_path=timezone_csv, key_column="store_id")
            }
