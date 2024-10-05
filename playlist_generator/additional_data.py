import re


def process_file_name(song_name_kor: str) -> str:
    """
    한국어 곡 제목을 윈도우 환경에서 파일명으로 사용할 수 있도록 변환하는 함수\\
    (윈도우 환경에서 사용할 수 없는 문자를 '_'로 변환)

    Args:
        song_name_kor (str): 한국어 곡 제목

    Returns:
        str: 파일명으로 사용할 수 있는 곡 제목
    """
    replace_str = '\\/:*?"<>|'
    file_name = [char if char not in replace_str else "_" for char in song_name_kor]
    return "".join(file_name)


def is_youtube_link(downloadable_link: str) -> bool:
    """
    다운가능한 링크가 유튜브 링크인지 알려주는 함수

    Args:
        downloadable_link (str): 다운로드 가능 링크

    Returns:
        bool: 해당 링크가 유튜브 링크인지 여부
    """
    yt_link_regex = re.compile(
        r"^http?s:\/\/(www\.youtube\.com\/watch\?v=|youtu\.be\/)[A-Za-z0-9-_]{11}.*$"
    )
    is_yt_link = yt_link_regex.match(downloadable_link)
    return is_yt_link is not None


if __name__ == "__main__":
    pass
