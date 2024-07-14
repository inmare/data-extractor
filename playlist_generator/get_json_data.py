from . import project_config as config
import json
import os


def get_json_file_name(date):
    return f"{date.year}-{date.month}-{config.JSON_FILE_SUFFIX}.json"


def write_json_data(date, info, file_name):
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


def check_download_status(info, data_type):
    for song_info in info:
        if (
            data_type == "music"
            and not song_info[config.ADDITIONAL_KEY["노래 다운 여부"]]
        ):
            return False
        if (
            data_type == "thumbnail"
            and not song_info[config.ADDITIONAL_KEY["썸네일 다운 여부"]]
        ):
            return False
    return True


if __name__ == "__main__":
    pass
