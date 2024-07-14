from . import excel_data, json_data
from .download_data import download_data
from .project_config import DlDataType


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
        pass
    else:
        # json 파일에 데이터 쓰기만 하기
        pass


if __name__ == "__main__":
    pass
