from enum import Enum
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
    Enum의 value로 dict를 사용하되, 무조건 json파일로 내보낼지 결정하는 "export" 키가 존재해야 한다.
    """

    def __init__(self, value: dict) -> None:
        # Enum을 정의할 때, export 키가 없으면 에러 발생
        if "export" not in value:
            raise CustomException("Data 클래스에 필요한 export 키가 없습니다.")

    @property
    def keyname(self) -> str:
        return self.name[0].lower() + self.name[1:]

    @property
    def export(self) -> bool:
        """
        데이터를 json 파일로 내보낼지 결정하는 메서드
        """
        return self.value["export"]


def get_data_by_key_name(data: DataEnum, key_name: str) -> DataEnum | None:
    """
    DataEnum에서 key_name에 해당하는 데이터를 반환한다.

    Args:
        data: DataEnum 클래스
        key_name: 찾고자 하는 key 이름

    Returns:
        DataEnum: key_name에 해당하는 데이터가 존재하면 해당 데이터를 반환하고, 없다면 None을 반환한다.
    """

    for item in data:
        if item.keyname == key_name:
            return item
    return None


class ExcelDataCfg(DataEnum):
    """
    엑셀에 들어있는 데이터와 관련한 Enum 클래스\\
    "export", "essential", "name" 키가 반드시 존재해야 한다.
    """

    Name = {
        "export": False,
        "essential": True,
        "name": "이름",
    }
    """
    실제 이름
    """
    Nickname = {
        "export": True,
        "essential": False,
        "name": "닉네임",
    }
    """
    닉네임\\
    없는 경우엔 익명A, 익명B와 같은 형식으로 대체
    """
    OriginalLink = {
        "export": True,
        "essential": False,
        "name": "원본 링크",
    }
    """
    원본 링크\\
    없는 경우에는 None으로 대체
    """
    DownloadableLink = {
        "export": True,
        "essential": True,
        "name": "다운로드 가능 링크",
    }
    """
    다운로드가 가능한 유튜브 링크\\
    링크의 형식이 유튜브가 아닌 경우에는 경고 발생
    """
    SongName = {
        "export": True,
        "essential": True,
        "name": "노래 제목",
    }
    """
    노래의 원 제목
    """
    SongNameKor = {
        "export": True,
        "essential": True,
        "name": "한국어 노래 제목",
    }
    """
    노래의 한국어 제목\\
    원 제목이 일본어가 아닌 경우에는 원 제목과 동일해야 함
    """
    Composer = {
        "export": True,
        "essential": True,
        "name": "작곡가",
    }
    """
    작곡가
    """
    Comment = {
        "export": True,
        "essential": True,
        "name": "코멘트",
    }
    """
    코멘트
    """
    KorLyricsLink = {
        "export": True,
        "essential": False,
        "name": "한국어 가사 링크",
    }
    """
    노래가 번역된 한국어 가사 링크\\
    없는 경우에는 None으로 대체
    """

    def __init__(self, value: dict) -> None:
        super().__init__(value)
        if "essential" not in value or "name" not in value:
            raise CustomException(
                "ExcelData 클래스에 필요한 essential 혹은 name 키가 없습니다."
            )

    @property
    def essential(self):
        """
        해당 데이터가 필수적인 데이터인지 반환한다.
        """
        return self.value["essential"]

    @property
    def ui_name(self):
        """
        엑셀 시트에서 사용자에게 보여지는 해당 키의 이름을 반환한다.
        """
        return self.value["name"]


class AdditionalDataCfg(DataEnum):
    # 노래의 다운로드 여부
    MusicDownloaded = {
        "export": False,
    }
    # 썸네일의 다운로드 여부
    ThumbnailDownloaded = {
        "export": False,
    }
    # 다운로드 할 때의 파일 이름
    FileName = {
        "export": True,
    }
    # 다운로드 가능 링크가 유튜브 링크인지 확인
    IsYoutubeLink = {
        "export": False,
    }

    def __init__(self, value: dict) -> None:
        super().__init__(value)


class Paths(Enum):
    """
    유튜브 다운로드 시 사용되는 파일 경로를 관리하는 Enum 클래스
    """

    MusicDir = "music"
    """
    노래 파일이 저장되는 폴더
    """
    ThumbnailDir = "thumbnail"
    """
    썸네일 파일이 저장되는 폴더
    """
    FFmpegFileDir = "assets/ffmpeg.exe"
    """
    ffmpeg.exe 파일의 경로
    """


class DownloadOption(Enum):
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


if __name__ == "__main__":
    pass
