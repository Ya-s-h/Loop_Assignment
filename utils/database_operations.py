import pandas as pd


def read_csv(file_path, key_column=None, record_value=None):
    """
    Read CSV data from the specified file.

    Args:
        file_path (str): The path to the CSV file.
        key_column (str, optional): The column to use as keys in the dictionary.
        record_value (str, optional): The value to use for retrieving a specific record.

    Returns:
        dict, list of dict, or None: If key_column is provided, a dictionary with keys as unique values in key_column
                                      and values as lists of dictionaries. If record_value is provided, a single dictionary.
                                      Otherwise, a list of dictionaries.
    """
    try:
        data = pd.read_csv(file_path)

        if key_column:
            if record_value:
                # Returning all occurences of record_value in key_column
                return data[data[key_column] == record_value].to_dict('records')
            else:
                # Grouping all the data by specific key_column
                return data.groupby(key_column).apply(lambda x: x.to_dict('records')).to_dict()
        else:
            # Returning all the data in dictionary format
            return data.to_dict('records')
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading CSV: {e}")

    return {} if key_column else []


# Example usage:
store_id_to_check = 1371971221718848145
status_csv = 'status.csv'
business_hours_csv = 'Menu hours.csv'
timezone_csv = 'timezone.csv'
