
import os
import time
import yaml
import json
from pathlib import Path
from datetime import datetime
from rad_data.utils.bunch import Bunch

os.environ['TZ'] = 'UTC'
time.tzset()


def get_config(path: str) -> Bunch:
    """
    Convert config yaml file to bunch object
    Args:
        path: File path for config file
    Returns: Bunch object

    """
    try:
        if not Path(path).exists():
            raise FileNotFoundError
        with open(path, 'r') as yaml_string:
            data = yaml.safe_load(yaml_string.read())
        return json.loads(json.dumps(data), object_hook=Bunch)
    except Exception as e:
        print(f'Error in get config from file, {e}')


def list_to_dict_by_key(list_of_dict: list, key: str) -> dict:
    """
    Convert list to dictionary by key
    Args:
        list_of_dict: List of dictionary
        key: Key name from dictionary in list
    Returns: Dictionary based on key value
    """
    docs = {}
    for item in list_of_dict:
        try:
            docs[str(item[key])] = item
        except Exception as e:
            print(f'Error in convert list to dictionary  by key, {e}')
    return docs


def datetime_to_unix(date_time: str or datetime, date_time_format: str = '%Y-%m-%dT%H:%M:%S') -> int:
    """
    Convert string to unix datetime
    Args:
        date_time: String or Date types date time
        date_time_format : format of date
    Returns: Unix date_time
    """
    date = datetime_formatter(date_time, date_time_format)
    return int(date.timestamp() * 1000)


def unix_to_datetime(unix_time: int) -> datetime:
    """
    Convert string to unix datetime
    Args:
        unix_time: String or Date types date time
    Returns: Unix date_time
    """
    if len(str(unix_time)) == 13:
        unix_time = int(unix_time / 1000)
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


def datetime_formatter(date_time: str or datetime, format: str) -> datetime:
    if type(date_time) is str:
        if '.' in date_time:
            date_time = date_time.split('.')[0]
            return datetime.strptime(date_time, format)
        else:
            return datetime.strptime(date_time, format)
    if type(date_time) is datetime:
        return date_time.replace(microsecond=0)
