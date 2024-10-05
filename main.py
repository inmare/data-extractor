from playlist_generator import Playlist
from playlist_generator.error import CustomException, UserInvokedException
from playlist_generator.logger import Logger
from playlist_generator.download_data import set_ffmpeg_path
import os
import sys

# program_path = os.path.join(sys.argv[0])
# file_name = os.path.join(
#     "10월 플레이리스트.xlsx"
# )  # "2024년 8월 보컬로이드 소모임 플레이리스트.xlsx"
program_path = sys.argv[0]
file_name = sys.argv[1]
try:

    playlist = Playlist(program_path=program_path, file_path=file_name)
    playlist.get_excel_data()
    playlist.init_additional_data()
    playlist.process_excel_data()

    non_yt_link_contained = playlist.check_downloadable_link()
    if non_yt_link_contained:
        Logger.debug(
            "일부 다운가능한 링크가 유튜브 링크가 아닙니다. 다운로드를 계속하려면 yes를, 아니라면 no를 입력하고 Enter를 눌러주세요."
        )
        answer = None
        while answer not in ["yes", "no"]:
            answer = input("다운로드를 계속 하시겠습니까?: ")
            if answer == "yes":
                break
            elif answer == "no":
                raise UserInvokedException()

    set_ffmpeg_path(playlist.program_dir)
    playlist.init_dl_path()
    playlist.download_and_update_status()

    all_data_downloaded = playlist.check_dl_status()
    while not all_data_downloaded:
        Logger.debug(
            "모든 데이터가 다운로드 되지 않았습니다. 다시 다운로드를 시도하려면 yes를, 이대로 압축을 진행하려면 no를 입력하고 Enter를 눌러주세요."
        )
        answer = None
        while answer not in ["yes", "no"]:
            answer = input("다운로드를 다시 시도하시겠습니까?: ")
            if answer == "yes":
                playlist.download_and_update_status(retry=True)
                all_data_downloaded = playlist.check_dl_status()
            elif answer == "no":
                break
        if answer == "no":
            break

    playlist.create_json_file()
    playlist.create_zip_file()
    playlist.delete_files()
    Logger.info("플레이리스트 파일 생성이 완료되었습니다.")
    input("Enter키를 눌러 프로그램을 종료합니다...")

except Exception as e:
    if isinstance(e, CustomException):
        Logger.error(e)
    elif isinstance(e, UserInvokedException):
        Logger.debug("프로그램을 종료합니다.")
        input("Enter키를 눌러 프로그램을 종료합니다...")
    else:
        Logger.error("에러가 발생했습니다. 아래는 구체적인 에러 메세지 입니다.")
        Logger.error(e)
