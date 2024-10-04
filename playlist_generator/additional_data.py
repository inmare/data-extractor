import re


class AdditionalData:
    def __init__(self):
        pass

    @staticmethod
    def process_file_name(song_name_kor: str) -> str:
        """
        한국어 곡 제목을 윈도우 환경에서 파일명으로 사용할 수 있도록 변환하는 함수
        """
        replace_str = '\\/:*?"<>|'
        file_name = [char if char not in replace_str else "_" for char in song_name_kor]
        return "".join(file_name)

    @staticmethod
    def is_youtube_link(downloadable_link: str) -> bool:
        """
        다운가능한 링크가 유튜브 링크인지 알려주는 함수
        """
        yt_link_regex = re.compile(
            r"^http?s:\/\/(www\.youtube\.com\/watch\?v=|youtu\.be\/)[A-Za-z0-9-_]{11}.*$"
        )
        is_yt_link = yt_link_regex.match(downloadable_link)
        return is_yt_link is not None
