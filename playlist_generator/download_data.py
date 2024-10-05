# from . import project_config as config
# from .project_config import DlDataType
# from .logger import log_print, LogType
# from PIL import Image
# import yt_dlp
# import os


import os
import yt_dlp
from PIL import Image
from .logger import Logger
from .configs import (
    PathCfg,
    ExcelDataCfg,
    AdditionalDataCfg,
    DownloadCfg,
    DownloadDataCfg,
)


def set_ffmpeg_path(program_dir: str) -> None:
    """
    yt_dlp에서 ffmpeg를 사용하기 위해 ffmpeg의 위치를 설정하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
    """
    DownloadCfg.Music.value["ffmpeg_location"] = os.path.join(
        program_dir, PathCfg.FFmpegFileDir.value
    )
    DownloadCfg.Thumbnail.value["ffmpeg_location"] = os.path.join(
        program_dir, PathCfg.FFmpegFileDir.value
    )


def set_dl_options(
    program_dir: str, file_name: str, data_type: DownloadDataCfg
) -> dict:
    """
    yt_dlp에서 다운로드할 파일의 경로를 설정하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        file_name (str): 파일 이름
        data_type (DownloadDataType): 다운로드할 데이터 종류

    Returns:
        dict: yt_dlp에서 사용할 다운로드 옵션
    """
    if data_type == DownloadDataCfg.Music:
        folder_name = PathCfg.MusicDir.value
        ydl_opts = DownloadCfg.Music.value.copy()
    elif data_type == DownloadDataCfg.Thumbnail:
        folder_name = PathCfg.ThumbnailDir.value
        ydl_opts = DownloadCfg.Thumbnail.value.copy()
    ydl_opts["outtmpl"] = os.path.join(program_dir, folder_name, file_name + ".%(ext)s")

    return ydl_opts


def download_data(
    program_dir: str,
    song_name: str,
    options: dict,
    link: str,
    data_type: DownloadDataCfg,
    file_name: str | None = None,
) -> bool:
    """
    yt_dlp를 사용하여 데이터를 다운로드하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        song_name (str): 노래 제목
        options (dict): yt_dlp에서 사용할 다운로드 옵션
        link (str): 다운로드 링크
        data_type (DownloadDataCfg): 다운로드할 데이터 종류
        file_name (str, optional): 파일 이름. 썸네일을 다운로드 할 때만 사용.

    Returns:
        bool: 다운로드 성공 여부
    """

    if data_type == DownloadDataCfg.Music:
        data_type_str = "노래"
    elif data_type == DownloadDataCfg.Thumbnail:
        data_type_str = "썸네일"

    try:
        Logger.debug(f'{data_type_str} "{song_name}" 다운로드를 시작합니다.')
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(link)
        Logger.info(f'{data_type_str} "{song_name}" 다운로드를 완료했습니다.')

        if data_type == DownloadDataCfg.Thumbnail:
            convert_thumbnail(program_dir, file_name)

        return True
    except Exception as _:
        # yt_dlp에서 발생하는 에러는 콘솔에 표시되기 때문에 따로 출력하지 않음
        Logger.error(f"{data_type_str} 다운로드 중 에러가 발생했습니다")
        return False


def convert_thumbnail(program_dir: str, file_name: str):
    """
    썸네일을 변환하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        file_name (str): 파일 이름
    """
    try:
        # 웹브라우저에서 지원되는 이미지 확장자들
        supported_formats = ["jpg", "jpeg", "png", "gif", "webp"]
        thumbnail_folder = PathCfg.ThumbnailDir.value
        for ext in supported_formats:
            thumbnail_path = os.path.join(
                program_dir, thumbnail_folder, f"{file_name}.{ext}"
            )
            if os.path.exists(thumbnail_path) and ext != "png":
                img = Image.open(thumbnail_path).convert("RGB")
                img.save(
                    os.path.join(program_dir, thumbnail_folder, f"{file_name}.png"),
                    "PNG",
                )
                os.remove(thumbnail_path)
                break
    except Exception as e:
        raise e


if __name__ == "__main__":
    pass
