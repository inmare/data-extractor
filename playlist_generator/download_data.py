from . import project_config as config
from .project_config import DlDataType
from .log_print import log_print, LogType
from PIL import Image
import yt_dlp
import os


def convert_thumbnail(file_name):
    log_print(LogType.PROGRESS, "썸네일을 변환 중 입니다...")
    # 웹브라우저에서 지원되는 이미지 확장자들
    supported_formats = ["jpg", "jpeg", "png", "gif", "webp"]
    thumbnail_folder = config.FOLDER_NAME["thumbnail"]
    for ext in supported_formats:
        thumbnail_path = os.path.join(thumbnail_folder, f"{file_name}.{ext}")
        if os.path.exists(thumbnail_path) and ext != "png":
            img = Image.open(thumbnail_path).convert("RGB")
            img.save(os.path.join(thumbnail_folder, f"{file_name}.png"), "PNG")
            os.remove(thumbnail_path)
            break


def download_data(
    playlist_info: list, data_type: DlDataType, retry_dl: bool = False
) -> list:
    """
    데이터를 기반으로 파일을 다운로드 하는 함수

    Args:
        playlist_info: 노래 정보가 담긴 리스트
        data_type: 다운로드할 데이터 종류
        retry_dl: 재다운로드 여부

    Returns:
        dl_status: 각 데이터의 다운로드 성공 여부를 담은 리스트
    """

    if data_type == DlDataType.MUSIC:
        folder_name = config.FOLDER_NAME["music"]
        ydl_opts = config.MUSIC_YDL_OPTS.copy()
        type_name = "노래"
        dl_status_key = config.ADDITIONAL_KEY["노래 다운 여부"]
    elif data_type == DlDataType.THUMBNAIL:
        folder_name = config.FOLDER_NAME["thumbnail"]
        ydl_opts = config.THUMBNAIL_YDL_OPTS.copy()
        type_name = "썸네일"
        dl_status_key = config.ADDITIONAL_KEY["썸네일 다운 여부"]

    log_print(LogType.PROGRESS, f"{type_name} 다운로드를 시작합니다.")

    # dict가 파이썬 최근 버전에서는 index를 기억함에 따라 아래와 같은 작업 가능
    dl_status = [True] * len(playlist_info)

    # 다운로드를 처음 하는 거면 폴더를 비워줌
    if not retry_dl:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        else:
            files = os.listdir(folder_name)
            for file in files:
                os.remove(os.path.join(folder_name, file))

    for idx, info in enumerate(playlist_info):
        song_name_kor = info[config.EXCEL_KEY["한국어 노래 제목"]]
        file_name = info[config.ADDITIONAL_KEY["파일 이름"]]
        link = info[config.EXCEL_KEY["다운로드 가능 링크"]]

        # 다시 다운로드 하는 거면 이미 다운로드 된 건 넘어감
        if retry_dl:
            if info[dl_status_key]:
                continue
            else:
                log_print(
                    LogType.PROGRESS,
                    f'{type_name} "{song_name_kor}" 다운로드를 다시 시작합니다.',
                )

        try:
            ydl_opts["outtmpl"] = os.path.join(folder_name, file_name + ".%(ext)s")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(link)
            if data_type == DlDataType.THUMBNAIL:
                convert_thumbnail(file_name)
            log_print(
                LogType.SUCCESS,
                f'{type_name} "{song_name_kor}"의 다운로드에 성공했습니다.',
            )
        except Exception as _:
            dl_status[idx] = False
            log_print(
                LogType.ERROR,
                f'{type_name} "{song_name_kor}"의 다운로드에 실패했습니다. 파일을 스킵합니다.',
            )

    return dl_status


if __name__ == "__main__":
    pass
