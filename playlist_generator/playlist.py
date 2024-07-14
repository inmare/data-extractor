from . import excel_data, json_data
from .download_data import download_data
from .project_config import DlDataType


def generate(excel_file_name: str):
    date_sheet, recommend_sheet = excel_data.get_sheets(excel_file_name)
    date = excel_data.get_date(date_sheet)
    # 날짜가 포함된 json 파일이 있는지 체크하기
    is_json_exist = json_data.check_json_file_exist(date)
    if is_json_exist:
        info = json_data.read_json_data(date)
        is_music_dl_success = json_data.check_dl_status(info, DlDataType.MUSIC)
        is_thumbnail_dl_success = json_data.check_dl_status(info, DlDataType.THUMBNAIL)
        if not is_music_dl_success:
            music_dl_status = download_data(info, DlDataType.MUSIC, retry_dl=True)
        if not is_thumbnail_dl_success:
            thumbnail_dl_staus = download_data(
                info, DlDataType.THUMBNAIL, retry_dl=True
            )
    else:
        info = excel_data.get_info(recommend_sheet)
        info, is_music_dl_success = download_data(info, DlDataType.MUSIC)
        info, is_thumbnail_dl_success = download_data(info, DlDataType.THUMBNAIL)

    if is_music_dl_success and is_thumbnail_dl_success:
        # json 파일에 데이터 쓰고 압축하기
        pass
    else:
        # json 파일에 데이터 쓰기만 하기
        pass


if __name__ == "__main__":
    pass
