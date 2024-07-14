from . import project_config as config
from .project_config import DlDataType
import json
import os


def get_json_file_name(date):
    return f"{date.year}-{str(date.month).zfill(2)}-{config.JSON_FILE_SUFFIX}.json"


def write_json_data(date, info):
    json_file_name = get_json_file_name(date)
    with open(json_file_name, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)


def read_json_data(date):
    json_file_name = get_json_file_name(date)
    with open(json_file_name, "r", encoding="utf-8") as f:
        info = json.load(f)
    return info


def check_json_file_exist(date):
    json_file_name = get_json_file_name(date)
    file_exists = os.path.exists(json_file_name)
    return file_exists


def check_dl_status(info, data_type):
    if data_type == DlDataType.MUSIC:
        key_name = config.ADDITIONAL_KEY["노래 다운 여부"]
    elif data_type == DlDataType.THUMBNAIL:
        key_name = config.ADDITIONAL_KEY["썸네일 다운 여부"]

    # 모든 dict의 key를 모아서 set으로 만들기
    all_keys = set().union(*(d.keys() for d in info))

    if key_name not in all_keys:
        return True

    return False


if __name__ == "__main__":
    pass
