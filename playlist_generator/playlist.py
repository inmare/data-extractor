from . import excel_data, json_data
from .download_data import download_data
from .project_config import DlDataType
from . import project_config as config
from .log_print import log_print, LogType
import zipfile


def zip_files(info_list, data_type, zipf):
    if data_type == DlDataType.MUSIC:
        folder_name = config.FOLDER_NAME["music"]
    elif data_type == DlDataType.THUMBNAIL:
        folder_name = config.FOLDER_NAME["thumbnail"]

    for info in info_list:
        file_name = info[config.ADDITIONAL_KEY["파일 이름"]]
        zipf.write(f"{folder_name}/{file_name}")


def add_dl_status(info, data_type, dl_status):
    if data_type == DlDataType.MUSIC:
        key_name = config.ADDITIONAL_KEY["노래 다운 여부"]
    elif data_type == DlDataType.THUMBNAIL:
        key_name = config.ADDITIONAL_KEY["썸네일 다운 여부"]

    for idx, info_dict in enumerate(info):
        info_dict[key_name] = dl_status[idx]


def get_dl_status(info, data_type, is_json_exist):
    if is_json_exist:
        # 노래나 썸네일을 다운로드 받지 못한 경우 다시 다운로드 받기
        is_dl_success = json_data.check_dl_status(info, data_type)
        if not is_dl_success:
            dl_status = download_data(info, data_type, retry_dl=True)
    else:
        dl_status = download_data(info, data_type)

    return dl_status


def generate(excel_file_name: str):
    date_sheet, recommend_sheet = excel_data.get_sheets(excel_file_name)
    date = excel_data.get_date(date_sheet)
    # 날짜가 포함된 json 파일이 있는지 체크하기
    is_json_exist = json_data.check_json_file_exist(date)
    if is_json_exist:
        info = json_data.read_json_data(date, is_json_exist)
    else:
        info = excel_data.get_info(recommend_sheet)
    music_dl_status = get_dl_status(info, DlDataType.MUSIC, is_json_exist)
    thumbnail_dl_status = get_dl_status(info, DlDataType.THUMBNAIL, is_json_exist)

    dl_success = not False in [music_dl_status, thumbnail_dl_status]

    if dl_success:
        # json 파일에 데이터 쓰고 압축하기
        json_data.write_json_data(date, info)
        log_print(LogType.SUCCESS, "모든 데이터를 다운로드 받았습니다.")
        zipf = zipfile.Zipfile(
            f"{date.year}-{date.month}-{config.ZIP_FILE_SUFFIX}.zip",
            "w",
            zipfile.ZIP_DEFLATED,
        )
        zip_files(info, DlDataType.MUSIC, zipf)
        zip_files(info, DlDataType.THUMBNAIL, zipf)
        zipf.write(json_data.get_json_file_name(date))
        zipf.close()
    else:
        # json 파일에 데이터 쓰기만 하기
        if False in music_dl_status:
            add_dl_status(info, DlDataType.MUSIC, music_dl_status)
        if False in thumbnail_dl_status:
            add_dl_status(info, DlDataType.THUMBNAIL, thumbnail_dl_status)
        json_data.write_json_data(date, info)
        log_print(
            LogType.WARNING,
            "모든 데이터를 다운로드 받지 못했습니다. 다시 프로그램을 시도해서 누락된 파일을 다운로드 하세요.",
        )


if __name__ == "__main__":
    pass
