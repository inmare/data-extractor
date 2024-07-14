from . import project_config as config
from .project_config import DlDataType
from .log_print import log_print
from enum import Enum, auto
import yt_dlp
import os


def download_again(info, data_type):
    pass


def download_inital(info, data_type):
    pass


"""
데이터를 기반으로 파일을 다운로드 하는 함수
:param playlist_info: 노래 정보가 담긴 리스트
:param data_type: 다운로드할 데이터 종류
:param download_again: 재다운로드 여부
:return: [info_list, download_success] info_list: 다운로드 정보가 담긴 리스트, download_success: 다운로드 성공 여부
"""


def download_data(
    playlist_info: list, data_type: DlDataType, download_again: bool = False
) -> list:
    info_list = playlist_info.copy()
    if data_type == DlDataType.MUSIC:
        folder_name = config.FOLDER_NAME["music"]
        ydl_opts = config.MUSIC_YDL_OPTS.copy()
        type_name = "노래"
        dl_again_key_name = config.ADDITIONAL_KEY["노래 다운 여부"]
    elif data_type == DlDataType.THUMBNAIL:
        folder_name = config.FOLDER_NAME["thumbnail"]
        ydl_opts = config.THUMBNAIL_YDL_OPTS.copy()
        type_name = "썸네일"
        dl_again_key_name = config.ADDITIONAL_KEY["썸네일 다운 여부"]

    for info in info_list:
        if info[dl_again_key_name]:
            download_again(info, data_type)
            break

    log_print("작업", f"{type_name} 다운로드를 시작합니다.")

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    else:
        files = os.listdir(folder_name)
        for file in files:
            os.remove(os.path.join(folder_name, file))

    download_success = True

    for info in info_list:
        song_name_kor = info[config.EXCEL_KEY["한국어 노래 제목"]]
        file_name = info[config.ADDITIONAL_KEY["파일 이름"]]
        link = info[config.EXCEL_KEY["다운로드 가능 링크"]]
        try:
            ydl_opts["outtmpl"] = os.path.join(folder_name, file_name + ".%(ext)s")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(link)

            log_print(
                "성공", f'{type_name} "{song_name_kor}"의 다운로드에 성공했습니다.'
            )
            if data_type == "music":
                info[config.ADDITIONAL_KEY["노래 다운 여부"]] = True
            elif data_type == "thumbnail":
                info[config.ADDITIONAL_KEY["썸네일 다운 여부"]] = True
        # except yt_dlp.utils.DownloadError as e:
        except Exception as e:
            if data_type == "music":
                info[config.ADDITIONAL_KEY["노래 다운 여부"]] = False
            elif data_type == "thumbnail":
                info[config.ADDITIONAL_KEY["썸네일 다운 여부"]] = False
            download_success = False
            log_print(
                "오류",
                f'{type_name} "{song_name_kor}"의 다운로드에 실패했습니다. 노래를 스킵합니다.',
            )

    return [info_list, download_success]


if __name__ == "__main__":
    pass
