from . import excel_data, json_data
from .download_data import download_data
from .project_config import DlDataType
from . import project_config as config
from .log_print import log_print, LogType
from .error import UserInvokedError
import zipfile
import shutil
import os


def delete_original_path(date):
    music_folder = config.FOLDER_NAME["music"]
    thumbnail_folder = config.FOLDER_NAME["thumbnail"]
    json_file = json_data.get_json_file_name(date)
    if os.path.exists(music_folder):
        shutil.rmtree(music_folder)
    if os.path.exists(thumbnail_folder):
        shutil.rmtree(thumbnail_folder)
    if os.path.exists(json_file):
        os.remove(json_file)


def zip_files(info_list, data_type, dl_status, zipf):
    if data_type == DlDataType.MUSIC:
        folder_name = config.FOLDER_NAME["music"]
        ext = "mp3"
    elif data_type == DlDataType.THUMBNAIL:
        folder_name = config.FOLDER_NAME["thumbnail"]
        ext = "png"

    for info, status in zip(info_list, dl_status):
        if not status:
            continue
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

            # if key_name == config.EXCEL_KEY["원본 링크"]:
            #     # 원본 링크가 비어있는 경우면 그냥 None으로 처리
            #     is_valid_link = info[key_name].startswith("http")
            #     final_info[key_name] = info[key_name] if is_valid_link else None
            # else:
            #     final_info[key_name] = info[key_name]
            final_info[key_name] = info[key_name]

        final_info_list.append(final_info)

    return final_info_list


def generate(excel_file_name: str):
    try:
        date_sheet, recommend_sheet = excel_data.get_sheets(excel_file_name)
        log_print(LogType.PROGRESS, f"파일 {excel_file_name}에서 데이터를 추출합니다.")

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

        while not dl_success:
            # json 파일에 데이터 쓰기만 하기
            if False in music_dl_status:
                add_dl_status(info, DlDataType.MUSIC, music_dl_status)
            if False in thumbnail_dl_status:
                add_dl_status(info, DlDataType.THUMBNAIL, thumbnail_dl_status)
            json_data.write_json_data(date, info)
            log_print(
                LogType.WARNING,
                "일부 데이터를 다운로드 받지 못했습니다.",
            )

            user_answer = None
            while user_answer not in ["yes", "no"]:
                user_answer = input(
                    "다시 한 번 다운로드를 시도하려면 yes를, 현재 파일들만으로 압축파일을 만들려면 no을 입력하고 Enter를 눌러주세요: "
                )

            if user_answer == "yes":
                # 다운로드가 안된 노래와 썸네일만 다시 다운로드 하기
                for idx, status in enumerate(music_dl_status):
                    if not status:
                        music_retry_status = download_data(
                            [info[idx]], DlDataType.MUSIC, retry_dl=True
                        )
                        if music_retry_status[0]:
                            music_dl_status[idx] = True

                for idx, status in enumerate(thumbnail_dl_status):
                    if not status:
                        thumbnail_retry_status = download_data(
                            [info[idx]], DlDataType.THUMBNAIL, retry_dl=True
                        )
                        if thumbnail_retry_status[0]:
                            thumbnail_dl_status[idx] = True

                dl_success = (
                    not False in music_dl_status and not False in thumbnail_dl_status
                )
            if user_answer == "no":
                break

        dl_success = not False in music_dl_status and not False in thumbnail_dl_status

        # json 파일에 데이터 쓰고 압축하기
        if dl_success:
            log_print(LogType.SUCCESS, "모든 데이터를 다운로드 받았습니다.")

        log_print(LogType.PROGRESS, "다운로드한 데이터로 압축파일을 생성합니다.")
        final_info_list = extract_final_info(info)
        json_data.write_json_data(date, final_info_list)

        zipf = zipfile.ZipFile(
            f"{date.year}-{str(date.month).zfill(2)}-{config.ZIP_FILE_SUFFIX}.zip",
            "w",
            zipfile.ZIP_DEFLATED,
        )
        zip_files(info, DlDataType.MUSIC, music_dl_status, zipf)
        zip_files(info, DlDataType.THUMBNAIL, thumbnail_dl_status, zipf)
        zipf.write(json_data.get_json_file_name(date))
        zipf.close()
        log_print(
            LogType.SUCCESS,
            f"{date.year}년 {date.month}월 플레이리스트 압축파일을 생성했습니다.",
        )
        delete_original_path(date)
        log_print(
            LogType.SUCCESS,
            f"생성된 압축파일 이름은 {date.year}-{str(date.month).zfill(2)}-{config.ZIP_FILE_SUFFIX}.zip 입니다.",
        )
        input("Enter키를 누르면 프로그램이 종료 됩니다...")

    except Exception as e:
        if isinstance(e, UserInvokedError):
            log_print(LogType.PROGRESS, e)
        else:
            log_print(LogType.ERROR, e)
            log_print(LogType.ERROR, "에러가 발생하였습니다. 프로그램이 종료됩니다.")
        if date:
            # 다운로드, 생성된 파일들이 있으면 삭제
            delete_original_path(date)
            # 압축파일이 생성되었으면 삭제
            zip_file_path = (
                f"{date.year}-{str(date.month).zfill(2)}-{config.ZIP_FILE_SUFFIX}.zip"
            )
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)
        input("Enter키를 누르면 프로그램이 종료 됩니다...")


if __name__ == "__main__":
    pass
