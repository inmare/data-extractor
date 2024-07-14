from . import get_excel_data, download_data, get_json_data


def generate(excel_file_name: str):
    date_sheet, recommend_sheet = get_excel_data.get_sheets(excel_file_name)
    date = get_excel_data.get_date(date_sheet)
    # 날짜가 포함된 json 파일이 있는지 체크하기
    is_json_exist = get_json_data.check_json_file_exist(date)
    if is_json_exist:
        info = get_json_data.read_json_data(date)
        music_dl_success = get_json_data.check_download_status(info, "music")
        thumbnail_dl_success = get_json_data.check_download_status(info, "thumbnail")
    else:
        info = get_excel_data.get_info(recommend_sheet)

    if not music_dl_success:
        info, music_dl_success = download_data.download_data(info, "music", True)
    if not thumbnail_dl_success:
        info, thumbnail_dl_success = download_data.download_data(
            info, "thumbnail", True
        )

    if music_dl_success and thumbnail_dl_success:
        # json 파일에 데이터 쓰고 압축하기
        pass
    else:
        # json 파일에 데이터 쓰기만 하기
        pass


if __name__ == "__main__":
    pass
