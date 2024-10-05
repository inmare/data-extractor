# from . import excel_data, json_data
# from .download_data import download_data
# from .project_config import DlDataType
# from . import project_config as config
# from .log_print import log_print, LogType
# import zipfile
# import shutil

import os
from .error import CustomException, UserInvokedException
from .excel_file import ExcelFile
from . import excel_data as ExcelData
from .configs import ExcelDataCfg, AdditionalDataCfg, DownloadDataCfg, PathCfg
from . import additional_data as AdditionalData
from . import download_data as DownloadData
from . import file_managment as FileManagment
from .logger import Logger
from .utils import get_current_time


class Playlist:
    def __init__(self, program_path: str, file_path: str) -> None:
        self.program_dir = os.path.dirname(program_path)
        self.file_path = file_path
        self.excel_file = ExcelFile(self.file_path)
        self.excel_data = None
        self.additional_data = None
        self.created_time = get_current_time()

    def get_excel_data(self):
        """
        파일 경로에서 엑셀 데이터를 가져오는 메서드
        """
        ordered_data = ExcelData.get_data_order(self.excel_file.data_sheet)
        self.excel_data = ExcelData.get_data(self.excel_file.data_sheet, ordered_data)

    def init_additional_data(self) -> None:
        array = []
        for _ in range(len(self.excel_data)):
            array.append({})
        self.additional_data = array

    def process_excel_data(self):
        """
        엑셀 데이터를 이용해서 파일 이름이랑 유튜브 링크 여부를 추가하는 메서드
        """
        if not self.excel_data:
            raise CustomException("엑셀 데이터가 존재하지 않습니다.")

        Logger.debug("곡명과 다운가능한 링크를 추가적으로 검사하는 중입니다.")

        for idx, data in enumerate(self.excel_data):
            song_name = data[ExcelDataCfg.SongNameKor.keyname]
            file_name = AdditionalData.process_file_name(song_name)
            if song_name != file_name:
                Logger.debug(f"{song_name}의 파일명을 {file_name}으로 설정했습니다.")
            self.additional_data[idx][AdditionalDataCfg.FileName.keyname] = file_name

            downloadable_link = data[ExcelDataCfg.DownloadableLink.keyname]
            is_youtube_link = AdditionalData.is_youtube_link(downloadable_link)

            self.additional_data[idx][
                AdditionalDataCfg.IsYoutubeLink.keyname
            ] = is_youtube_link

    def check_downloadable_link(self) -> bool:
        """
        다운가능한 링크에 유튜브 링크가 아닌 것이 있는지 검사함

        Returns:
            bool: 유튜브 링크가 아닌 것이 하나라도 있으면 True, 아니면 False
        """
        non_yt_link_contained = False
        for idx, data in enumerate(self.additional_data):
            if not data[AdditionalDataCfg.IsYoutubeLink.keyname]:
                person_name = self.excel_data[idx][ExcelDataCfg.Name.keyname]
                downloadable_link = self.excel_data[idx][
                    ExcelDataCfg.DownloadableLink.keyname
                ]
                Logger.warning(
                    f"{person_name}님의 다운가능한 링크가 유튜브 링크가 아닙니다."
                )
                Logger.warning(downloadable_link)
                non_yt_link_contained = True

        Logger.info("곡명과 다운가능한 링크 검사를 완료했습니다.")

        return non_yt_link_contained

    def init_dl_path(self):
        """
        다운로드 받을 폴더를 삭제 후 다시 생성하는 메서드
        """
        FileManagment.create_folder(self.program_dir, PathCfg.MusicDir)
        FileManagment.create_folder(self.program_dir, PathCfg.ThumbnailDir)

    def download_and_update_status(self, retry: bool = False):
        """
        노래와 썸네일을 다운로드 받고 다운로드 여부를 추가 데이터에 업데이트함

        Args:
            retry (bool, optional): 다운로드를 다시 시도할지 여부
        """
        if retry:
            # 만약에 재시도라면 다운로드 여부를 확인하고 다시 다운로드 받기
            music_dl_key = AdditionalDataCfg.MusicDownloaded.keyname
            thumbnail_dl_key = AdditionalDataCfg.ThumbnailDownloaded.keyname
            for data in self.additional_data:
                if (
                    not music_dl_key in data.keys()
                    or not thumbnail_dl_key in data.keys()
                ):
                    raise CustomException(
                        "아직 노래나 썸네일이 다운로드 된 상태가 아닙니다."
                    )
            Logger.info("다시 다운로드를 시도합니다.")
        else:
            Logger.info(
                "노래와 썸네일의 다운로드를 시작합니다. 유튜브 영상 다운로드 프로그램의 메세지가 일부 표시될 수 있습니다."
            )

        for idx, data in enumerate(self.playlist_data):
            downloadable_link = data[ExcelDataCfg.DownloadableLink.keyname]
            file_name = data[AdditionalDataCfg.FileName.keyname]
            song_name = data[ExcelDataCfg.SongNameKor.keyname]

            if retry:
                music_downloaded = data[AdditionalDataCfg.MusicDownloaded.keyname]
                if music_downloaded:
                    continue

            # 노래 다운로드
            music_dl_option = DownloadData.set_dl_options(
                self.program_dir, file_name, DownloadDataCfg.Music
            )

            music_dl_status = DownloadData.download_data(
                self.program_dir,
                song_name,
                music_dl_option,
                downloadable_link,
                DownloadDataCfg.Music,
            )

            self.additional_data[idx][
                AdditionalDataCfg.MusicDownloaded.keyname
            ] = music_dl_status

        for idx, data in enumerate(self.playlist_data):
            downloadable_link = data[ExcelDataCfg.DownloadableLink.keyname]
            file_name = data[AdditionalDataCfg.FileName.keyname]
            song_name = data[ExcelDataCfg.SongNameKor.keyname]

            if retry:
                thumbnail_downloaded = data[
                    AdditionalDataCfg.ThumbnailDownloaded.keyname
                ]
                if thumbnail_downloaded:
                    continue

            # 썸네일 다운로드
            thumbnail_dl_option = DownloadData.set_dl_options(
                self.program_dir, file_name, DownloadDataCfg.Thumbnail
            )

            thumbnail_dl_status = DownloadData.download_data(
                self.program_dir,
                song_name,
                thumbnail_dl_option,
                downloadable_link,
                DownloadDataCfg.Thumbnail,
                file_name,
            )

            self.additional_data[idx][
                AdditionalDataCfg.ThumbnailDownloaded.keyname
            ] = thumbnail_dl_status

    def check_dl_status(self) -> bool:
        """
        노래와 썸네일이 전부 다운로드 되었는지 확인함.

        Returns:
            bool: 전부 다운로드 되었으면 True, 하나라도 다운로드가 안되었으면 False
        """

        all_data_downloaded = True
        for idx, add_data in enumerate(self.additional_data):
            song_name = self.excel_data[idx][ExcelDataCfg.SongNameKor.keyname]
            if not add_data[AdditionalDataCfg.MusicDownloaded.keyname]:
                Logger.warning(f'"{song_name}"의 노래가 다운로드 되지 않았습니다.')
                all_data_downloaded = False
            if not add_data[AdditionalDataCfg.ThumbnailDownloaded.keyname]:
                Logger.warning(f'"{song_name}"의 썸네일이 다운로드 되지 않았습니다.')
                all_data_downloaded = False

        if all_data_downloaded:
            Logger.info("모든 데이터가 다운로드 되었습니다.")

        return all_data_downloaded

    def create_json_file(self):
        """
        플레이리스트에 대한 정보를 담은 json파일을 생성하는 메서드
        """
        try:
            json_data = []
            for data in self.playlist_data:
                for value in ExcelDataCfg:
                    if value.export:
                        json_data.append(data[value.keyname])

                for value in AdditionalDataCfg:
                    if value.export:
                        json_data.append(data[value.keyname])

            FileManagment.save_json_file(
                self.program_dir, f"{self.file_prefix}.json", json_data
            )
        except Exception as e:
            raise e

    def create_zip_file(self):
        """
        다운로드한 노래, 썸네일 파일로 zip파일을 생성하는 메서드
        """
        try:
            Logger.debug("다운로드한 파일들로 압축파일 생성을 시작합니다...")
            original_path = []
            save_path = []

            music_folder_rel_path = PathCfg.MusicDir.value
            thumbnail_folder_rel_path = PathCfg.ThumbnailDir.value

            music_folder_path = os.path.join(self.program_dir, music_folder_rel_path)
            thumbnail_folder_path = os.path.join(
                self.program_dir, thumbnail_folder_rel_path
            )

            # 노래, 썸네일 파일 경로 추가
            # TODO: 나중에 적절한 함수로 따로 분리하기
            for data in self.playlist_data:
                # 노래나 썸네일의 경로가 존재할 때만 배열에 추가
                file_name = data[AdditionalDataCfg.FileName.keyname]

                music_ext = "mp3"
                music_file_path = os.path.join(
                    music_folder_path, f"{file_name}.{music_ext}"
                )

                if os.path.exists(music_file_path):
                    original_path.append(music_file_path)
                    save_path.append(
                        os.path.join(music_folder_rel_path, f"{file_name}.{music_ext}")
                    )

                thumbnail_ext = "png"
                thumbnail_file_path = os.path.join(
                    thumbnail_folder_path, f"{file_name}.{thumbnail_ext}"
                )

                if os.path.exists(thumbnail_file_path):
                    original_path.append(thumbnail_file_path)
                    save_path.append(
                        os.path.join(
                            thumbnail_folder_rel_path, f"{file_name}.{thumbnail_ext}"
                        )
                    )

            # json 파일 경로 추가
            json_file_name = f"{self.file_prefix}.json"
            json_file_path = os.path.join(self.program_dir, json_file_name)

            if os.path.exists(json_file_path):
                original_path.append(json_file_path)
                save_path.append(os.path.join(json_file_name))

            zip_file_name = f"{self.file_prefix}.zip"

            FileManagment.save_zip_file(
                self.program_dir, zip_file_name, original_path, save_path
            )
            Logger.info(f"압축 파일을 생성했습니다.")
            Logger.info(f"생성된 압축 파일 이름은 {zip_file_name} 입니다.")
        except Exception as e:
            raise e

    def delete_files(self):
        Logger.debug("기존에 생성된 파일과 폴더들을 삭제합니다.")
        FileManagment.delete_folder(self.program_dir, PathCfg.MusicDir)
        FileManagment.delete_folder(self.program_dir, PathCfg.ThumbnailDir)
        json_file_name = f"{self.file_prefix}.json"
        FileManagment.delete_file(self.program_dir, json_file_name)
        Logger.info("삭제가 완료되었습니다.")

    @property
    def playlist_data(self):
        """
        엑셀 데이터와 추가 데이터를 합쳐서 플레이리스트 데이터를 반환하는 프로퍼티
        """
        if not self.excel_data or not self.additional_data:
            raise CustomException("엑셀 데이터와 추가 데이터를 먼저 불러와주세요.")

        playlist_data = []
        for i in range(len(self.excel_data)):
            playlist_data.append({**self.excel_data[i], **self.additional_data[i]})

        return playlist_data

    @property
    def file_prefix(self):
        """
        파일 이름에 사용될 접두사를 반환하는 프로퍼티
        """
        if not self.excel_file.date:
            raise CustomException("엑셀 파일의 날짜 정보가 없습니다.")

        return FileManagment.get_file_prefix(self.excel_file.date, self.created_time)


if __name__ == "__main__":
    pass
