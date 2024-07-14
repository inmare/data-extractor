from .log_print import log_print
from enum import Enum, auto


# youtube-dl logger용 클래스
class loggerOutputs:
    def error(msg: str):
        error_msg = msg.removeprefix("ERROR: ")
        log_print("오류", error_msg)

    def warning(msg):
        pass
        # log_print("경고", msg)

    def debug(msg):
        pass
        # log_print("작업", msg)


# 그 외 설정들
DATE_CELL = {
    "year": "I4",
    "month": "J4",
}

START_ROW = 3

EXCEL_KEY = {
    "이름": "name",
    "닉네임": "nickname",
    "원본 링크": "originalLink",
    "다운로드 가능 링크": "downloadableLink",
    "노래 제목": "songName",
    "한국어 노래 제목": "songNameKor",
    "작곡가": "composer",
    "코멘트": "comment",
    "한국어 가사 링크": "korLyricsLink",
}

# 무조건 엑셀 파일에 들어있어야 하는 값들
ESSENTIAL_KEY = [
    "원본 링크",
    "다운로드 가능 링크",
    "노래 제목",
    "한국어 노래 제목",
    "작곡가",
    "코멘트",
]

# 추가적으로 데이터에 포함될 key 값
ADDITIONAL_KEY = {
    "파일 이름": "fileName",
    "노래 다운 여부": "audioDownloaded",
    "썸네일 다운 여부": "thumbnailDownloaded",
}

# 최종적으로 데이터에 포함될 key 값
FINAL_OUTPUT_KEY = [
    "파일 이름",
    "닉네임",
    "노래 제목",
    "한국어 노래 제목",
    "작곡가",
    "코멘트",
    "한국어 가사 링크",
]

FOLDER_NAME = {
    "music": "music",
    "thumbnail": "thumbnail",
}


class DlDataType(Enum):
    MUSIC = auto()
    THUMBNAIL = auto()


MUSIC_YDL_OPTS = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "quiet": True,
    "logger": loggerOutputs,
}

THUMBNAIL_YDL_OPTS = {
    "skip_download": True,  # Skip downloading the video
    "writethumbnail": True,  # Download the thumbnail
    "quiet": True,
    "logger": loggerOutputs,
}

JSON_FILE_SUFFIX = "플레이리스트"


if __name__ == "__main__":
    pass
