import os
from enum import Enum, auto
from .error import CustomException


class ExcelSheetCfg(Enum):
    DateSheetIdx = 0
    YearCell = "I4"
    MonthCell = "J4"
    RecommendSheetIdx = 1
    KeyDataRow = 1
    StartDataRow = 3


class DataEnum(Enum):
    """
    Playlist 데이터를 다루는 기본 enum 클래스\\
    Enum의 value로 dict를 사용하되, json의 key에 대항하는 "keyname"과 json파일로 내보낼지 결정하는 "export"가 존재해야 한다.
    """

    def __init__(self, value: dict) -> None:
        # Enum을 정의할 때, export 키가 없으면 에러 발생
        if "keyname" not in value or "export" not in value:
            raise CustomException(
                "Data 클래스에 필요한 keyname과 export 키가 없습니다."
            )

    @property
    def keyname(self) -> str:
        return self.value["keyname"]

    @property
    def export(self) -> bool:
        """
        데이터를 json 파일로 내보낼지 결정하는 메서드
        """
        return self.value["export"]


def get_data_by_keyname(data: DataEnum, keyname: str) -> DataEnum | None:
    """
    DataEnum에서 keyname에 해당하는 데이터를 반환한다.

    Args:
        data: DataEnum 클래스
        keyname: 찾고자 하는 key 이름

    Returns:
        DataEnum: keyname에 해당하는 데이터가 존재하면 해당 데이터를 반환하고, 없다면 None을 반환한다.
    """

    for item in data:
        if item.keyname == keyname:
            return item
    return None


class ExcelDataCfg(DataEnum):
    """
    엑셀에 들어있는 데이터와 관련한 Enum 클래스\\
    "export", "essential", "ui_name" 키가 반드시 존재해야 한다.
    """

    Name = {
        "keyname": "name",
        "export": False,
        "essential": True,
        "ui_name": "이름",
    }
    """
    실제 이름
    """
    Nickname = {
        "keyname": "nickname",
        "export": True,
        "essential": False,
        "ui_name": "닉네임",
    }
    """
    닉네임\\
    없는 경우엔 익명A, 익명B와 같은 형식으로 대체
    """
    OriginalLink = {
        "keyname": "originalLink",
        "export": True,
        "essential": False,
        "ui_name": "원본 링크",
    }
    """
    원본 링크\\
    없는 경우에는 None으로 대체
    """
    DownloadableLink = {
        "keyname": "downloadableLink",
        "export": True,
        "essential": True,
        "ui_name": "다운로드 가능 링크",
    }
    """
    다운로드가 가능한 유튜브 링크\\
    링크의 형식이 유튜브가 아닌 경우에는 경고 발생
    """
    SongName = {
        "keyname": "songName",
        "export": False,
        "essential": True,
        "ui_name": "노래 제목",
    }
    """
    노래의 원 제목
    """
    SongNameKor = {
        "keyname": "songNameKor",
        "export": True,
        "essential": True,
        "ui_name": "한국어 노래 제목",
    }
    """
    노래의 한국어 제목\\
    원 제목이 일본어가 아닌 경우에는 원 제목과 동일해야 함
    """
    Composer = {
        "keyname": "composer",
        "export": True,
        "essential": True,
        "ui_name": "작곡가",
    }
    """
    작곡가
    """
    Comment = {
        "keyname": "comment",
        "export": True,
        "essential": True,
        "ui_name": "코멘트",
    }
    """
    코멘트
    """
    KorLyricsLink = {
        "keyname": "korLyricsLink",
        "export": True,
        "essential": False,
        "ui_name": "한국어 가사 링크",
    }
    """
    노래가 번역된 한국어 가사 링크\\
    없는 경우에는 None으로 대체
    """

    def __init__(self, value: dict) -> None:
        super().__init__(value)
        if "essential" not in value or "ui_name" not in value:
            raise CustomException(
                "ExcelData 클래스에 필요한 essential 혹은 ui_name 키가 없습니다."
            )

    @property
    def essential(self):
        """
        해당 데이터가 필수적인 데이터인지 반환
        """
        return self.value["essential"]

    @property
    def ui_name(self):
        """
        엑셀 시트에서 사용자에게 보여지는 해당 키의 이름을 반환
        """
        return self.value["ui_name"]


class AdditionalDataCfg(DataEnum):
    MusicDownloaded = {
        "keyname": "musicDownloaded",
        "export": False,
    }
    """
    노래의 다운로드 여부
    """
    ThumbnailDownloaded = {
        "keyname": "thumbnailDownloaded",
        "export": False,
    }
    """
    썸네일의 다운로드 여부
    """
    FileName = {
        "keyname": "fileName",
        "export": True,
    }
    """
    다운로드 할 때 설정될 파일 이름
    """
    IsYoutubeLink = {
        "keyname": "isYoutubeLink",
        "export": False,
    }
    """
    다운로드 가능한 링크가 유튜브 링크인지 여부
    """

    def __init__(self, value: dict) -> None:
        super().__init__(value)


class PathCfg(Enum):
    """
    유튜브 다운로드 시 사용되는 파일 경로를 관리하는 Enum 클래스
    """

    MusicDir = os.path.join("music")
    """
    노래 파일이 저장되는 폴더
    """
    ThumbnailDir = os.path.join("thumbnail")
    """
    썸네일 파일이 저장되는 폴더
    """
    FFmpegFileDir = os.path.join("assets", "ffmpeg.exe")
    """
    ffmpeg.exe 파일의 경로
    """


class DownloadCfg(Enum):
    Music = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    Thumbnail = {
        "skip_download": True,  # 비디오 다운로드 스킵
        "writethumbnail": True,  # 썸네일 다운로드
        "quiet": True,
    }


class DownloadDataCfg(Enum):
    Music = auto()
    Thumbnail = auto()


if __name__ == "__main__":
    pass
