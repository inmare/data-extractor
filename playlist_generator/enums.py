from enum import Enum
from .error import CustomException


class DataEnum(Enum):
    """
    Playlist 데이터를 다루는 기본 enum 클래스\\
    Enum의 value로 dict를 사용하되, 무조건 json파일로 내보낼지 결정하는 "export" 키가 존재해야 한다.
    """

    def __init__(self, value: dict) -> None:
        # Enum을 정의할 때, export 키가 없으면 에러 발생
        if "export" not in value:
            raise CustomException("Data 클래스에 필요한 export 키가 없습니다.")

    def __str__(self):
        return self.name[0].lower() + self.name[1:]

    def __repr__(self):
        return self.name[0].lower() + self.name[1:]

    def should_export(self):
        """
        데이터를 json 파일로 내보낼지 결정하는 메서드
        """
        return self.value["export"]


def get_data_by_key_name(data: DataEnum, key_name: str) -> DataEnum:
    """
    DataEnum에서 key_name에 해당하는 데이터를 반환한다.

    Args:
        data: DataEnum 클래스
        key_name: 찾고자 하는 key 이름

    Returns:
        DataEnum: key_name에 해당하는 데이터가 존재하면 해당 데이터를 반환하고, 없다면 None을 반환한다.
    """
    # next는 iterator에 대해서 다음 요소를 반환하는 함수이다.
    return next((item for item in data if item == key_name), None)


class ExcelSheet(Enum):
    """
    엑셀 시트 관련 설정들이 들어있는 Enum 클래스
    """

    DateSheetIdx = 0
    """
    날짜 데이터가 있는 시트의 인덱스
    """
    YearCell = "I4"
    """
    시트에서 연도가 들어있는 셀
    """
    MonthCell = "J4"
    """
    시트에서 월이 들어있는 셀
    """
    RecommendSheetIdx = 1
    """
    곡 추천 리스트 시트의 인덱스
    """
    KeyDataRow = 2
    """
    데이터의 key 값이 들어있는 행
    """

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.value


class ExcelData(DataEnum):
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

    def is_essential(self):
        """
        해당 데이터가 필수적인 데이터인지 반환한다.
        """
        return self.value["essential"]

    def get_ui_name(self):
        """
        엑셀 시트에서 사용자에게 보여지는 해당 키의 이름을 반환한다.
        """
        return self.value["name"]


if __name__ == "__main__":
    pass
