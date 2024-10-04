# from playlist_generator import playlist
# from playlist_generator.project_config import (
#     FFMPEG_PATH,
#     MUSIC_YDL_OPTS,
#     THUMBNAIL_YDL_OPTS,
# )
# import sys
# import os

# program_dir = os.path.dirname(sys.argv[0])
# file_name = sys.argv[1]
# MUSIC_YDL_OPTS["ffmpeg_location"] = program_dir + FFMPEG_PATH
# THUMBNAIL_YDL_OPTS["ffmpeg_location"] = program_dir + FFMPEG_PATH

# playlist.generate(str(program_dir), file_name)

from playlist_generator import Playlist
from playlist_generator.error import CustomException, UserInvokedException
from playlist_generator.logger import Logger
import os
import sys

program_dir = sys.argv[0]
file_name = "2024년 8월 보컬로이드 소모임 플레이리스트.xlsx"
# program_dir = sys.argv[0]
# file_name = sys.argv[1]
try:
    playlist = Playlist(program_path=program_dir, file_path=file_name)
    playlist.get_excel_data()
    playlist.init_additional_data()
    playlist.add_data_using_excel_data()
    playlist.check_downloadable_link()
    playlist.download_data()
except Exception as e:
    if isinstance(e, CustomException):
        Logger.error(e)
    elif isinstance(e, UserInvokedException):
        input("Enter키를 눌러 프로그램을 종료합니다...")
    else:
        Logger.error("에러가 발생했습니다. 아래는 구체적인 에러 메세지 입니다.")
        print(e)

