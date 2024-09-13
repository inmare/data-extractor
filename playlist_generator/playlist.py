from . import excel_data, json_data
from .download_data import download_data
from .project_config import DlDataType
from . import project_config as config
from .log_print import log_print, LogType
import zipfile


def zip_files(info_list, data_type, zipf):
    if data_type == DlDataType.MUSIC:
        folder_name = config.FOLDER_NAME["music"]
        ext = "mp3"
    elif data_type == DlDataType.THUMBNAIL:
        folder_name = config.FOLDER_NAME["thumbnail"]
        ext = "png"

    for info in info_list:
        file_name = info[config.ADDITIONAL_KEY["파일 이름"]]
        zipf.write(f"{folder_name}/{file_name}.{ext}")


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
            return dl_status
        else:
            return [True] * len(info)
    else:
        dl_status = download_data(info, data_type)
        return dl_status


def extract_final_info(info_list):
    final_info_names = config.FINAL_OUTPUT_KEY

    final_info_list = []
    for info in info_list:
        final_info = {}
        for name in final_info_names:
            if name not in config.EXCEL_KEY.keys():
                key_name = config.ADDITIONAL_KEY[name]
            else:
                key_name = config.EXCEL_KEY[name]

            if key_name == config.EXCEL_KEY["원본 링크"]:
                # 원본 링크가 비어있는 경우면 그냥 None으로 처리
                is_valid_link = info[key_name].startswith("http")
                final_info[key_name] = info[key_name] if is_valid_link else None
            else:
                final_info[key_name] = info[key_name]

        final_info_list.append(final_info)

    return final_info_list


def generate(excel_file_name: str):
    date_sheet, recommend_sheet = excel_data.get_sheets(excel_file_name)
    date = excel_data.get_date(date_sheet)
    # 날짜가 포함된 json 파일이 있는지 체크하기
    is_json_exist = json_data.check_json_file_exist(date)
    if is_json_exist:
        info = json_data.read_json_data(date)
    else:
        info = excel_data.get_info(recommend_sheet)
    music_dl_status = get_dl_status(info, DlDataType.MUSIC, is_json_exist)
    thumbnail_dl_status = get_dl_status(info, DlDataType.THUMBNAIL, is_json_exist)

    dl_success = not False in music_dl_status and not False in thumbnail_dl_status

    if dl_success:
        # json 파일에 데이터 쓰고 압축하기
        final_info_list = extract_final_info(info)
        json_data.write_json_data(date, final_info_list)
        log_print(LogType.SUCCESS, "모든 데이터를 다운로드 받았습니다.")
        zipf = zipfile.ZipFile(
            f"{date.year}-{str(date.month).zfill(2)}-{config.ZIP_FILE_SUFFIX}.zip",
            "w",
            zipfile.ZIP_DEFLATED,
        )
        zip_files(info, DlDataType.MUSIC, zipf)
        zip_files(info, DlDataType.THUMBNAIL, zipf)
        zipf.write(json_data.get_json_file_name(date))
        zipf.close()
        log_print(
            LogType.SUCCESS,
            f"{date.year}년 {date.month}월 플레이리스트 압축파일을 생성했습니다.",
        )
        log_print(
            LogType.SUCCESS,
            f"생성된 압축파일 이름은 {date.year}-{str(date.month).zfill(2)}-{config.ZIP_FILE_SUFFIX}.zip 입니다.",
        )
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
        log_print(
            LogType.WARNING,
            "혹은 생성된 모든 폴더와 파일을 삭제하고 엑셀 파일의 링크 정보를 수정한 후 다시 시도하세요.",
        )


if __name__ == "__main__":
    pass
